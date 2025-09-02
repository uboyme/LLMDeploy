import os

def print_one_level(path):
    try:
        items = sorted(os.listdir(path))
    except FileNotFoundError:
        print(f"路径不存在: {path}")
        return
    except PermissionError:
        print(f"没有权限访问: {path}")
        return

    print(path)
    for name in items:
        # 跳过 .svg 文件
        if name.lower().endswith(".svg"):
            continue
        print("├── " + name)

if __name__ == "__main__":
    root_dir = r"C:\\develop\\LLMDeploy\\sys-webui-main"  # 你要查看的目录
    print_one_level(root_dir)
