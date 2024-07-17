# show_file_changes.py

"""
This script displays all changes made to a specific file in a Git repository.
It retrieves the commit history for the file and shows the changes for each commit.
"""

import os
import subprocess
import argparse

def get_commit_history(file_path):
    """
    Get the commit history for a specific file.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        list: A list of commit hashes affecting the file.
    """
    command = ["git", "log", "--follow", "--format=%H", file_path]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error getting commit history: {result.stderr}")
    return result.stdout.splitlines()

def show_file_changes(file_path):
    """
    Show changes for each commit affecting the specified file.

    Parameters:
        file_path (str): The path to the file.
    """
    commit_hashes = get_commit_history(file_path)
    for commit_hash in commit_hashes:
        command = ["git", "show", f"{commit_hash}:{file_path}"]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Error showing changes for commit {commit_hash}: {result.stderr}")
        print(f"Commit: {commit_hash}")
        print(result.stdout)
        print("-" * 80)

def main():
    """
    Main function to execute the script.
    """
    parser = argparse.ArgumentParser(description="Display all changes made to a specific file in a Git repository.")
    parser.add_argument("file_path", help="The path to the file.")
    
    args = parser.parse_args()
    file_path = args.file_path

    if not os.path.isfile(file_path):
        print("File not found. Please enter a valid file path.")
        return
    
    try:
        show_file_changes(file_path)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
