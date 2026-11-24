"""把文章里的本地图片处理成图床链接，产出一份可直接同步到多平台的稿子。

流程：Mermaid 代码块转 PNG -> SVG 转 PNG -> 连同普通本地图片按内容哈希复制进
blog-images 仓库并推送 -> 正文引用全部换成 jsDelivr 链接 -> 写出新文件。
原文章文件不动。

用法:
    python script/prepare_images.py "Flutter版本选择指南/2026-11.md"
    python script/prepare_images.py "Flutter版本选择指南/2026-11.md" --dry-run
    python script/prepare_images.py "Flutter版本选择指南/2026-11.md" --output temp/同步稿.md

退出码:
    0 图片全部就绪，可以同步
    1 参数 / 文件问题
    2 图床仓库或 git 推送失败
    3 有本地图片找不到，同步出去会是坏图
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import image_host
from mermaid_to_png import process_mermaid_content
from svg_to_png import batch_convert_svg_to_png


def read_markdown(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="gbk") as f:
            return f.read()


def default_output_path(md_path):
    """temp/sync/<相对路径用下划线拼起来>.md，避免同名的月份文件互相覆盖。"""
    rel = os.path.relpath(os.path.abspath(md_path), image_host.BLOG_ROOT)
    stem = os.path.splitext(rel)[0].replace("\\", "_").replace("/", "_")
    return os.path.join(image_host.BLOG_ROOT, "temp", "sync", f"{stem}.md")


def convert_diagrams(content, md_path):
    """Mermaid 和 SVG 转 PNG，返回 (新正文, {源绝对路径: PNG绝对路径}, 生成的PNG列表)。"""
    working_content, mermaid_pngs = process_mermaid_content(content, md_path)

    svg_paths = sorted({
        rec["abs_path"] for rec in image_host.find_local_images(working_content, md_path)
        if rec["abs_path"].lower().endswith(".svg") and os.path.isfile(rec["abs_path"])
    })
    generated_pngs = batch_convert_svg_to_png(svg_paths) if svg_paths else []

    convert_map = {}
    for svg_path in svg_paths:
        png_path = os.path.splitext(svg_path)[0] + ".png"
        if os.path.isfile(png_path):
            convert_map[svg_path] = png_path

    return working_content, convert_map, generated_pngs + mermaid_pngs


def collect_upload_files(content, md_path, convert_map):
    """正文里所有需要进图床的本地文件（SVG 取转换后的 PNG）。"""
    files = set()
    for rec in image_host.find_local_images(content, md_path):
        target = convert_map.get(rec["abs_path"], rec["abs_path"])
        if os.path.isfile(target):
            files.add(target)
    return sorted(files)


def cleanup_generated(paths):
    """删掉本地临时生成的 PNG（图床已有，稿子里走 CDN）。"""
    for path in paths:
        try:
            if os.path.isfile(path):
                os.remove(path)
        except OSError as e:
            print(f"  临时文件清理失败 {path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="把文章本地图片上传 GitHub 图床并改写链接")
    parser.add_argument("markdown", help="文章 Markdown 路径")
    parser.add_argument("--output", help="输出文件路径，默认 temp/sync/<相对路径>.md")
    parser.add_argument("--dry-run", action="store_true", help="只列出要上传的图片，不写仓库不提交")
    parser.add_argument("--keep-generated", action="store_true", help="保留临时生成的 PNG")
    args = parser.parse_args()

    md_path = os.path.abspath(args.markdown)
    if not os.path.isfile(md_path):
        print(f"错误：找不到文章 {md_path}")
        return 1

    print(f"处理文章: {md_path}")
    content = read_markdown(md_path)

    working_content, convert_map, generated = convert_diagrams(content, md_path)
    files = collect_upload_files(working_content, md_path, convert_map)

    # 正文里引用了但本地不存在的图片，先报出来
    missing = [
        rec["raw"] for rec in image_host.find_local_images(working_content, md_path)
        if not os.path.isfile(convert_map.get(rec["abs_path"], rec["abs_path"]))
    ]

    print(f"共 {len(files)} 张图片需要进图床，{len(missing)} 处引用找不到本地文件")
    for path in files:
        print(f"  [IMG] {os.path.relpath(path, image_host.BLOG_ROOT)}")
    for raw in missing:
        print(f"  [MISS] {raw}")

    if args.dry_run:
        cleanup_generated(generated)
        print("dry-run：未写入图床仓库，未生成稿子")
        return 3 if missing else 0

    ok, mapping, detail = image_host.upload_images(image_host.IMAGE_REPO_LOCAL_PATH, files)
    print(f"图床: {detail}")
    if not ok:
        print("错误：图片没能推到图床，此时同步出去图片会 404，先修好再继续")
        return 2

    final_content, records = image_host.rewrite_image_links(
        working_content, md_path, mapping=mapping, convert_map=convert_map
    )

    output_path = os.path.abspath(args.output) if args.output else default_output_path(md_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    print("=" * 20 + " 图片链接映射 " + "=" * 20)
    for rec in records:
        if rec["status"] == "cdn":
            print(f"  [OK]   {rec['raw']}")
            print(f"         -> {rec['url']}")
        elif rec["status"] == "missing":
            print(f"  [MISS] {rec['raw']}（本地找不到，引用原样保留）")
    print("=" * 56)
    print(f"稿子已写出: {output_path}")
    print("标题仍从 frontmatter 取，结尾替换在这份稿子上做，原文章文件不动")

    if not args.keep_generated:
        cleanup_generated(generated)

    remaining = [rec["raw"] for rec in records if rec["status"] == "missing"]
    if remaining:
        print(f"警告：{len(remaining)} 处本地图片找不到，草稿会出现坏图")
        return 3

    print("图片全部就绪，可以同步")
    return 0


if __name__ == "__main__":
    sys.exit(main())
