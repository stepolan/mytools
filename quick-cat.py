# quick-cat.py

"""
This script concatenates multiple files, adds a directory structure, and formats the content for markdown.

Purpose:
    The main goal of this script is to provide an organized and easy-to-read markdown document that includes
    multiple code files along with their directory structure. This is particularly useful for sharing with
    a Large Language Model (LLM) or other collaborators to quickly bring them up to speed with what you are
    working on. By providing both the content and the structure, it becomes easier to understand the context
    and relationships between the files.

Usage example:
    python quick-cat.py app.py ./source/config.py /static/js/javascript.js /templates/index.html -o combined_output.md --copy

    This command concatenates app.py, config.py, javascript.js, and index.html into a markdown file named combined_output.md,
    including a directory structure and syntax highlighting for each file's content. The --copy flag copies the output to the clipboard.

Arguments:
    files (list of str): List of file paths to concatenate.
    -o, --output (str): Output file name (default: output.md).
    --skip-prompt (bool): Skip adding the additional prompt content at the beginning.
    --copy (bool): Copy the output to the clipboard.

Output:
    The script produces a markdown file with the following features:
    - A visual representation of the directory structure of the input files.
    - Concatenated contents of each file, with appropriate markdown syntax highlighting based on file type.
"""


import os
import argparse
import logging
import platform
import subprocess
from pathlib import Path
import glob

# Constants
CHUNK_SIZE = 4096

# Sets up logging
def setup_logging(script_name):
    """Setup logging configuration to output logs to a file and console."""
    log_dir = './logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'{script_name}.log')

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ])

# Directory structure
def generate_directory_structure(files):
    """
    Generates a text representation of the directory structure for the given files.

    Parameters:
        files (list of str): List of file paths.

    Returns:
        list of str: Directory structure lines.
    """
    structure = []
    root = Path('.').resolve()
    for file in files:
        path = Path(file).resolve()
        try:
            relative_path = path.relative_to(root)
        except ValueError:
            relative_path = path  # If the path is not relative, use the absolute path
        parts = list(relative_path.parts)
        for i in range(len(parts)):
            part = parts[:i + 1]
            line = '│   ' * (len(part) - 1) + '├── ' + part[-1]
            if line not in structure:
                structure.append(line)
    return structure

# File types
def get_file_type(file):
    """
    Determines the file type based on the file extension.

    Parameters:
        file (Path): Path object of the file.

    Returns:
        str: File type string for markdown syntax highlighting.
    """
    ext = file.suffix.lower()
    file_types = {
        '.py': 'python',
        '.js': 'javascript',
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.log': '',
        '.txt': '',
        '.md': 'markdown',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.sh': 'shell',
        '.c': 'c',
        '.cpp': 'cpp',
        '.java': 'java',
        '.php': 'php',
        '.rb': 'ruby',
        '.go': 'go',
        '.swift': 'swift',
        '.rs': 'rust',
        '.pl': 'perl',
        '.ps1': 'powershell',
        '.bat': 'batch',
        '.vbs': 'vbscript',
        '.ini': 'ini',
        '.toml': 'toml',
        '.csv': 'csv',
        '.tsv': 'tsv',
        '.rst': 'rst',
        '.tex': 'tex',
        '.org': 'org',
        '.jsx': 'jsx',
        '.tsx': 'tsx'
    }
    return file_types.get(ext, '')

