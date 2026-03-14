import shutil
import re
import sys
import os
import subprocess

# 导入新提取的 SVG 转换逻辑
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from svg_to_png import batch_convert_svg_to_png
from mermaid_to_png import process_mermaid_content

# ================= 配置区域 =================
# 图床仓库信息
GITHUB_USER = "lzt-code"
IMAGE_REPO_NAME = "blog-images"
IMAGE_REPO_BRANCH = "main"

# CDN 域名配置 (可选用: gcore.jsdelivr.net, fastly.jsdelivr.net, cdn.jsdelivr.net)
CDN_DOMAIN = "gcore.jsdelivr.net"

# 图床仓库本地路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_ROOT = os.path.dirname(CURRENT_DIR)
WORKSPACE_ROOT = os.path.dirname(BLOG_ROOT)
IMAGE_REPO_LOCAL_PATH = os.path.join(WORKSPACE_ROOT, IMAGE_REPO_NAME)
# ===========================================

def upload_images_and_verify(image_repo_path, files_to_upload):
    """
    将文件复制到图床仓库并提交
    files_to_upload: 绝对路径列表
    """
    if not os.path.exists(image_repo_path):
        print(f"错误：图床仓库路径不存在: {image_repo_path}")
        print(f"请确保你已经 clone 了 {IMAGE_REPO_NAME} 仓库到 {WORKSPACE_ROOT}")
        return False
    
    target_dir = os.path.join(image_repo_path, "img")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    print(f"\n正在处理图床仓库: {image_repo_path}")
    
    added_count = 0
    for src_path in files_to_upload:
        if os.path.exists(src_path):
            file_name = os.path.basename(src_path)
            # 扁平化存储：直接放在 img/ 下，注意同名文件覆盖问题
            dst_path = os.path.join(target_dir, file_name)
            shutil.copy2(src_path, dst_path)
            added_count += 1
            print(f"  复制到图床: {file_name}")
    
    if added_count == 0:
        print("  没有文件需要上传到图床")
        return True
        
    # Git 操作
    try:
        # 1. git pull (先拉取最新代码，避免冲突)
        print("  执行 git pull...")
        subprocess.run(["git", "pull"], cwd=image_repo_path, check=False)

        # 2. git add
        subprocess.run(["git", "add", "."], cwd=image_repo_path, check=True)
        
        # 3. git commit
        status = subprocess.run(["git", "status", "--porcelain"], cwd=image_repo_path, capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", "Auto upload images"], cwd=image_repo_path, check=True)
            print("  图床仓库已提交")
            
            # 4. git push
            print("  正在推送图床仓库...")
            subprocess.run(["git", "push"], cwd=image_repo_path, check=True)
            print("  图床仓库推送成功")
        else:
            print("  图床仓库无变更，跳过提交")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  图床仓库 Git 操作失败: {e}")
        return False
    except Exception as e:
        print(f"  图床仓库操作出错: {e}")
        return False

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
    # 格式: https://{CDN_DOMAIN}/gh/user/repo@branch/img/
    # 注意：这里假设所有图片都上传到了 blog-images/img/ 目录下
    cdn_prefix = f"https://{CDN_DOMAIN}/gh/{GITHUB_USER}/{IMAGE_REPO_NAME}@{IMAGE_REPO_BRANCH}/img/"

    # 简单判断是否配置了用户信息
    if GITHUB_USER == "your_username":
        print("警告: 你还没有配置 GITHUB_USER，生成的链接可能无法访问。")
        print("请打开 script/export_wechat.py 修改配置区域。")
        print("-" * 50)

    # --- 0.5 扫描并转换 Mermaid ---
    content, mermaid_pngs = process_mermaid_content(content, file_path)

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

    # --- 1.2 更新原始文件中的链接 (SVG -> PNG) ---
    # 用户要求：图片转换完成后修改文章中的链接，链接替换为png图片
    
    def update_source_link(match):
        alt = match.group(1)
        link = match.group(2)
        
        # 忽略网络链接
        if link.startswith("http:") or link.startswith("https:"):
            return match.group(0)
            
        # 如果是 SVG，替换后缀并增加 CDN 前缀
        if link.lower().endswith('.svg'):
            local_rel_path, _ = resolve_local_path(link, file_path)
            if local_rel_path:
                # 替换后缀
                png_filename = os.path.basename(local_rel_path)
                png_filename = os.path.splitext(png_filename)[0] + ".png"
                
                # 拼接 CDN (使用扁平化的文件名)
                full_url = cdn_prefix + png_filename
                return f"![{alt}]({full_url})"
            
        return match.group(0)

    # 对 content 进行替换 (注意 content 此时已经包含了 Mermaid 的替换结果)
    new_source_content = re.sub(r'!\[(.*?)\]\((.*?)\)', update_source_link, content)
    
    # 将修改后的内容写回原文件
    # 这样本地 Markdown 文件中的链接也会被更新为 PNG，且 Mermaid 代码块会被替换为图片链接
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_source_content)
        print(f"  已更新原始文件链接: {file_path}")
    except Exception as e:
        print(f"  更新原始文件失败: {e}")
    
    # 更新 content 变量，供后续生成预览使用
    content = new_source_content
                
    all_generated_files = generated_pngs + mermaid_pngs

    # --- 1.6 上传图片到图床并验证 ---
    if all_generated_files:
        if not upload_images_and_verify(IMAGE_REPO_LOCAL_PATH, all_generated_files):
            print("警告：图片上传失败，生成的链接可能无法访问！")

    # --- 2. 替换链接 (用于生成预览文件) ---
    # 正则替换：匹配 ![](./xxx) 或 ![](xxx) 这种相对路径
    
    def replace_link(match):
        alt_text = match.group(1)
        rel_path = match.group(2)
        
        local_rel_path, abs_path = resolve_local_path(rel_path, file_path)
        
        if local_rel_path is None:
            # 网络链接
            return match.group(0)
            
        # 检查是否是 SVG，如果是，替换为 PNG 后缀
        filename = os.path.basename(local_rel_path)
        if filename.lower().endswith('.svg'):
            filename = os.path.splitext(filename)[0] + ".png"
            
        # 拼接完整 CDN 链接 (扁平化)
        full_url = cdn_prefix + filename
        
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
    print(f"\n[提示] 请确保你已经将图片推送到 GitHub: https://github.com/{GITHUB_USER}/{IMAGE_REPO_NAME}")

    # 清理本地临时生成的 PNG 图片
    if all_generated_files:
        print("\n正在清理本地临时生成的 PNG 图片...")
        for file in all_generated_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"  已清理: {file}")
            except Exception as e:
                print(f"  清理失败 {file}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python script/export_wechat.py <markdown文件路径>")
        print("示例: python script/export_wechat.py \"Flutter版本选择指南/2026-01.md\"")
    else:
        convert_to_wechat_format(sys.argv[1])
