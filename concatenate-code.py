import os
import logging
import readline
import glob
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

# Constants
OUTPUT_FILE = "./output/concatenate-code.txt"
LOG_FILE = "./logs/concatenate-code.log"

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def expand_path(path):
    """Expands the tilde to the user's home directory if present in the path."""
    return os.path.expanduser(path)

def complete_path(text, state):
    """Autocomplete function for directory paths."""
    results = glob.glob(text + '*') + [None]
    return results[state]

readline.set_completer_delims('\t')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete_path)

def find_files(directory, extensions):
    """Finds all files in the given directory and its subdirectories that match the specified extensions."""
    logging.info(f"Searching for files in directory: {directory} with extensions: {extensions}")
    files_to_concatenate = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                files_to_concatenate.append(os.path.relpath(os.path.join(root, file)))
    logging.info(f"Found {len(files_to_concatenate)} files to concatenate.")
    return files_to_concatenate

def highlight_path(path):
    """Highlights the '/' in a path with white color."""
    dirs = path.split('/')
    highlighted_dirs = [Fore.LIGHTGREEN_EX + part + Style.RESET_ALL if part != dirs[-1] else Fore.YELLOW + part + Style.RESET_ALL for part in dirs]
    return '/'.join(highlighted_dirs)

def prompt_include_all_files(files):
    """Prompt the user to include all found files."""
    print("The following files were found:\n")
    for file in files:
        print(Fore.LIGHTGREEN_EX + highlight_path(file) + Style.RESET_ALL)
    include_all = input("\nDo you want to include all these files in all directories? " +
                        Fore.WHITE + "(" + Fore.LIGHTGREEN_EX + "y" + Fore.WHITE + "/" + Fore.LIGHTRED_EX + "n" + Fore.WHITE + ") " +
                        Style.RESET_ALL + "[default: " + Fore.LIGHTGREEN_EX + "YES" + Style.RESET_ALL + "]: ")
    logging.debug(f"User input for include all files: {include_all}")
    return include_all.lower() in ["y", "yes", ""]

def prompt_include_directory(directory, excluded_directories):
    """Prompt the user to include a directory."""
    if any(directory.startswith(excluded) for excluded in excluded_directories):
        logging.info(f"Automatically excluding directory {directory} and its files due to parent exclusion.")
        return False
    
    include_directory = input(f"Do you want to include this directory: " +
                              Fore.LIGHTGREEN_EX + highlight_path(directory) + Style.RESET_ALL + "? " +
                              Fore.WHITE + "(" + Fore.LIGHTGREEN_EX + "y" + Fore.WHITE + "/" + Fore.LIGHTRED_EX + "n" + Fore.WHITE + ") " +
                              Style.RESET_ALL + "[default: " + Fore.LIGHTGREEN_EX + "YES" + Style.RESET_ALL + "]: ")
    logging.debug(f"User input for directory {directory}: {include_directory}")
    return include_directory.lower() in ["y", "yes", ""]

def prompt_include_all_files_in_directories():
    """Prompt the user to include all files in included directories."""
    include_all = input("Do you want to include all files in the included directories? " +
                        Fore.WHITE + "(" + Fore.LIGHTGREEN_EX + "y" + Fore.WHITE + "/" + Fore.LIGHTRED_EX + "n" + Fore.WHITE + ") " +
                        Fore.CYAN + "[default: " + Fore.LIGHTGREEN_EX + "YES" + Style.RESET_ALL + "]: ")
    logging.debug(f"User input for include all files in directories: {include_all}")
    return include_all.lower() in ["y", "yes", ""]

def prompt_include_file(file, excluded_directories):
    """Prompt the user to include a file."""
    if any(file.startswith(excluded) for excluded in excluded_directories):
        logging.info(f"Automatically excluding file {file} due to parent directory exclusion.")
        return False
    
    include_file = input(f"Do you want to include this file: " +
                         Fore.LIGHTGREEN_EX + highlight_path(os.path.dirname(file)) + "/" + Fore.YELLOW + os.path.basename(file) + Style.RESET_ALL + "? " +
                         Fore.WHITE + "(" + Fore.LIGHTGREEN_EX + "y" + Fore.WHITE + "/" + Fore.LIGHTRED_EX + "n" + Fore.WHITE + ") " +
                         Fore.CYAN + "[default: " + Fore.LIGHTGREEN_EX + "YES" + Style.RESET_ALL + "]: ")
    logging.debug(f"User input for file {file}: {include_file}")
    return include_file.lower() in ["y", "yes", ""]

