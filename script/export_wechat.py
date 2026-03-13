import re
import sys
import os
import subprocess
import shutil

# 导入新提取的 SVG 转换逻辑
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from svg_to_png import batch_convert_svg_to_png
from mermaid_to_png import process_mermaid_content

# ================= 配置区域 =================
# 图床仓库信息
GITHUB_USER = "lzt-code"
IMAGE_REPO_NAME = "blog-images"
IMAGE_REPO_BRANCH = "main"
IMAGE_REPO_URL = f"https://github.com/{GITHUB_USER}/{IMAGE_REPO_NAME}.git"

# CDN 域名配置 (可选用: gcore.jsdelivr.net, fastly.jsdelivr.net, cdn.jsdelivr.net)
CDN_DOMAIN = "gcore.jsdelivr.net"


# 图床仓库本地路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_ROOT = os.path.dirname(CURRENT_DIR)
WORKSPACE_ROOT = os.path.dirname(BLOG_ROOT)
IMAGE_REPO_LOCAL_PATH = os.path.join(WORKSPACE_ROOT, IMAGE_REPO_NAME)
# ===========================================

def prepare_image_repo(repo_path, repo_url):
    """
    准备图床仓库：如果不存在则克隆，如果存在则拉取最新代码
    """
    if not os.path.exists(repo_path):
        print(f"正在克隆图床仓库到 {repo_path} ...")
        try:
            subprocess.run(["git", "clone", repo_url, repo_path], check=True)
        except subprocess.CalledProcessError:
            print(f"错误：无法克隆仓库 {repo_url}。请检查网络或手动克隆。")
            sys.exit(1)
    else:
        print(f"正在更新图床仓库 {repo_path} ...")
        try:
            subprocess.run(["git", "-C", repo_path, "pull"], check=True)
        except subprocess.CalledProcessError:
            print("警告：无法更新图床仓库，将尝试直接使用。")

def upload_images_and_verify(repo_path):
    """
    提交并推送图片，并验证推送结果
    """
    print("正在提交并推送图片...")
    try:
        subprocess.run(["git", "-C", repo_path, "add", "."], check=True)
        
        # 检查是否有变更
        status = subprocess.run(["git", "-C", repo_path, "status", "--porcelain"], capture_output=True, text=True).stdout
        if not status.strip():
            print("图床仓库没有变化，无需推送。")
            return True

        subprocess.run(["git", "-C", repo_path, "commit", "-m", "Upload blog images"], check=True)
        
        # 推送并验证
        push_result = subprocess.run(["git", "-C", repo_path, "push"], check=True)
        
        if push_result.returncode == 0:
            print("✅ 图片已成功推送到远程仓库！")
            return True
        else:
            print("❌ 推送失败，请检查 git 输出。")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 图床 Git 操作失败: {e}")
        return False

def resolve_local_path(rel_path, md_file_path):
    """
    解析 Markdown 图片链接的本地路径
    返回: (相对项目根目录的路径, 绝对文件系统路径)
    """
    if rel_path.startswith("http:") or rel_path.startswith("https:"):
        return None, None
        
    md_dir = os.path.dirname(md_file_path)
    
    if not rel_path.startswith("/"):
        local_rel_path = os.path.normpath(os.path.join(md_dir, rel_path))
    else:
        local_rel_path = rel_path.lstrip("/").lstrip("\\")
    
    abs_path = os.path.abspath(local_rel_path)
    return local_rel_path, abs_path

