# remove_line_from_files.py

# This script searches for files with a specified extension in a directory,
# finds an exact line in each file, and removes that line.
# The extension and line to remove can be provided as command-line arguments
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

def remove_line_from_file(file_path, line_to_remove):
    """
    Remove the specified line from the file and log each removal.

    Parameters:
        file_path (str): Path to the file.
        line_to_remove (str): The exact line to remove from the file.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            for line in lines:
                if line.strip() != line_to_remove:
                    file.write(line)
                else:
                    logging.info(f"Removed line from file {file_path}: {line.strip()}")

        logging.info(f"Completed processing file: {file_path}")

    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")

def process_files(directory, extension, line_to_remove):
    """
    Process all files in the directory with the specified extension,
    removing the specified line from each file.

    Parameters:
        directory (str): Directory to search for files.
        extension (str): File extension to filter by.
        line_to_remove (str): The exact line to remove from the files.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                logging.debug(f"Processing file: {file_path}")
                remove_line_from_file(file_path, line_to_remove)

def main():
    parser = argparse.ArgumentParser(description="Remove an exact line from all files of a specified type in a directory.")
    parser.add_argument('--extension', help="File extension to filter by (e.g., .txt)")
    parser.add_argument('--line', help="The exact line to remove from the files")

    args = parser.parse_args()

    script_name = os.path.basename(sys.argv[0])
    setup_logging(script_name)
    clear_screen()

    directory = os.getcwd()
    extension = args.extension or get_user_input("Enter the file extension to filter by", ".txt")
    line_to_remove = args.line or get_user_input("Enter the exact line to remove", "Sample line to remove")

    logging.info(f"Starting to process files in directory: {directory}")
    process_files(directory, extension, line_to_remove)
    logging.info("Operation completed successfully.")

if __name__ == '__main__':
    main()