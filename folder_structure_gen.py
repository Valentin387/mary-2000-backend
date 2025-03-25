import os
import argparse

def generate_tree(directory, prefix="", ignored_folders={"env", ".vscode", "node_modules", "__pycache__"}):
    """Recursively generates a tree structure of the given directory, ignoring specified folders."""
    entries = sorted(os.listdir(directory))
    entries = [e for e in entries if not e.startswith(".") and e not in ignored_folders]  # Ignore hidden and specified folders
    
    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = index == len(entries) - 1
        connector = "└── " if is_last else "├── "
        print(prefix + connector + entry)
        
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            generate_tree(path, new_prefix, ignored_folders)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a tree structure of the given folder.")
    parser.add_argument("directory", nargs="?", default=os.getcwd(), help="Path to the folder (default: current directory)")
    args = parser.parse_args()
    
    print(args.directory)
    print("\nProject Structure:")
    generate_tree(args.directory)
