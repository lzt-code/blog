"""GitHub 图床公共逻辑。

内容哈希命名、本地路径解析、复制进图床仓库 + git 提交推送、Markdown 图片链接改写。
export_wechat.py（公众号预览）和 prepare_images.py（多平台同步）共用这一份实现，
改图床配置或文件名规则只改这里，别在调用方再抄一遍。
"""

import hashlib
import os
import re
import shutil
import subprocess
from urllib.parse import quote

# ================= 图床配置 =================
GITHUB_USER = "lzt-code"
IMAGE_REPO_NAME = "blog-images"
IMAGE_REPO_BRANCH = "main"

# CDN 域名 (可选用: gcore.jsdelivr.net, fastly.jsdelivr.net, cdn.jsdelivr.net)
CDN_DOMAIN = "gcore.jsdelivr.net"

# 图床仓库里的图片目录（扁平化存储，不按文章分目录）
IMG_DIR_NAME = "img"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_ROOT = os.path.dirname(CURRENT_DIR)
WORKSPACE_ROOT = os.path.dirname(BLOG_ROOT)
# 图床仓库本地路径
IMAGE_REPO_LOCAL_PATH = os.path.join(WORKSPACE_ROOT, IMAGE_REPO_NAME)
# ===========================================

# 已经是公网地址的引用，不处理
REMOTE_PREFIXES = ("http://", "https://", "//", "data:", "ftp://")

# ![alt](path)、![alt](<path>)、![alt](path "title")
IMAGE_RE = re.compile(
    r'!\[(?P<alt>[^\]]*)\]\(\s*(?P<path><[^>]*>|[^()\s]+)(?P<title>\s+"[^"]*")?\s*\)'
)


def get_file_hash(file_path):
    """计算文件的 MD5 哈希值。"""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()


def get_unique_filename(file_path):
    """生成唯一文件名: filename_hash8.ext，同名不同内容不会互相覆盖。"""
    base_name = os.path.basename(file_path)
    if not os.path.exists(file_path):
        return base_name

    file_hash = get_file_hash(file_path)
    name, ext = os.path.splitext(base_name)
    return f"{name}_{file_hash[:8]}{ext}"


def build_cdn_url(file_name, cdn_domain=CDN_DOMAIN, user=GITHUB_USER,
                  repo=IMAGE_REPO_NAME, branch=IMAGE_REPO_BRANCH):
    """拼出 jsDelivr 地址，非 ASCII 文件名和空格会被转义。"""
    return (
        f"https://{cdn_domain}/gh/{user}/{repo}@{branch}/"
        f"{IMG_DIR_NAME}/{quote(file_name)}"
    )


def is_remote(rel_path):
    """判断引用是否已经是公网地址 / 内联数据。"""
    lowered = rel_path.strip().lower()
    return lowered.startswith(REMOTE_PREFIXES)


def resolve_local_path(rel_path, md_file_path):
    """解析 Markdown 图片引用。

    返回 (相对仓库根目录的路径, 绝对路径)；公网引用返回 (None, None)。
    以 / 开头的路径按仓库根目录解析，其他按 Markdown 文件所在目录解析。
    """
    raw = rel_path.strip()
    if raw.startswith("<") and raw.endswith(">"):
        raw = raw[1:-1]

    if is_remote(raw):
        return None, None

    raw = raw.replace("\\", "/")
    if raw.startswith("/"):
        abs_path = os.path.abspath(os.path.join(BLOG_ROOT, raw.lstrip("/")))
    else:
        md_dir = os.path.dirname(os.path.abspath(md_file_path))
        abs_path = os.path.abspath(os.path.join(md_dir, raw))

    return os.path.relpath(abs_path, BLOG_ROOT), abs_path


def _map_outside_code(content, func):
    """逐行处理，跳过 ``` / ~~~ 围栏代码块里的内容（代码里的图片语法不算图片）。"""
    lines = content.split("\n")
    out = []
    in_fence = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append(line)
            continue
        out.append(line if in_fence else func(line))
    return "\n".join(out)


def find_local_images(content, md_file_path):
    """列出正文里所有本地图片引用。

    每项: {"alt": 替代文字, "raw": 原引用, "abs_path": 绝对路径}
    """
    records = []

    def scan(line):
        for m in IMAGE_RE.finditer(line):
            _, abs_path = resolve_local_path(m.group("path"), md_file_path)
            if abs_path is None:
                continue
            records.append({
                "alt": m.group("alt"),
                "raw": m.group("path"),
                "abs_path": abs_path,
            })
        return line

    _map_outside_code(content, scan)
    return records


