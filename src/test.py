import os
import argparse

DEFAULT_IGNORE_DIRS = {".git", ".idea", ".vscode", "__pycache__", "node_modules", "dist", "build", ".venv", "venv"}
DEFAULT_IGNORE_EXTS = {".svg", ".png", ".jpg", ".jpeg", ".gif", ".map", ".ico"}

def should_skip_dir(dirname: str, ignore_dirs: set[str]) -> bool:
    return dirname in ignore_dirs

def should_skip_file(filename: str, ignore_exts: set[str]) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in ignore_exts

def print_tree(root: str, prefix: str, max_depth: int | None,
               ignore_dirs: set[str], ignore_exts: set[str], level: int = 0):
    try:
        entries = sorted(os.listdir(root))
    except PermissionError:
        print(prefix + "└── [Permission Denied]")
        return

    # 目录与文件分开，目录优先
    dirs = [e for e in entries if os.path.isdir(os.path.join(root, e)) and not should_skip_dir(e, ignore_dirs)]
    files = [e for e in entries if os.path.isfile(os.path.join(root, e)) and not should_skip_file(e, ignore_exts)]
    entries_ordered = dirs + files

    for idx, name in enumerate(entries_ordered):
        path = os.path.join(root, name)
        connector = "└── " if idx == len(entries_ordered) - 1 else "├── "
        print(prefix + connector + name)

        if os.path.isdir(path):
            if max_depth is None or level + 1 < max_depth:
                extension = "    " if idx == len(entries_ordered) - 1 else "│   "
                print_tree(path, prefix + extension, max_depth, ignore_dirs, ignore_exts, level + 1)

def main():
    parser = argparse.ArgumentParser(description="打印目录结构（支持忽略目录/后缀与最大深度）")
    parser.add_argument("root", nargs="?", default=".", help="起始目录（默认当前目录）")
    parser.add_argument("--max-depth", type=int, default=None, help="最大递归深度（默认不限制）")
    parser.add_argument("--ignore-dirs", nargs="*", default=None, help="要忽略的目录名（空格分隔）")
    parser.add_argument("--ignore-exts", nargs="*", default=None, help="要忽略的文件扩展名（含点）")
    parser.add_argument("--include-svgs", action="store_true", help="包含 .svg 文件（默认忽略）")
    args = parser.parse_args()

    ignore_dirs = set(args.ignore_dirs) if args.ignore_dirs is not None else DEFAULT_IGNORE_DIRS
    ignore_exts = set(args.ignore_exts) if args.ignore_exts is not None else set(DEFAULT_IGNORE_EXTS)
    if args.include_svgs:
        ignore_exts.discard(".svg")

    root = os.path.abspath(args.root)
    print(root)
    print_tree(root, "", args.max_depth, ignore_dirs, ignore_exts)

if __name__ == "__main__":
    # Windows 控制台若出现乱码，可在 PowerShell 执行： chcp 65001
    main()
