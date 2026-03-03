import os

def scan_project(project_path):
    files_content = []

    excluded_dirs = ["Drivers", "Middlewares"]

    for root, dirs, files in os.walk(project_path):

        if any(excluded in root for excluded in excluded_dirs):
            continue
        for file in files:
            if file.endswith(".c") or file.endswith(".h"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        files_content.append(content)
                except Exception as e:
                    print(f"Could not read {full_path}: {e}")

    return files_content