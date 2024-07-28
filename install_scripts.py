# install_scripts.py

"""
This script lists all Python files in the current directory and its subdirectories.
It prompts the user whether they want to make each file executable and copy it to /usr/local/bin.
"""

import os
import sys
import shutil
import subprocess
import glob
import readline
import logging
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

# Setup logging
LOG_FILE = "./logs/script_installer.log"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
DESTINATION_DIR = '/usr/local/bin'
ZSHRC_PATH = os.path.expanduser('~/.zshrc')

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def complete_path(text, state):
    """Autocomplete function for directory paths."""
    results = glob.glob(text + '*') + [None]
    return results[state]

readline.set_completer_delims('\t')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete_path)

def highlight_path(path):
    """Highlights the '/' in a path with white color."""
    dirs = path.split('/')
    highlighted_dirs = [Fore.LIGHTGREEN_EX + part + Style.RESET_ALL if part != dirs[-1] else Fore.YELLOW + part + Style.RESET_ALL for part in dirs]
    return '/'.join(highlighted_dirs)

def copy_script(script_name, destination_path):
    """Copies the script to the destination path."""
    try:
        shutil.copy(script_name, destination_path)
        print(f"Copied {script_name} to {destination_path}")
        logging.info(f"Copied {script_name} to {destination_path}")
    except Exception as e:
        print(f"Error copying script: {e}")
        logging.error(f"Error copying script: {e}")

def make_executable(path):
    """Makes the script at the given path executable."""
    try:
        subprocess.run(['sudo', 'chmod', '+x', path], check=True)
        print(f"Made {path} executable")
        logging.info(f"Made {path} executable")
    except subprocess.CalledProcessError as e:
        print(f"Error making script executable: {e}")
        logging.error(f"Error making script executable: {e}")

def ensure_path_in_zshrc(destination_dir, zshrc_path):
    """Ensures the destination directory is in the PATH by updating .zshrc if necessary."""
    try:
        with open(zshrc_path, 'r') as file:
            lines = file.readlines()
        
        path_export = f'export PATH=$PATH:{destination_dir}\n'
        
        if path_export not in lines:
            with open(zshrc_path, 'a') as file:
                file.write(path_export)
            print(f"Added {destination_dir} to PATH in {zshrc_path}")
            logging.info(f"Added {destination_dir} to PATH in {zshrc_path}")
        else:
            print(f"{destination_dir} is already in PATH")
            logging.info(f"{destination_dir} is already in PATH")
        
        # Source the .zshrc file within a shell context
        subprocess.run(f'source {zshrc_path}', shell=True, executable='/bin/zsh', check=True)
        print("Sourced the .zshrc file")
        logging.info("Sourced the .zshrc file")
    except Exception as e:
        print(f"Error updating {zshrc_path}: {e}")
        logging.error(f"Error updating {zshrc_path}: {e}")

def prompt_include_all_files(files):
    """Prompt the user to include all found files."""
    print("The following Python files were found:\n")
    for file in files:
        print(Fore.LIGHTGREEN_EX + highlight_path(file) + Style.RESET_ALL)
    include_all = input("\nDo you want to include all these files? " +
                        Fore.WHITE + "(" + Fore.LIGHTGREEN_EX + "y" + Fore.WHITE + "/" + Fore.LIGHTRED_EX + "n" + Fore.WHITE + ") " +
                        Style.RESET_ALL + "[default: " + Fore.LIGHTGREEN_EX + "YES" + Style.RESET_ALL + "]: ")
    logging.debug(f"User input for include all files: {include_all}")
    return include_all.lower() in ["y", "yes", ""]

def prompt_include_file(file):
    """Prompt the user to include a single file."""
    include_file = input(f"Do you want to include this file: " +
                         Fore.LIGHTGREEN_EX + highlight_path(file) + Style.RESET_ALL + "? " +
                         Fore.WHITE + "(" + Fore.LIGHTGREEN_EX + "y" + Fore.WHITE + "/" + Fore.LIGHTRED_EX + "n" + Fore.WHITE + "/" + Fore.LIGHTYELLOW_EX + "s" + Fore.WHITE + ") " +
                         Style.RESET_ALL + "[default: " + Fore.LIGHTGREEN_EX + "YES" + Style.RESET_ALL + "]: ")
    logging.debug(f"User input for file {file}: {include_file}")
    return include_file.lower()

def find_python_files(directory):
    """
    Finds all Python files in the given directory and its subdirectories.

    Parameters:
        directory (str): The directory to search for Python files.

    Returns:
        list of str: List of Python file paths.
    """
    return glob.glob(os.path.join(directory, '**', '*.py'), recursive=True)

def main():
    logging.info("Script started")
    try:
        clear_screen()
        if len(sys.argv) > 1:
            python_files = [sys.argv[1]]
        else:
            current_directory = os.getcwd()
            python_files = find_python_files(current_directory)
        
        if not python_files:
            print(Fore.RED + "No Python files found in the current directory." + Style.RESET_ALL)
            logging.warning("No Python files found in the current directory.")
            return
        
        if prompt_include_all_files(python_files):
            files_to_include = python_files
        else:
            files_to_include = []
            for file in python_files:
                user_choice = prompt_include_file(file)
                if user_choice in ["y", "yes", ""]:
                    files_to_include.append(file)
                elif user_choice in ["s", "skip"]:
                    break
        
        for file in files_to_include:
            destination_path = os.path.join(DESTINATION_DIR, os.path.basename(file))
            copy_script(file, destination_path)
            make_executable(destination_path)
        
        ensure_path_in_zshrc(DESTINATION_DIR, ZSHRC_PATH)
        
        print(Fore.GREEN + "Selected files have been copied and made executable." + Style.RESET_ALL)
        logging.info("Selected files have been copied and made executable.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
    finally:
        logging.info("Script ended")

if __name__ == "__main__":
    main()