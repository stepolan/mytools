import os
import logging
import argparse
import subprocess

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def list_files(startpath, include_hidden):
    """
    List all files and directories in the given directory.
    
    Parameters:
        startpath (str): The path to the directory to list.
        include_hidden (bool): Whether to include hidden files and directories.
    
    Returns:
        list: A list of file and directory paths.
    """
    output_lines = []
    for root, dirs, files in os.walk(startpath):
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * level + '├── '
        output_lines.append(f"{indent}{os.path.basename(root)}/")
        subindent = '│   ' * (level + 1) + '├── '
        for i, f in enumerate(files):
            if i == len(files) - 1:
                subindent = subindent.replace('├──', '└──')
            output_lines.append(f"{subindent}{f}")
    return output_lines

def save_to_file(output_lines, output_file):
    """
    Save the directory structure to a file.
    
    Parameters:
        output_lines (list): The lines of directory structure.
        output_file (str): The output file name.
    """
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            for line in output_lines:
                f.write(line + '\n')
        logging.info(f"Directory structure saved to {output_file}")
    except Exception as e:
        logging.error(f"Error writing to file: {e}")

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def copy_to_clipboard(file_path):
    """Copy the content of the file to the clipboard."""
    try:
        with open(file_path, 'r') as file:
            data = file.read()
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(data.encode('utf-8'))
        logging.info("Directory structure copied to clipboard.")
    except Exception as e:
        logging.error(f"Error copying to clipboard: {e}")

def main():
    """Main function to handle user input and list directory structure."""
    setup_logging()
    clear_screen()

    parser = argparse.ArgumentParser(description="List directory structure.")
    parser.add_argument("output_file", nargs='?', default='dirfn.txt', help="The output text file name (default: dirfn.txt).")
    args = parser.parse_args()

    startpath = input(f"\033[32mEnter the directory path to list (default: {os.getcwd()}, e.g., ~/dev/): \033[0m").strip() or os.getcwd()
    startpath = os.path.expanduser(startpath)
    output_file = os.path.join('./output', args.output_file)

    if not os.path.exists(startpath):
        logging.error("The specified directory does not exist.")
        return
    
    include_hidden = input("\033[32mDo you want to include hidden directories and files? (y/n): \033[0m").strip().lower() == 'y'
    
    output_lines = list_files(startpath, include_hidden)
    if not output_lines:
        logging.info("No files or directories found.")
        return

    clear_screen()
    print("\033[34mDirectory structure:\033[0m\n")
    for line in output_lines:
        print(line)

    save_to_file(output_lines, output_file)

    copy_to_clipboard_choice = input("\033[32mDo you want to copy the directory structure to the clipboard? (y/n): \033[0m").strip().lower()
    if copy_to_clipboard_choice == 'y':
        copy_to_clipboard(output_file)

if __name__ == "__main__":
    main()
