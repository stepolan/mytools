# replace_string_in_files.py

# This script searches for files with a specified extension in a directory,
# finds all occurrences of a specified string in each file, and replaces them with a new string.
# The extension, string to find, and new string can be provided as command-line arguments
# or will be prompted from the user if not provided.

import os
import argparse
import logging
import sys

def setup_logging(script_name):
    """Setup logging configuration."""
    log_dir = './logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'{script_name}.log')

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ])

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input(prompt, default_value):
    """Prompt the user for input, returning a default value if none provided."""
    user_input = input(f"\033[32m{prompt} (default: {default_value}): \033[0m").strip()
    return user_input or default_value

def replace_string_in_file(file_path, string_to_find, new_string):
    """
    Replace all occurrences of the specified string in the file with a new string and log each replacement.

    Parameters:
        file_path (str): Path to the file.
        string_to_find (str): The string to find in the file.
        new_string (str): The new string to replace the old string with.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        new_content = content.replace(string_to_find, new_string)

        with open(file_path, 'w') as file:
            file.write(new_content)

        logging.info(f"Replaced string in file {file_path}: '{string_to_find}' with '{new_string}'")

    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")

def process_files(directory, extension, string_to_find, new_string):
    """
    Process all files in the directory with the specified extension,
    replacing the specified string with a new string in each file.

    Parameters:
        directory (str): Directory to search for files.
        extension (str): File extension to filter by.
        string_to_find (str): The string to find in the files.
        new_string (str): The new string to replace the old string with.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                logging.debug(f"Processing file: {file_path}")
                replace_string_in_file(file_path, string_to_find, new_string)

def main():
    parser = argparse.ArgumentParser(description="Replace a string in all files of a specified type in a directory.")
    parser.add_argument('--extension', help="File extension to filter by (e.g., .txt)")
    parser.add_argument('--string', help="The string to find in the files")
    parser.add_argument('--new_string', help="The new string to replace the old string with")

    args = parser.parse_args()

    script_name = os.path.basename(sys.argv[0])
    setup_logging(script_name)
    clear_screen()

    directory = os.getcwd()
    extension = args.extension or get_user_input("Enter the file extension to filter by", ".txt")
    string_to_find = args.string or get_user_input("Enter the string to find", "old_string")
    new_string = args.new_string or get_user_input("Enter the new string to replace the old string with", "new_string")

    logging.info(f"Starting to process files in directory: {directory}")
    process_files(directory, extension, string_to_find, new_string)
    logging.info("Operation completed successfully.")

if __name__ == '__main__':
    main()