# Concatenation
def concatenate_files(files, output_file, skip_prompt=False):
    """
    Concatenates the content of multiple files, adds directory structure and file type annotations.

    Parameters:
        files (list of str): List of file paths to concatenate.
        output_file (str): The name of the output file.
        skip_prompt (bool): Whether to skip adding the additional prompt content at the beginning.
    """
    with open(output_file, 'w') as out_file:
        if not skip_prompt:
            # Write the LLM prompt
            out_file.write("You are a super helpful coding assistant!\n\n")
            out_file.write("Below you will find relevant files for a project I am working on. Please analyze these different files and confirm that you understand their purpose. Do not offer updates or show me code at this time. If you do not understand something, please ask me questions for clarification.\n\n")
            out_file.write("\n# When providing code help, please adhere to the following guidelines\n")
            out_file.write("\n1. **Provide Code in Sections**: Do not provide whole files. Instead, provide specific sections, functions, or lines as needed.\n")
            out_file.write("\n2. **Example for Line Changes**:\n")
            out_file.write("    - Change this line:\n")
            out_file.write("\n      ```python\n")
            out_file.write("      Old line here\n")
            out_file.write("      ```\n")
            out_file.write("\n    - To this:\n")
            out_file.write("\n      ```python\n")
            out_file.write("      New line here\n")
            out_file.write("      ```\n")
            out_file.write("\n**Note**: When providing markdown code boxes, escape internal backticks by using triple backslashes before the backticks.\n")
            out_file.write("\n## Style Guide for Writing Tools\n")
            out_file.write("\n### 1. **Introduction**\n")
            out_file.write("\n- Purpose of the Style Guide\n")
            out_file.write("- Importance of Consistency\n")
            out_file.write("\n## 2. **Script Header**\n")
            out_file.write("\n- **Script Name Comment**: Include the name of the script at the top as a comment. This helps identify the log and output files.\n")
            out_file.write("\n  ```python\n")
            out_file.write("  # script_name.py\n")
            out_file.write("  ```\n")
            out_file.write("\n- **Summary Comment**: Include a brief summary of the script's purpose and functionality in comments at the top, after the filename and a line break.\n")
            out_file.write("\n  ```python\n")
            out_file.write("  # script_name.py\n")
            out_file.write("\n  # This script combines multiple text files into a single text file.\n")
            out_file.write("  # It prompts the user for the directory containing the text files,\n")
            out_file.write("  # reads each file, and writes their contents into an output file.\n")
            out_file.write("  ```\n")
            out_file.write("\n## 3. **Imports**\n")
            out_file.write("\n- **Grouping Imports**: Group imports in the following order: standard library imports, related third-party imports, local application/library-specific imports.\n")
            out_file.write("- **Absolute Imports**: Use absolute imports when possible.\n")
            out_file.write("\n## 4. **Configuration Management**\n")
            out_file.write("\n- **Configuration Files**: Use configuration files for storing settings that might change frequently. This can help make your scripts more flexible and easier to manage.\n")
            out_file.write("\n  ```python\n")
            out_file.write("  import json\n")
            out_file.write("\n  def load_config(config_file):\n")
            out_file.write("      \"\"\"Load configuration settings from a file.\"\"\"\n")
            out_file.write("      with open(config_file, 'r') as f:\n")
            out_file.write("          config = json.load(f)\n")
            out_file.write("      return config\n")
            out_file.write("  ```\n")
            out_file.write("\n## 5. **Function Definitions**\n")
            out_file.write("\n- **Comment Titles**: Provide a concise title for every function as a comment above the function. Example:\n")
            out_file.write("\n  ```python\n")
            out_file.write("  # Data processing\n")
            out_file.write("  def process_data(data):\n")
            out_file.write("    \"\"\"\n")
            out_file.write("    Process the given data.\n")
            out_file.write("\n    Parameters:\n")
            out_file.write("        data (list): A list of data items to be processed.\n")
            out_file.write("\n    Returns:\n")
            out_file.write("        list: The processed data.\n")
            out_file.write("    \"\"\"\n")
            out_file.write("    print(f\"Processing data: {data}\")\n")
            out_file.write("    processed_data = [item * 2 for item in data]\n")
            out_file.write("    print(\"Data processing complete.\")\n")
            out_file.write("    return processed_data\n")
            out_file.write("  ```\n")
            out_file.write("\n- **Function Docstrings**: Provide a clear explanation of the function's purpose, parameters, and return values. Example:\n")
            out_file.write("\n  ```python\n")
            out_file.write("  # Example function\n")
            out_file.write("  def example_function(param1, param2):\n")
            out_file.write("      \"\"\"\n")
            out_file.write("      Brief description of the function.\n")
            out_file.write("\n      Parameters:\n")
            out_file.write("          param1 (type): Description of param1.\n")
            out_file.write("          param2 (type): Description of param2.\n")
            out_file.write("      \n")
            out_file.write("      Returns:\n")
            out_file.write("          return_type: Description of the return value.\n")
            out_file.write("      \"\"\"\n")
            out_file.write("  ```\n")
            out_file.write("\n- **Modular Code**: Break down tasks into small, reusable functions.\n")
            out_file.write("\n## 6. **Code Formatting**\n")
            out_file.write("\n- **Indentation**: Use 4 spaces for indentation.\n")
            out_file.write("- **Line Length**: Limit all lines to a maximum of 79 characters.\n")
            out_file.write("- **Blank Lines**: Use blank lines to separate top-level function and class definitions.\n")
            out_file.write("- **String Quotes**: In general, use single quotes for short strings and double quotes for longer strings or when a string contains a single quote.\n")
            out_file.write("- **Whitespace in Expressions and Statements**:\n")
            out_file.write("  - Avoid extraneous whitespace in the following situations: immediately inside parentheses, brackets or braces; immediately before a comma, semicolon, or colon; immediately before the open parenthesis that starts the argument list of a function call.\n")
            out_file.write("  - Use a single space around binary operators and after a comma.\n")
            out_file.write("- **Naming Conventions**:\n")
            out_file.write("  - Use `CamelCase` for class names.\n")
            out_file.write("  - Use `lower_case_with_underscores` for functions and variable names.\n")
            out_file.write("  - Use `UPPER_CASE_WITH_UNDERSCORES` for constants.\n")
            out_file.write("\n## 7. **Commenting**\n")
            out_file.write("\n- **Inline Comments**: Use comments to explain complex logic or important sections of code.\n")
            out_file.write("\n  ```python\n")
            out_file.write("  # This loop processes each file in the directory\n")
            out_file.write("  for file in files:\n")
            out_file.write("      ...\n")
            out_file.write("  ```\n")
            out_file.write("\n## 8. **Logging**\n")
            out_file.write("\n- **Setup Logging**: Configure logging to output to both the console and a log file in the `./logs` directory. The log file should be named according to the script name.\n")
            out_file.write("\n  ```python\n")
            out_file.write("  def setup_logging(script_name):\n")
            out_file.write("      \"\"\"Setup logging configuration.\"\"\"\n")
            out_file.write("      log_dir = './logs'\n")
            out_file.write("      os.makedirs(log_dir, exist_ok=True)\n")
            out_file.write("      log_file = os.path.join(log_dir, f'{script_name}.log')\n")
            out_file.write("\n      logging.basicConfig(level=logging.DEBUG,\n")
            out_file.write("                          format='%(asctime)s - %(levelname)s - %(message)s',\n")
            out_file.write("                          handlers=[\n")
            out_file.write("                              logging.FileHandler(log_file),\n")
            out_file.write("                              logging.StreamHandler()\n")
            out_file.write("                          ])\n")
            out_file.write("  ```\n")
            out_file.write("\n- **Logging Levels**: Use appropriate logging levels (`DEBUG`, `INFO`, `ERROR`) to provide detailed and useful log messages.\n")
            out_file.write("\n    ```python\n")
            out_file.write("    logging.debug(f\"Processing file: {file_path}\")\n")
            out_file.write("    logging.info(\"Operation completed successfully.\")\n")
            out_file.write("    logging.error(f\"Error processing file: {e}\")\n")
            out_file.write("    ```\n")
            out_file.write("\n## 9. **Error Handling**\n")
            out_file.write("\n- **Try-Except Blocks**: Use try-except blocks to handle potential errors gracefully.\n")
            out_file.write("\n    ```python\n")
            out_file.write("    try:\n")
            out_file.write("        # code that may raise an exception\n")
            out_file.write("    except Exception as e:\n")
            out_file.write("        logging.error(f\"An error occurred: {e}\")\n")
            out_file.write("    ```\n")
            out_file.write("\n- **Using Whole New Functions**: Implement whole new functions within try-except blocks to keep the code modular and maintainable.\n")
            out_file.write("\n## 10. **Testing and Debugging**\n")
            out_file.write("\n- **Unit Tests**: Write unit tests for your functions to ensure they work correctly.\n")
            out_file.write("\n  ```python\n")
            out_file.write("  import unittest\n")
            out_file.write("\n  class TestExampleFunction(unittest.TestCase):\n")
            out_file.write("      def test_example_function(self):\n")
            out_file.write("          self.assertEqual(example_function(param1, param2), expected_result)\n")
            out_file.write("\n  if __name__ == '__main__':\n")
            out_file.write("      unittest.main()\n")
            out_file.write("  ```\n")
            out_file.write("\n## 12. **PEP 8 Compliance**\n")
            out_file.write("\n- Summary of Key Points\n")
            out_file.write("  - **Indentation**: Use 4 spaces per indentation level.\n")
            out_file.write("  - **Line Length**: Limit all lines to a maximum of 79 characters.\n")
            out_file.write("  - **Blank Lines**: Use blank lines to separate top-level function and class definitions.\n")
            out_file.write("  - **Imports**:\n")
            out_file.write("    - Imports should usually be on separate lines.\n")
            out_file.write("    - Group imports in the following order: standard library imports, related third-party imports, local application/library-specific imports.\n")
            out_file.write("    - Use absolute imports when possible.\n")
            out_file.write("  - **String Quotes**: In general, use single quotes for short strings and double quotes for longer strings or when a string contains a single quote.\n")
            out_file.write("  - **Whitespace in Expressions and Statements**:\n")
            out_file.write("    - Avoid extraneous whitespace in the following situations: immediately inside parentheses, brackets or braces; immediately before a comma, semicolon, or colon; immediately before the open parenthesis that starts the argument list of a function call.\n")
            out_file.write("    - Use a single space around binary operators and after a comma.\n")
            out_file.write("  - **Naming Conventions**:\n")
            out_file.write("    - Use `CamelCase` for class names.\n")
            out_file.write("    - Use `lower_case_with_underscores` for functions and variable names.\n")
            out_file.write("    - Use `UPPER_CASE_WITH_UNDERSCORES` for constants.\n")
            out_file.write("\nRemember to follow the guidelines provided in the style guide to maintain consistency and readability in the code.\n")
                
        # Write the directory structure
        out_file.write("\nHere is the directory structure:\n")
        out_file.write('\n├── ./\n')
        directory_structure = generate_directory_structure(files)
        for line in directory_structure:
            out_file.write(line + '\n')
        out_file.write('\n')
        
        # Concatenate the contents of each file
        out_file.write("\nHere are the files:\n\n")
        for file in files:
            path = Path(file).resolve()
            try:
                relative_path = path.relative_to(Path('.').resolve())
            except ValueError:
                relative_path = path  # If the path is not relative, use the absolute path
            file_type = get_file_type(path)
            
            out_file.write(f'./{relative_path}\n\n')
            out_file.write(f'```{file_type}\n')
            
            try:
                with open(file, 'r') as f:
                    out_file.write(f.read())
            except Exception as e:
                logging.error(f"Error reading file {file}: {e}")
            
            out_file.write('\n```\n\n')


