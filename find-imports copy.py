#find-imports.py

import os
import re
import logging
import argparse

def setup_logging():
    log_dir = './logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'find_imports.log')

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ])

def find_imports(directory):
    """
    This function searches for Python import statements in all .py files within the given directory
    and returns a set of unique module names.
    
    Parameters:
        directory (str): The path to the directory to search.
    
    Returns:
        set: A set of unique module names imported in the Python files.
    """
    imports = set()
    logging.info(f"Searching for imports in directory: {directory}")
    for root, _, files in os.walk(directory):
        logging.debug(f"Walking through directory: {root}")
        if '.conda' in root:
            logging.debug(f"Skipping directory: {root}")
            continue
        for file in files:
            logging.debug(f"Found file: {file}")
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                logging.info(f"Processing file: {file_path}")
                try:
                    with open(file_path, 'r') as f:
                        for line in f:
                            match = re.match(r'^\s*(?:import|from)\s+([^\s]+)', line)
                            if match and match.group(1).strip():
                                imports.add(match.group(1).split('.')[0].strip())
                except Exception as e:
                    logging.error(f"Error reading file {file}: {e}")
    return imports

def list_directories(base_directory):
    """
    List immediate subdirectories within the given base directory, sorting hidden directories first and then alphabetically.
    
    Parameters:
        base_directory (str): The path to the base directory to search.
    
    Returns:
        list: A list of directory paths.
    """
    directories = [d.path for d in os.scandir(base_directory) if d.is_dir() and '.conda' not in d.path]
    directories = [d.replace(base_directory, '').lstrip('/.') for d in directories]
    directories.sort(key=lambda d: (not d.startswith('.'), d.lower()))
    logging.debug(f"Directories found: {directories}")
    return directories

def list_python_files(directory):
    """
    List all .py files within the given directory.
    
    Parameters:
        directory (str): The path to the directory to search.
    
    Returns:
        list: A list of Python file paths.
    """
    python_files = []
    logging.info(f"Listing Python files in directory: {directory}")
    for root, _, files in os.walk(directory):
        logging.debug(f"Checking directory: {root}")
        if '.conda' in root:
            logging.debug(f"Skipping directory: {root}")
            continue
        for file in files:
            logging.debug(f"Found file: {file}")
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    logging.debug(f"Python files found: {python_files}")
    return python_files

def truncate(text, length):
    """
    Truncate the text to a specified length, adding '...' if it exceeds that length.
    
    Parameters:
        text (str): The text to truncate.
        length (int): The maximum length of the text.
    
    Returns:
        str: The truncated text.
    """
    return text if len(text) <= length else text[:length - 3] + '...'

def clear_screen():
    """
    Clear the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def display_directories(directories):
    """
    Display directories in a table format with numbers next to them.
    
    Parameters:
        directories (list): A list of directory paths to display.
    """
    column_width = 70  # Set the width for the directory column
    print("\033[34m+----+------------------------------------------------------------------------+\033[0m")
    for i, directory in enumerate(directories, 1):
        truncated_directory = truncate(directory, column_width)
        print(f"\033[34m|\033[0m \033[33m{i:<2}\033[0m \033[34m|\033[0m \033[33m{truncated_directory:<70}\033[0m \033[34m|\033[0m")
    print("\033[34m+----+------------------------------------------------------------------------+\033[0m")

def display_files(files):
    """
    Display files in a table format with numbers next to them.
    
    Parameters:
        files (list): A list of file paths to display.
    """
    column_width = 70  # Set the width for the file column
    clear_screen()
    print("\033[34m+------------------------------------------------------------------------+\033[0m")
    for i, file in enumerate(files, 1):
        truncated_file = truncate(file, column_width)
        print(f"\033[34m|\033[0m \033[33m{truncated_file:<70}\033[0m \033[34m|\033[0m")
    print("\033[34m+------------------------------------------------------------------------+\033[0m")

def display_imports(imports):
    """
    Display the list of imports in a box format.
    
    Parameters:
        imports (list): A list of import statements to display.
    """
    clear_screen()
    print("\033[34m+------------------------------------------------------------------------+\033[0m")
    for imp in imports:
        print(f"\033[34m|\033[0m \033[33m{imp:<70}\033[0m \033[34m|\033[0m")
    print("\033[34m+------------------------------------------------------------------------+\033[0m\n")

def main():
    setup_logging()
    clear_screen()
    
    startpath = input(f"\033[32mEnter the directory path to list (default: {os.getcwd()}, e.g., ~/dev/): \033[0m").strip() or os.getcwd()
    startpath = os.path.expanduser(startpath)
    
    if not os.path.isdir(startpath):
        logging.error("The specified base directory does not exist.")
        return
    
    directories = list_directories(startpath)
    if not directories:
        logging.info("No directories found in the specified base directory.")
        return
    
    clear_screen()
    display_directories(directories)
    
    choice = input(f"\n\033[32mEnter the number of the directory to analyze (default is: {startpath}): \033[0m").strip()
    
    if choice:
        try:
            choice = int(choice)
            if choice < 1 or choice > len(directories):
                logging.error("Invalid choice. Please enter a valid number.")
                return
            selected_directory = os.path.join(startpath, directories[choice - 1])
        except ValueError:
            logging.error("Invalid input. Please enter a number.")
            return
    else:
        selected_directory = startpath
    
    logging.info(f"Selected directory: {selected_directory}")
    
    python_files = list_python_files(selected_directory)
    if not python_files:
        logging.info("No Python files found in the selected directory.")
        return

    clear_screen()
    display_files(python_files)
    
    confirm = input(f"\n\033[32mDo you want to analyze the above {len(python_files)} files? (y/n default=y): \033[0m").strip().lower()
    if confirm not in ['yes', 'y', '']:
        logging.info("Operation cancelled by the user.")
        return
    
    imports = find_imports(selected_directory)
    
    print("\n\033[34m+------------------------------------------------------------------------+\033[0m")
    for imp in sorted(imports):
        print(f"\033[34m|\033[0m \033[33m{imp:<70}\033[0m \033[34m|\033[0m")
    print("\033[34m+------------------------------------------------------------------------+\033[0m\n")

    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "identified_imports.txt")

    with open(output_file, "w") as f:
        for imp in sorted(imports):
            f.write(f"{imp}\n")
    
    logging.info(f"Identified imports have been written to {output_file}")

if __name__ == "__main__":
    main()