def confirm_directories(files):
    """Confirm directories with the user."""
    directories = sorted(set(os.path.dirname(file) for file in files))
    logging.info(f"Directories to confirm: {directories}")
    included_files = []
    excluded_directories = set()

    for directory in directories:
        if prompt_include_directory(directory, excluded_directories):
            included_files.extend([file for file in files if file.startswith(directory) and file not in included_files])
            logging.info(f"Including directory {directory} and its files.")
        else:
            excluded_directories.add(directory)
            logging.info(f"Excluding directory {directory} and its files.")

    return included_files, excluded_directories

def confirm_files(files, excluded_directories):
    """Confirm files with the user."""
    logging.info(f"Files to confirm: {files}")
    confirmed_files = []
    for file in files:
        if prompt_include_file(file, excluded_directories):
            confirmed_files.append(file)
            logging.info(f"Including file {file}.")
        else:
            logging.info(f"Excluding file {file}.")
    return confirmed_files

def concatenate_files(files, output_file):
    """Concatenates the content of the specified files into a single output file."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as outfile:
        outfile.write("List of files being concatenated:\n")
        for file in files:
            outfile.write(f"{file}\n")
        
        for file in files:
            outfile.write("\n" + "#" * 45 + "\n")
            outfile.write(f"#   {file}\n")
            outfile.write("#" * 45 + "\n\n")
            with open(file, "r") as infile:
                outfile.write(infile.read())
            outfile.write("\n")
    logging.info(f"Concatenated {len(files)} files into {output_file}")

def prompt_file_types():
    """Prompt the user to select the types of files to include."""
    file_extensions = []
    extension_prompts = [
        (".py", "Do you want to grab *.py files? ", True),
        (".js", "Do you want to grab *.js files? ", False),
        (".html", "Do you want to grab *.html files? ", False),
        (".json", "Do you want to grab *.json files? ", False),
        (".md", "Do you want to grab *.md files? ", False),
    ]

    for ext, prompt, default in extension_prompts:
        default_str = "YES" if default else "NO"
        include = input(prompt + Fore.WHITE + "(" + Fore.LIGHTGREEN_EX + "y" + Fore.WHITE + "/" + Fore.LIGHTRED_EX + "n" + Fore.WHITE + ") " +
                        Style.RESET_ALL + f"[default: {Fore.LIGHTGREEN_EX if default else Fore.LIGHTRED_EX}{default_str}{Style.RESET_ALL}]: ")
        if include.lower() in ["y", "yes", ""] if default else include.lower() in ["y", "yes"]:
            file_extensions.append(ext)
    logging.debug(f"Selected file extensions: {file_extensions}")
    return file_extensions

def main():
    """Main function to execute the script logic."""
    try:
        starting_directory = input("Enter the starting directory " +
                                   Fore.GREEN + "[default: current directory]: " + Style.RESET_ALL) or "."
        starting_directory = expand_path(starting_directory)
        logging.debug(f"Starting directory: {starting_directory}")
        # clear_screen()

        file_extensions = prompt_file_types()
        # clear_screen()

        files_to_concatenate = find_files(starting_directory, file_extensions)
        logging.debug(f"Files to concatenate: {files_to_concatenate}")

        if not files_to_concatenate:
            print(Fore.RED + "No files found to concatenate." + Style.RESET_ALL)
            logging.warning("No files found to concatenate.")
        else:
            if prompt_include_all_files(files_to_concatenate):
                confirmed_files = files_to_concatenate
                excluded_directories = set()
            else:
                confirmed_files, excluded_directories = confirm_directories(files_to_concatenate)
                logging.debug(f"Confirmed directories: {confirmed_files}")
                if not prompt_include_all_files_in_directories():
                    confirmed_files = confirm_files(confirmed_files, excluded_directories)
                    logging.debug(f"Confirmed files: {confirmed_files}")

            if confirmed_files:
                concatenate_files(confirmed_files, OUTPUT_FILE)
                print(Fore.GREEN + f"All selected files have been concatenated into {OUTPUT_FILE}" + Style.RESET_ALL)
                logging.info(f"Successfully concatenated files into {OUTPUT_FILE}")
            else:
                print(Fore.YELLOW + "No files were selected for concatenation." + Style.RESET_ALL)
                logging.info("No files were selected for concatenation.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
