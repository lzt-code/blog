import os
import re
import sys

# 用仓库根目录执行也能 import 同目录的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import image_host
from image_host import (
    BLOG_ROOT,
    IMAGE_REPO_LOCAL_PATH,
    IMAGE_REPO_NAME,
    GITHUB_USER,
)
from mermaid_to_png import process_mermaid_content
from svg_to_png import batch_convert_svg_to_png


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

    # 简单判断是否配置了用户信息
    if GITHUB_USER == "your_username":
        print("警告: 你还没有配置 GITHUB_USER，生成的链接可能无法访问。")
        print("请打开 script/image_host.py 修改图床配置区域。")
        print("-" * 50)

    # --- 1. Mermaid 代码块转 PNG（只在内存里替换，不写回原文件）---
    working_content, mermaid_pngs = process_mermaid_content(content, file_path)

    # --- 2. SVG 转 PNG ---
    svg_paths = sorted({
        rec["abs_path"] for rec in image_host.find_local_images(working_content, file_path)
        if rec["abs_path"].lower().endswith(".svg") and os.path.isfile(rec["abs_path"])
    })
    generated_pngs = batch_convert_svg_to_png(svg_paths) if svg_paths else []

    convert_map = {}
    for svg_path in svg_paths:
        png_path = os.path.splitext(svg_path)[0] + ".png"
        if os.path.isfile(png_path):
            convert_map[svg_path] = png_path

    # --- 3. 正文引用的本地图片全部上传图床 ---
    upload_files = sorted({
        convert_map.get(rec["abs_path"], rec["abs_path"])
        for rec in image_host.find_local_images(working_content, file_path)
        if os.path.isfile(convert_map.get(rec["abs_path"], rec["abs_path"]))
    })
    ok, mapping, detail = image_host.upload_images(IMAGE_REPO_LOCAL_PATH, upload_files)
    print(f"图床: {detail}")
    if not ok:
        print("警告：图片上传失败，生成的链接可能无法访问！")

    # --- 4. 正文引用替换为 CDN 链接 ---
    final_content, records = image_host.rewrite_image_links(
        working_content, file_path, mapping=mapping, convert_map=convert_map
    )
    for rec in records:
        if rec["status"] == "missing":
            print(f"警告: 本地图片不存在，引用保持原样 -> {rec['raw']}")

    # 将代码块空格替换为 HTML 不换行空格
    final_content = convert_code_block_spaces_to_nbsp(final_content)

    output_dir = os.path.join(BLOG_ROOT, "temp")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "预览.md")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print("="*20 + " 转换成功 " + "="*20)
    print(f"已保存到: {output_path}")
    print("  (原始文件保持不变，保留了 Mermaid 代码块和原始链接)")
    print("="*50)
    print(f"\n[提示] 请确保你已经将图片推送到 GitHub: https://github.com/{GITHUB_USER}/{IMAGE_REPO_NAME}")

    # 清理本地临时生成的 PNG 图片（图床已有，预览里走 CDN）
    generated_files = generated_pngs + mermaid_pngs
    if generated_files:
        print("\n正在清理本地临时生成的 PNG 图片...")
        for file in generated_files:
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