def upload_images(image_repo_path, files, push=True):
    """把本地图片复制进图床仓库并推送。

    files: 绝对路径列表
    返回 (ok, mapping, detail)；mapping 为 {绝对路径: 图床文件名}。
    """
    mapping = {}

    if not os.path.isdir(image_repo_path):
        return False, mapping, (
            f"图床仓库不存在: {image_repo_path}"
            f"（请先 clone {IMAGE_REPO_NAME} 到 {WORKSPACE_ROOT}）"
        )

    targets = [os.path.abspath(f) for f in files]
    if not targets:
        return True, mapping, "没有图片需要上传"

    img_dir = os.path.join(image_repo_path, IMG_DIR_NAME)
    os.makedirs(img_dir, exist_ok=True)

    copied = 0
    cached = 0
    for src in targets:
        if not os.path.isfile(src):
            continue
        file_name = get_unique_filename(src)
        mapping[src] = file_name
        dst = os.path.join(img_dir, file_name)
        if os.path.isfile(dst) and get_file_hash(dst) == get_file_hash(src):
            cached += 1
            continue
        shutil.copy2(src, dst)
        copied += 1
        print(f"  复制到图床: {file_name}")

    if copied == 0:
        return True, mapping, f"{cached} 张图片已在图床，无需提交"

    # 先拉一次，避免远端有新提交导致 push 被拒；失败不阻断，继续按本地状态走
    subprocess.run(["git", "pull", "--rebase"], cwd=image_repo_path,
                   capture_output=True, text=True, check=False)

    add = subprocess.run(["git", "add", IMG_DIR_NAME], cwd=image_repo_path,
                         capture_output=True, text=True, check=False)
    if add.returncode != 0:
        return False, mapping, f"git add 失败: {(add.stderr or add.stdout).strip()}"

    status = subprocess.run(["git", "status", "--porcelain"], cwd=image_repo_path,
                            capture_output=True, text=True, check=False)
    if status.stdout.strip():
        commit = subprocess.run(
            ["git", "commit", "-m", f"chore(images): upload {copied} image(s)"],
            cwd=image_repo_path, capture_output=True, text=True, check=False,
        )
        if commit.returncode != 0:
            return False, mapping, f"git commit 失败: {(commit.stderr or commit.stdout).strip()}"
        print("  图床仓库已提交")

    if push:
        print("  正在推送图床仓库...")
        pushed = subprocess.run(["git", "push"], cwd=image_repo_path,
                                capture_output=True, text=True, check=False)
        if pushed.returncode != 0:
            detail = (pushed.stderr or pushed.stdout).strip()
            return False, mapping, f"git push 失败: {detail[-300:]}"
        print("  图床仓库推送成功")

    return True, mapping, f"新上传 {copied} 张，{cached} 张已在图床"


def rewrite_image_links(content, md_file_path, mapping=None, convert_map=None):
    """把正文里的本地图片引用换成图床链接。

    mapping: {绝对路径: 图床文件名}，来自 upload_images
    convert_map: {源绝对路径: 实际上传的绝对路径}，用于 SVG→PNG 这类替身
    返回 (new_content, records)，records 每项带 status:
      remote  - 本来就是公网链接，未改动
      cdn     - 已换成图床链接
      missing - 本地文件找不到，引用保持原样
    """
    mapping = mapping or {}
    convert_map = convert_map or {}
    records = []

    def replace_line(line):
        def _sub(m):
            alt = m.group("alt")
            raw = m.group("path")
            title = m.group("title") or ""

            _, abs_path = resolve_local_path(raw, md_file_path)
            if abs_path is None:
                records.append({"raw": raw, "abs_path": None, "url": None, "status": "remote"})
                return m.group(0)

            target = convert_map.get(abs_path, abs_path)
            file_name = mapping.get(target)
            if not file_name and os.path.isfile(target):
                file_name = get_unique_filename(target)

            if not file_name:
                records.append({"raw": raw, "abs_path": abs_path, "url": None, "status": "missing"})
                return m.group(0)

            url = build_cdn_url(file_name)
            records.append({"raw": raw, "abs_path": abs_path, "url": url, "status": "cdn"})
            return f"![{alt}]({url}{title})"

        return IMAGE_RE.sub(_sub, line)

    new_content = _map_outside_code(content, replace_line)
    return new_content, records
