import re
import sys
import os
import subprocess

# 导入新提取的 SVG 转换逻辑
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from svg_to_png import batch_convert_svg_to_png

# ================= 配置区域 =================
# 请在此处填入你的 GitHub 信息
#  https://github.com/lzt-code/blog/
GITHUB_USER = "lzt-code"  # 你的 GitHub 用户名
REPO_NAME = "blog"             # 你的仓库名 (假设当前目录名为 blog，这里默认填 blog，请根据实际情况修改)
BRANCH = "main"                # 你的分支名 (通常是 main 或 master)
# ===========================================

def run_git_commands(files_to_add):
    """
    自动执行 git add 和 git commit -m "Auto convert svg to png"
    """
    if not files_to_add:
        return

    print("\n正在自动提交生成的 PNG 文件到 Git...")
    
    try:
        # 1. git add
        # 注意：文件路径可能包含空格，需要小心处理，subprocess.run 接受列表参数比较安全
        cmd_add = ["git", "add"] + files_to_add
        subprocess.run(cmd_add, check=True)
        print(f"  已添加 {len(files_to_add)} 个文件到暂存区")
        
        # 2. git commit
        # 检查是否有变更需要提交
        status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status_result.stdout.strip():
            cmd_commit = ["git", "commit", "-m", "Auto convert svg to png"]
            subprocess.run(cmd_commit, check=True)
            print("  已完成 Git 提交")
            print("  [重要] 请记得执行 'git push' 将更改推送到远程仓库！")
        else:
            print("  暂存区没有变化，跳过提交")
            
    except subprocess.CalledProcessError as e:
        print(f"  Git 操作失败: {e}")
    except Exception as e:
        print(f"  Git 操作出错: {e}")

def resolve_local_path(rel_path, md_file_path):
    """
    解析 Markdown 图片链接的本地路径
    返回: (相对项目根目录的路径, 绝对文件系统路径)
    """
    # 如果已经是网络链接
    if rel_path.startswith("http:") or rel_path.startswith("https:"):
        return None, None
        
    md_dir = os.path.dirname(md_file_path)
    
    if not rel_path.startswith("/"):
        # 相对路径 (./xxx 或 xxx)
        # 相对于 md 文件所在目录
        local_rel_path = os.path.normpath(os.path.join(md_dir, rel_path))
    else:
        # 绝对路径 (/assets/xxx)
        # 这里的绝对路径通常是指相对于项目根目录
        local_rel_path = rel_path.lstrip("/")
        local_rel_path = local_rel_path.lstrip("\\")
    
    # 获取绝对文件系统路径 (假设脚本在项目根目录运行)
    # 如果 md_file_path 是相对路径，local_rel_path 也是基于 CWD 的相对路径
    abs_path = os.path.abspath(local_rel_path)
    
    return local_rel_path, abs_path

def convert_to_wechat_format(file_path):
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                content = f.read()
        except Exception as e:
            print(f"读取文件失败: {e}")
            return

    # 构造 jsDelivr 的前缀
    # 格式: https://fastly.jsdelivr.net/gh/user/repo@branch/
    cdn_prefix = f"https://fastly.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@{BRANCH}/"

    # 简单判断是否配置了用户信息
    if GITHUB_USER == "your_username":
        print("警告: 你还没有配置 GITHUB_USER，生成的链接可能无法访问。")
        print("请打开 script/export_wechat.py 修改配置区域。")
        print("-" * 50)

    # --- 1. 扫描并转换 SVG ---
    matches = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
    svgs_to_convert = []
    
    for alt, rel_path in matches:
        if rel_path.lower().endswith('.svg'):
            _, abs_path = resolve_local_path(rel_path, file_path)
            if abs_path:
                svgs_to_convert.append(abs_path)
    
    # 去重
    svgs_to_convert = list(set(svgs_to_convert))
    
    generated_pngs = []
    if svgs_to_convert:
        generated_pngs = batch_convert_svg_to_png(svgs_to_convert)
                
    # --- 1.5 自动提交 Git ---
    if generated_pngs:
        run_git_commands(generated_pngs)

    # --- 2. 替换链接 ---
    # 正则替换：匹配 ![](./xxx) 或 ![](xxx) 这种相对路径
    
    def replace_link(match):
        alt_text = match.group(1)
        rel_path = match.group(2)
        
        local_rel_path, abs_path = resolve_local_path(rel_path, file_path)
        
        if local_rel_path is None:
            # 网络链接
            return match.group(0)
            
        # 检查是否是 SVG，如果是，替换为 PNG 后缀
        if local_rel_path.lower().endswith('.svg'):
            local_rel_path = os.path.splitext(local_rel_path)[0] + ".png"
            
        # 将反斜杠替换为正斜杠（Windows兼容）
        full_local_path = local_rel_path.replace("\\", "/")
        
        # 拼接完整 CDN 链接
        full_url = cdn_prefix + full_local_path
        
        return f"![{alt_text}]({full_url})"

    new_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_link, content)

    output_dir = "temp"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, "预览.md")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("="*20 + " 转换成功 " + "="*20)
    print(f"已保存到: {output_path}")
    print("="*50)
    print(f"\n[提示] 请确保你已经将图片推送到 GitHub: https://github.com/{GITHUB_USER}/{REPO_NAME}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python script/export_wechat.py <markdown文件路径>")
        print("示例: python script/export_wechat.py \"Flutter版本选择指南/2026-01.md\"")
    else:
        convert_to_wechat_format(sys.argv[1])