def split_into_chunks(file_path, chunk_size=CHUNK_SIZE):
    """
    Splits a file into smaller chunks.

    Parameters:
        file_path (str): The path to the file to split.
        chunk_size (int): The size of each chunk in characters.

    Returns:
        list of str: List of file paths of the chunks.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]
    chunk_files = []
    base_name = Path(file_path).stem
    ext = Path(file_path).suffix

    for i, chunk in enumerate(chunks):
        chunk_file_path = f"{base_name}_chunk_{i + 1}{ext}"
        with open(chunk_file_path, 'w') as chunk_file:
            chunk_file.write(chunk)
        chunk_files.append(chunk_file_path)

    return chunk_files

def split_into_chunks_with_messages(file_path, chunk_size=CHUNK_SIZE):
    """
    Splits a file into smaller chunks with whole lines and adds end-of-part messages.

    Parameters:
        file_path (str): The path to the file to split.
        chunk_size (int): The size of each chunk in characters.

    Returns:
        list of str: List of file paths of the chunks.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    lines = content.splitlines(keepends=True)
    chunks = []
    current_chunk = ''
    part_number = 1

    for line in lines:
        if len(current_chunk) + len(line) > chunk_size:
            # Add end-of-part message
            if part_number == len(chunks) + 1:  # For all parts except the last one
                current_chunk += f"\nEnd of part {part_number}. Please confirm receipt and let me know when you are ready for the next part.\n"
            chunks.append(current_chunk)
            current_chunk = ''
            part_number += 1
        current_chunk += line

    # Add the last chunk
    if current_chunk:
        current_chunk += f"\nEnd of part {part_number}. This is the final part. Please confirm receipt of all parts and proceed with the analysis only after receiving this message.\n"
        chunks.append(current_chunk)

    # Write chunks to files
    chunk_files = []
    base_name = Path(file_path).stem
    ext = Path(file_path).suffix

    for i, chunk in enumerate(chunks):
        chunk_file_path = f"{base_name}_chunk_{i + 1}{ext}"
        with open(chunk_file_path, 'w') as chunk_file:
            chunk_file.write(chunk)
        chunk_files.append(chunk_file_path)

    return chunk_files

