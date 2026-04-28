import shutil
import re
import sys
import os
import subprocess
import hashlib

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

def get_file_hash(file_path):
    """计算文件的 MD5 哈希值"""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def get_unique_filename(file_path):
    """生成唯一文件名: filename_hash.ext"""
    if not os.path.exists(file_path):
        return os.path.basename(file_path)
        
    file_hash = get_file_hash(file_path)
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    # 使用前8位哈希即可
    return f"{name}_{file_hash[:8]}{ext}"

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
            # 使用内容哈希生成唯一文件名，防止重名覆盖
            file_name = get_unique_filename(src_path)
            # 扁平化存储：直接放在 img/ 下
            dst_path = os.path.join(target_dir, file_name)
            
            # 检查目标文件是否已存在且内容一致
            if os.path.exists(dst_path):
                # 如果文件已存在，可能是之前上传过，或者哈希碰撞（极小概率）
                # 既然是基于内容的哈希，内容应该是一样的，所以可以跳过，或者覆盖
                pass
            
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

def convert_code_block_spaces_to_nbsp(markdown_content):
    """将 fenced code block 中的普通空格替换为真实 NBSP 字符，避免公众号粘贴时空格被折叠。"""
    pattern = r'```[^\n]*\n[\s\S]*?```'
    nbsp_char = '\u00A0'

    def _replace_spaces_in_block(match):
        block = match.group(0)
        lines = block.split('\n')

        # 仅处理代码内容，不改动围栏行
        if len(lines) <= 2:
            return block

        for i in range(1, len(lines) - 1):
            lines[i] = lines[i].replace(' ', nbsp_char)

        return '\n'.join(lines)

    return re.sub(pattern, _replace_spaces_in_block, markdown_content)

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
    # 我们在副本上操作，不修改原始 content 变量（如果你后面还需要原始 content 的话）
    # 实际上这里直接修改 content 也可以，只要最后不写回原文件即可
    working_content, mermaid_pngs = process_mermaid_content(content, file_path)

    # --- 1. 扫描并转换 SVG ---
    matches = re.findall(r'!\[(.*?)\]\((.*?)\)', working_content)
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

    all_generated_files = generated_pngs + mermaid_pngs

    # --- 1.6 上传图片到图床并验证 ---
    if all_generated_files:
        if not upload_images_and_verify(IMAGE_REPO_LOCAL_PATH, all_generated_files):
            print("警告：图片上传失败，生成的链接可能无法访问！")

    # --- 2. 替换所有链接为 CDN 链接 ---
    def replace_with_cdn(match):
        alt_text = match.group(1)
        rel_path = match.group(2)
        
        local_rel_path, abs_path = resolve_local_path(rel_path, file_path)
        
        if local_rel_path is None:
            # 已经是网络链接
            return match.group(0)
            
        target_abs_path = abs_path
        
        # 处理 SVG -> PNG 的映射
        if rel_path.lower().endswith('.svg'):
            png_path = os.path.splitext(abs_path)[0] + ".png"
            if os.path.exists(png_path):
                target_abs_path = png_path
        
        # 获取最终文件名 (优先使用哈希唯一文件名)
        if os.path.exists(target_abs_path):
            # 只有在上传列表中的文件才强制使用哈希文件名（确保 CDN 链接正确）
            # 其他本地图片如果存在，也建议使用哈希文件名并上传（但此处逻辑仅处理已上传的）
            filename = get_unique_filename(target_abs_path)
        else:
            # 如果文件不存在（可能转换失败），回退到原始文件名
            filename = os.path.basename(target_abs_path)
            if filename.lower().endswith('.svg'):
                filename = os.path.splitext(filename)[0] + ".png"
            
        # 拼接完整 CDN 链接
        full_url = cdn_prefix + filename
        return f"![{alt_text}]({full_url})"

    final_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_with_cdn, working_content)

    # 将代码块空格替换为 HTML 不换行空格实体
    final_content = convert_code_block_spaces_to_nbsp(final_content)

    output_dir = "temp"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, "预览.md")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print("="*20 + " 转换成功 " + "="*20)
    print(f"已保存到: {output_path}")
    print("  (原始文件保持不变，保留了 Mermaid 代码块和原始链接)")
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
