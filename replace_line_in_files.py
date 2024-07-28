# replace_line_in_files.py

# This script searches for files with a specified extension in a directory,
# finds an exact line in each file, and replaces that line with a new line.
# The extension, line to replace, and new line can be provided as command-line arguments
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

def replace_line_in_file(file_path, line_to_replace, new_line):
    """
    Replace the specified line in the file with a new line and log each replacement.

    Parameters:
        file_path (str): Path to the file.
        line_to_replace (str): The exact line to replace in the file.
        new_line (str): The new line to replace the old line with.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            for line in lines:
                if line.strip() == line_to_replace:
                    file.write(new_line + '\n')
                    logging.info(f"Replaced line in file {file_path}: {line.strip()} with {new_line}")
                else:
                    file.write(line)

        logging.info(f"Completed processing file: {file_path}")

    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")

def process_files(directory, extension, line_to_replace, new_line):
    """
    Process all files in the directory with the specified extension,
    replacing the specified line with a new line in each file.

    Parameters:
        directory (str): Directory to search for files.
        extension (str): File extension to filter by.
        line_to_replace (str): The exact line to replace in the files.
        new_line (str): The new line to replace the old line with.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                logging.debug(f"Processing file: {file_path}")
                replace_line_in_file(file_path, line_to_replace, new_line)

def main():
    parser = argparse.ArgumentParser(description="Replace an exact line in all files of a specified type in a directory.")
    parser.add_argument('--extension', help="File extension to filter by (e.g., .txt)")
    parser.add_argument('--line', help="The exact line to replace in the files")
    parser.add_argument('--new_line', help="The new line to replace the old line with")

    args = parser.parse_args()

    script_name = os.path.basename(sys.argv[0])
    setup_logging(script_name)
    clear_screen()

    directory = os.getcwd()
    extension = args.extension or get_user_input("Enter the file extension to filter by", ".txt")
    line_to_replace = args.line or get_user_input("Enter the exact line to replace", "Sample line to replace")
    new_line = args.new_line or get_user_input("Enter the new line to replace the old line with", "New sample line")

    logging.info(f"Starting to process files in directory: {directory}")
    process_files(directory, extension, line_to_replace, new_line)
    logging.info("Operation completed successfully.")

if __name__ == '__main__':
    main()
