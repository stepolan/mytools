# combine-txt-files.py

# This script combines multiple text files into a single text file.
# It prompts the user for the directory containing the text files,
# reads each file, and writes their contents into an output file.

import os
import logging
import argparse

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

def combine_text_files(directory, output_file):
    """
    Combine multiple text files in the specified directory into a single text file.
    
    Parameters:
        directory (str): The path to the directory containing the text files.
        output_file (str): The path to the output file.
    """
    try:
        with open(output_file, 'w') as outfile:
            for filename in os.listdir(directory):
                if filename.endswith('.txt'):
                    file_path = os.path.join(directory, filename)
                    logging.info(f"Processing file: {file_path}")
                    with open(file_path, 'r') as infile:
                        outfile.write(infile.read())
                        outfile.write("\n")
        logging.info(f"All text files have been combined into {output_file}")
    except Exception as e:
        logging.error(f"Error combining text files: {e}")

def main():
    script_name = os.path.basename(__file__).split('.')[0]
    setup_logging(script_name)
    clear_screen()

    parser = argparse.ArgumentParser(description="Combine multiple text files into a single text file.")
    parser.add_argument("output_file", nargs='?', default='combined.txt', help="The output text file name (default: combined.txt).")
    args = parser.parse_args()

    startpath = input(f"\033[32mEnter the directory path containing the text files (default: {os.getcwd()}): \033[0m").strip() or os.getcwd()
    startpath = os.path.expanduser(startpath)

    if not os.path.exists(startpath):
        logging.error("The specified directory does not exist.")
        return

    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, args.output_file)

    combine_text_files(startpath, output_file)

if __name__ == "__main__":
    main()