def split_into_chunks_with_messages(file_path, chunk_size=CHUNK_SIZE):
    """
    Splits a file into smaller chunks with whole lines and adds end-of-part messages.

    Parameters:
        file_path (str): The path to the file to split.
        chunk_size (int): The size of each chunk in characters.

    Returns:
        list of str: List of file paths of the chunks.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    lines = content.splitlines(keepends=True)
    chunks = []
    current_chunk = ''
    part_number = 1

    for line in lines:
        if len(current_chunk) + len(line) > chunk_size:
            # Add end-of-part message
            if part_number == len(chunks) + 1:  # For all parts except the last one
                current_chunk += f"\nEnd of part {part_number}. Please confirm receipt and let me know when you are ready for the next part.\n"
            chunks.append(current_chunk)
            current_chunk = ''
            part_number += 1
        current_chunk += line

    # Add the last chunk
    if current_chunk:
        current_chunk += f"\nEnd of part {part_number}. This is the final part. Please confirm receipt of all parts and proceed with the analysis only after receiving this message.\n"
        chunks.append(current_chunk)

    # Write chunks to files
    chunk_files = []
    base_name = Path(file_path).stem
    ext = Path(file_path).suffix

    for i, chunk in enumerate(chunks):
        chunk_file_path = f"{base_name}_chunk_{i + 1}{ext}"
        with open(chunk_file_path, 'w') as chunk_file:
            chunk_file.write(chunk)
        chunk_files.append(chunk_file_path)

    return chunk_files


# Copy contents to clipboard
def copy_to_clipboard(content):
    """
    Copies the given content to the clipboard.

    Parameters:
        content (str): The content to copy to the clipboard.
    """
    system = platform.system()
    try:
        if system == 'Linux':
            subprocess.run(['xclip', '-selection', 'clipboard'], input=content.encode('utf-8'))
        elif system == 'Darwin':  # macOS
            subprocess.run(['pbcopy'], input=content.encode('utf-8'))
        elif system == 'Windows':
            subprocess.run(['clip'], input=content.encode('utf-8'))
        else:
            print(f"Clipboard copy not supported on {system}.")
            
        print("Contents copied to clipboard.")
    except Exception as e:
        logging.error(f"Error copying contents to clipboard: {e}")

# Add recursive option to glob
def collect_files(patterns, recursive=False):
    """
    Collects files matching the given patterns, optionally searching directories recursively.

    Parameters:
        patterns (list of str): List of file patterns to match.
        recursive (bool): Whether to search directories recursively.

    Returns:
        list of str: List of file paths matching the patterns.
    """
    files = []
    for pattern in patterns:
        if recursive:
            files.extend(glob.glob(pattern, recursive=True))
        else:
            files.extend(glob.glob(pattern))
    return files

def main():
    """
    Main function to parse arguments and execute file concatenation.
    """
    usage_example = """\
    Usage example:
        python quick-cat.py *.py *.js *.html -o my_files_combined.md --copy --recursive
    """
    description = "Concatenate files with directory structure and content.\n\n" + usage_example

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('patterns', nargs='+', help='List of file patterns to concatenate')
    parser.add_argument('-o', '--output', default='output.md', help='Output file name (default: output.md)')
    parser.add_argument('--skip-prompt', action='store_true', help='Skip adding the LLM prompt content at the beginning')
    parser.add_argument('--copy', action='store_true', help='Copy the output to the clipboard')
    parser.add_argument('--recursive', action='store_true', help='Recursively search directories for files matching the patterns')

    args = parser.parse_args()

    setup_logging('concatenate_files')
    
    files = collect_files(args.patterns, recursive=args.recursive)
    
    if not files:
        logging.error("No files found matching the given patterns.")
        return
    
    concatenate_files(files, args.output, skip_prompt=args.skip_prompt)
    logging.info("File concatenation completed successfully.")
    
    # Split the output file into chunks with messages
    chunk_files = split_into_chunks_with_messages(args.output)
    logging.info(f"Output file split into {len(chunk_files)} chunks.")

    # Ask the user if they want to copy the contents to the clipboard
    if args.copy or input("Do you want to copy the contents to the clipboard? ([y]es/no): ").strip().lower() in ['yes', 'y', '']:
        for chunk_file in chunk_files:
            with open(chunk_file, 'r') as f:
                chunk_content = f.read()
            copy_to_clipboard(chunk_content)
            input("Press Enter to copy the next chunk...")

if __name__ == '__main__':
    main()