def convert_to_wechat_format(file_path):
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 {file_path}")
        return

    # 1. 准备图床仓库
    prepare_image_repo(IMAGE_REPO_LOCAL_PATH, IMAGE_REPO_URL)
    img_repo_dir = os.path.join(IMAGE_REPO_LOCAL_PATH, 'img')
    if not os.path.exists(img_repo_dir):
        os.makedirs(img_repo_dir)

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

    print(f"正在处理文章: {file_path}")

    # 记录已经移动/复制到图床的文件名，避免重复处理
    processed_filenames = set()

    # --- 2. 扫描并转换 Mermaid ---
    # content 会被更新（Mermaid 代码块 -> assets/xxx.png 链接）
    # generated_mermaid_pngs 是生成的本地 PNG 绝对路径列表
    content, generated_mermaid_pngs = process_mermaid_content(content, file_path)
    
    # 立即将 Mermaid 图片移动到图床仓库
    for png_path in generated_mermaid_pngs:
        if os.path.exists(png_path):
            filename = os.path.basename(png_path)
            dst_path = os.path.join(img_repo_dir, filename)
            shutil.move(png_path, dst_path)
            processed_filenames.add(filename)
            print(f"  已移动 Mermaid 图片: {filename} -> 图床")
    
    # 尝试清理空的 assets 目录
    assets_dir = os.path.join(os.path.dirname(file_path), 'assets')
    if os.path.exists(assets_dir) and not os.listdir(assets_dir):
        os.rmdir(assets_dir)
        print("  已清理空的 assets 目录")

    # --- 3. 扫描并转换 SVG ---
    matches = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
    svgs_to_convert = []
    
    for alt, rel_path in matches:
        if rel_path.lower().endswith('.svg'):
            _, abs_path = resolve_local_path(rel_path, file_path)
            if abs_path and os.path.exists(abs_path):
                svgs_to_convert.append(abs_path)
    
    svgs_to_convert = list(set(svgs_to_convert))
    if svgs_to_convert:
        generated_svg_pngs = batch_convert_svg_to_png(svgs_to_convert)
        # 立即将 SVG 转换的 PNG 图片移动到图床仓库
        for png_path in generated_svg_pngs:
            if os.path.exists(png_path):
                filename = os.path.basename(png_path)
                dst_path = os.path.join(img_repo_dir, filename)
                shutil.move(png_path, dst_path)
                processed_filenames.add(filename)
                print(f"  已移动 SVG 转换图片: {filename} -> 图床")

    # --- 4. 处理其他普通图片 ---
    # 再次扫描所有图片链接
    all_matches = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
    for alt, rel_path in all_matches:
        local_rel, abs_path = resolve_local_path(rel_path, file_path)
        
        if local_rel: # 是本地图片链接
            filename = os.path.basename(abs_path)
            
            # 如果是 SVG，我们在上面已经处理过并移动了对应的 PNG，
            # 这里只需要确保 filename 指向 PNG 即可
            if filename.lower().endswith('.svg'):
                filename = os.path.splitext(filename)[0] + ".png"
            
            # 如果这个文件已经在 processed_filenames 里，说明是刚刚生成并移动的，不用管
            if filename in processed_filenames:
                continue
                
            # 否则，这可能是一个普通的 PNG/JPG 图片，或者是之前就已经转换过的
            # 我们需要检查源文件是否存在，如果存在则复制
            # 注意：如果源链接是 SVG，abs_path 指向 SVG，但我们需要复制的是对应的 PNG（如果之前转换过但没移动？）
            # 不，如果是 SVG，上面的步骤已经重新转换并移动了。
            # 所以这里主要处理非 SVG 的普通图片。
            
            real_source_path = abs_path
            if abs_path.lower().endswith('.svg'):
                # SVG 的源文件不需要复制，因为我们只上传 PNG
                continue
            
            if os.path.exists(real_source_path):
                dst_path = os.path.join(img_repo_dir, filename)
                # 如果图床里没有，或者源文件更新，则复制
                if not os.path.exists(dst_path) or os.stat(real_source_path).st_mtime > os.stat(dst_path).st_mtime:
                    shutil.copy2(real_source_path, dst_path)
                    print(f"  已复制普通图片: {filename} -> 图床")
                processed_filenames.add(filename)

    # --- 5. 上传图片并验证 ---
    if not upload_images_and_verify(IMAGE_REPO_LOCAL_PATH):
        print("警告：图片上传失败，生成的链接可能无法访问！")
        # 这里可以选择是否继续替换链接，建议继续，因为用户可能稍后手动 push

    # --- 6. 替换链接为 CDN 地址 ---
    # 格式: https://{CDN_DOMAIN}/gh/user/repo@branch/img/filename
    cdn_prefix = f"https://{CDN_DOMAIN}/gh/{GITHUB_USER}/{IMAGE_REPO_NAME}@{IMAGE_REPO_BRANCH}/img/"
    
    def replace_link(match):
        alt_text = match.group(1)
        rel_path = match.group(2)
        
        local_rel_path, abs_path = resolve_local_path(rel_path, file_path)
        
        if local_rel_path is None:
            # 网络链接，保持原样
            return match.group(0)
            
        # 获取文件名
        filename = os.path.basename(abs_path)
        
        # 如果是 SVG，链接后缀改为 .png
        if filename.lower().endswith('.svg'):
            filename = os.path.splitext(filename)[0] + ".png"
            
        # 拼接完整 CDN 链接
        full_url = cdn_prefix + filename
        
        return f"![{alt_text}]({full_url})"

    new_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_link, content)

    # --- 7. 保存文件 (无备份) ---
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("="*20 + " 处理完成 " + "="*20)
    print(f"文章已更新: {file_path}")
    print(f"图片CDN根路径: {cdn_prefix}")
    print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python script/export_wechat.py <markdown文件路径>")
        print("示例: python script/export_wechat.py \"Flutter版本选择指南/2026-01.md\"")
    else:
        convert_to_wechat_format(sys.argv[1])
