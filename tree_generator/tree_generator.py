import os

def print_tree(startpath, prefix="", ignored_folders=None):
    """Recursively prints the directory tree structure, ignoring specified folders."""
    if ignored_folders is None:
        ignored_folders = []

    for item in os.listdir(startpath):
        path = os.path.join(startpath, item)

        # Check if the current item is a directory and should be ignored
        if os.path.isdir(path):
            if item in ignored_folders:
                continue  # Skip this folder

            print(f"{prefix}├── {item}/")  # Directory
            print_tree(path, prefix + "│   ", ignored_folders)  # Recursive call for subdirectory
        else:
            print(f"{prefix}├── {item}")  # File

if __name__ == "__main__":
    print("Directory structure:")
    # Specify the directory you want to start from
    directory = r"C:\Users\willi\IdeaProjects\06ScapeBot-master"
    ignored_folders = ["positive", "negative", "fish_bot", "farmer", ".git", ".idea"]  # Folders to ignore
    print_tree(directory, ignored_folders=ignored_folders)  # Pass ignored folders
