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
    python quick-cat.py "*.py" "./source/*.py" "/static/js/*.js" "/templates/*.html" -o combined_output.md --copy

    This command concatenates all .py files, .js files in /static/js, and .html files in /templates into a 
    markdown file named combined_output.md, including a directory structure and syntax highlighting for each 
    file's content. The --copy flag copies the output to the clipboard.

Arguments:
    patterns (list of str): List of file patterns to concatenate.
    -o, --output (str): Output file name (default: output.md).
    -sp, --skip-prompt (bool): Skip adding the additional prompt content at the beginning.
    -pf, --prompt-file (str): Path to a file containing the prompt content to include at the beginning.
    -c, --copy (bool): Copy the output to the clipboard.
    -r, --recursive (bool): Recursively search directories for files matching the patterns.
    -ex, --exclude (list of str): Patterns of files to exclude.
    -cs, --chunk-size (int): Chunk size for splitting the output file (default: 150000).
    -d, --delete-chunks (bool): Delete chunk files after copying to clipboard.

Output:
    The script produces a markdown file with the following features:
    - A visual representation of the directory structure of the input files.
    - Concatenated contents of each file, with appropriate markdown syntax highlighting based on file type.
    - Optionally splits the output into chunks with end-of-part messages and continuation notices.
    - Optionally copies the output or chunks to the clipboard.
    - Optionally deletes the chunk files after copying to clipboard.
"""

import os
import argparse
import logging
import platform
import subprocess
from pathlib import Path
import glob

# Constants
CHUNK_SIZE = 100000

FILE_TYPE_LANGUAGES = {
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
    '.tsx': 'tsx',
    '.feature': 'cucumber',
    '.abap': 'abap',
    '.adb': 'ada',
    '.ads': 'ada',
    '.ada': 'ada',
    '.ahk': 'ahk',
    '.ahkl': 'ahk',
    '.htaccess': 'apacheconf',
    'apache.conf': 'apacheconf',
    'apache2.conf': 'apacheconf',
    '.applescript': 'applescript',
    '.as': 'as',
    '.as3': 'as3',
    '.asy': 'asy',
    '.ksh': 'bash',
    '.bash': 'bash',
    '.ebuild': 'bash',
    '.eclass': 'bash',
    '.bat': 'bat',
    '.cmd': 'bat',
    '.befunge': 'befunge',
    '.bmx': 'blitzmax',
    '.boo': 'boo',
    '.bf': 'brainfuck',
    '.b': 'brainfuck',
    '.c': 'c',
    '.h': 'c',
    '.cfm': 'cfm',
    '.cfml': 'cfm',
    '.cfc': 'cfm',
    '.tmpl': 'cheetah',
    '.spt': 'cheetah',
    '.cl': 'cl',
    '.lisp': 'cl',
    '.el': 'cl',
    '.clj': 'clojure',
    '.cljs': 'clojure',
    '.cmake': 'cmake',
    'CMakeLists.txt': 'cmake',
    '.coffee': 'coffeescript',
    '.sh-session': 'console',
    'control': 'control',
    '.cpp': 'cpp',
    '.hpp': 'cpp',
    '.c++': 'cpp',
    '.h++': 'cpp',
    '.cc': 'cpp',
    '.hh': 'cpp',
    '.cxx': 'cpp',
    '.hxx': 'cpp',
    '.pde': 'cpp',
    '.cs': 'csharp',
    '.css': 'css',
    '.pyx': 'cython',
    '.pxd': 'cython',
    '.pxi': 'cython',
    '.d': 'd',
    '.di': 'd',
    '.pas': 'delphi',
    '.diff': 'diff',
    '.patch': 'diff',
    '.dpatch': 'dpatch',
    '.darcspatch': 'dpatch',
    '.duel': 'duel',
    '.jbst': 'duel',
    '.dylan': 'dylan',
    '.dyl': 'dylan',
    '.erb': 'erb',
    '.erl-sh': 'erl',
    '.erl': 'erlang',
    '.hrl': 'erlang',
    '.evoque': 'evoque',
    '.factor': 'factor',
    '.flx': 'felix',
    '.flxh': 'felix',
    '.f': 'fortran',
    '.f90': 'fortran',
    '.s': 'gas',
    '.S': 'gas',
    '.kid': 'genshi',
    '.gitignore': 'gitignore',
    '.vert': 'glsl',
    '.frag': 'glsl',
    '.geo': 'glsl',
    '.plot': 'gnuplot',
    '.plt': 'gnuplot',
    '.go': 'go',
    '.man': 'groff',
    '.1': 'groff',
    '.2': 'groff',
    '.3': 'groff',
    '.4': 'groff',
    '.5': 'groff',
    '.6': 'groff',
    '.7': 'groff',
    '.8': 'groff',
    '.9': 'groff',
    '.haml': 'haml',
    '.hs': 'haskell',
    '.htm': 'html',
    '.xhtml': 'html',
    '.xslt': 'html',
    '.hx': 'hx',
    '.hy': 'hybris',
    '.hyb': 'hybris',
    '.cfg': 'ini',
    '.io': 'io',
    '.ik': 'ioke',
    '.weechatlog': 'irc',
    '.jade': 'jade',
    '.java': 'java',
    '.jsp': 'jsp',
    '.lhs': 'lhs',
    '.ll': 'llvm',
    '.lgt': 'logtalk',
    '.lua': 'lua',
    '.wlua': 'lua',
    '.mak': 'make',
    'Makefile': 'make',
    'makefile': 'make',
    'Makefile.': 'make',
    'GNUmakefile': 'make',
    '.mao': 'mako',
    '.maql': 'maql',
    '.mhtml': 'mason',
    '.mc': 'mason',
    '.mi': 'mason',
    'autohandler': 'mason',
    'dhandler': 'mason',
    '.md': 'markdown',
    '.mo': 'modelica',
    '.def': 'modula2',
    '.mod': 'modula2',
    '.moo': 'moocode',
    '.mu': 'mupad',
    '.mxml': 'mxml',
    '.myt': 'myghty',
    'autodelegate': 'myghty',
    '.asm': 'nasm',
    '.ASM': 'nasm',
    '.ns2': 'newspeak',
    '.objdump': 'objdump',
    '.m': 'objectivec',
    '.j': 'objectivej',
    '.ml': 'ocaml',
    '.mli': 'ocaml',
    '.mll': 'ocaml',
    '.mly': 'ocaml',
    '.ooc': 'ooc',
    '.pl': 'perl',
    '.pm': 'perl',
    '.php': 'php',
    '.php(345)': 'php',
    '.ps': 'postscript',
    '.eps': 'postscript',
    '.pot': 'pot',
    '.po': 'pot',
    '.pov': 'pov',
    '.inc': 'pov',
    '.prolog': 'prolog',
    '.pro': 'prolog',
    '.pl': 'prolog',
    '.properties': 'properties',
    '.proto': 'protobuf',
    '.py3tb': 'py3tb',
    '.pytb': 'pytb',
    '.sc': 'python',
    '.tac': 'python',
    '.r': 'r',
    '.rb': 'rb',
    '.rbw': 'rb',
    '.rake': 'rb',
    '.gemspec': 'rb',
    '.rbx': 'rb',
    '.duby': 'rb',
    '.Rout': 'rconsole',
    '.r': 'rebol',
    '.r3': 'rebol',
    '.cw': 'redcode',
    '.rhtml': 'rhtml',
    '.rst': 'rst',
    '.sass': 'sass',
    '.scala': 'scala',
    '.scaml': 'scaml',
    '.scm': 'scheme',
    '.scss': 'scss',
    '.st': 'smalltalk',
    '.tpl': 'smarty',
    'sources.list': 'sourceslist',
    '.S': 'splus',
    '.R': 'splus',
    '.sql': 'sql',
    '.sqlite3-console': 'sqlite3',
    'squid.conf': 'squidconf',
    '.ssp': 'ssp',
    '.tcl': 'tcl',
    '.tcsh': 'tcsh',
    '.csh': 'tcsh',
    '.tex': 'tex',
    '.txt': 'text',
    '.v': 'v',
    '.vala': 'vala',
    '.vapi': 'vala',
    '.vb': 'vbnet',
    '.bas': 'vbnet',
    '.vm': 'velocity',
    '.fhtml': 'velocity',
    '.vim': 'vim',
    '.vimrc': 'vim',
    '.xqy': 'xquery',
    '.xquery': 'xquery'
}

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
            relative_path = path
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
    # Extract the file extension
    ext = Path(file).suffix.lower()
    # Return the language if it's in the dictionary, else default to 'text'
    return FILE_TYPE_LANGUAGES.get(ext, 'text')

def concatenate_files(files, output_file, skip_prompt=False, prompt_file=None):
    """
    Concatenates the content of multiple files, adds directory structure and file type annotations.

    Parameters:
        files (list of str): List of file paths to concatenate.
        output_file (str): The name of the output file.
        skip_prompt (bool): Whether to skip adding the additional prompt content at the beginning.
        prompt_file (str): Path to a file containing the prompt content to include at the beginning.
    """
    with open(output_file, 'w') as out_file:
        if prompt_file:
            try:
                with open(prompt_file, 'r') as pf:
                    prompt_content = pf.read()
                out_file.write(prompt_content + '\n\n')
            except Exception as e:
                logging.error(f"Error reading prompt file {prompt_file}: {e}")
        elif not skip_prompt:
            # Write the LLM prompt
            out_file.write("You are a super helpful coding assistant!\n\n")
            out_file.write("Instructions:\n\nBelow you will find relevant files for a project I am working on. Please analyze these different files and confirm that you understand their purpose. I will provide multiple files, and I will let you know when the final file is provided. Do not offer updates or show me code at this time. If you do not understand something, please ask me questions for clarification.\n\n")
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
            out_file.write("\nINSTRUCTION I am senging multiple parts, please confirm receipt of the files and let me know when you are ready for the next part.  Do not do anything else until you have all the parts.\n\n")
                
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
                current_chunk += f"\nEnd of part {part_number}. Please confirm receipt.\n"
                chunks.append(current_chunk)
                current_chunk = ''
                part_number += 1
        current_chunk += line

    if current_chunk:  # Add the last chunk
        current_chunk += f"\nEnd of part {part_number}. Please confirm receipt.\n"
        chunks.append(current_chunk)

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

from pathlib import Path

from pathlib import Path

def split_into_chunks_with_messages(file_path, chunk_size):
    """
    Splits a file into smaller chunks with whole lines and handles code boxes properly,
    adding end-of-part messages and continuation notices.

    Parameters:
        file_path (str): The path to the file to split.
        chunk_size (int): The size of each chunk in characters.

    Returns:
        list of str: List of file paths of the chunks.
    """
    def count_chunks(file_path, chunk_size):
        with open(file_path, 'r') as f:
            content = f.read()

        lines = content.splitlines(keepends=True)
        current_chunk = ''
        chunk_count = 0
        in_code_box = False

        for line in lines:
            if line.startswith('```') and not in_code_box:
                in_code_box = True
            elif line.startswith('```') and in_code_box:
                in_code_box = False

            if len(current_chunk) + len(line) > chunk_size:
                chunk_count += 1
                current_chunk = ''  # Reset for new chunk

            current_chunk += line

        if len(current_chunk) > 0:
            chunk_count += 1  # For the last chunk

        return chunk_count

    total_chunks = count_chunks(file_path, chunk_size)

    def add_end_of_part_message(chunk, part_number, total_chunks, current_file_name, in_code_box):
        if in_code_box:
            chunk += '```\n'
        chunk += f"\n{current_file_name} continued in next file\n"
        chunk += f"\nEnd of part {part_number} of {total_chunks}. Please confirm receipt and let me know when you are ready for the next part.\n"
        return chunk

    def add_start_of_part_message(current_chunk, part_number, current_file_name, in_code_box):
        """
        Adds a start-of-part message to the current chunk with appropriate code box formatting.

        Parameters:
            current_chunk (str): The current chunk of text.
            part_number (int): The part number for the chunk.
            current_file_name (str): The name of the current file.
            in_code_box (bool): Whether the chunk is within a code box.

        Returns:
            str: The updated chunk with the start-of-part message.
        """
        current_chunk += f"\nBeginning of part {part_number}\n\n"
        current_chunk += f"{current_file_name} (continued)\n\n"
        if in_code_box:
            # Use the get_file_type function to determine the code box language
            file_type = get_file_type(current_file_name)
            current_chunk += f'```{file_type}\n'
        return current_chunk

    with open(file_path, 'r') as f:
        content = f.read()

    lines = content.splitlines(keepends=True)
    chunks = []
    current_chunk = ''
    part_number = 1
    in_code_box = False
    current_file_name = ""

    for line in lines:
        if line.startswith('```') and not in_code_box:
            in_code_box = True
        elif line.startswith('```') and in_code_box:
            in_code_box = False

        if len(current_chunk) + len(line) > chunk_size:
            current_chunk = add_end_of_part_message(current_chunk, part_number, total_chunks, current_file_name, in_code_box)
            chunks.append(current_chunk)
            part_number += 1
            current_chunk = add_start_of_part_message('', part_number, current_file_name, in_code_box)

        current_chunk += line

        # Track the current file name for continuation messages
        if line.startswith('./') and not in_code_box:
            current_file_name = line.strip()

    if current_chunk:
        if in_code_box:
            current_chunk += '```\n'
        current_chunk += f"\nEnd of part {part_number} of {total_chunks}. This is the final part. Please confirm receipt of all parts and proceed with the analysis only after receiving this message.\n"
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
def collect_files(patterns, exclude_patterns=None, recursive=False):
    """
    Collects files matching the given patterns, optionally searching directories recursively.
    Excludes files matching the given exclusion patterns.

    Parameters:
        patterns (list of str): List of file patterns to match.
        exclude_patterns (list of str): List of file patterns to exclude.
        recursive (bool): Whether to search directories recursively.

    Returns:
        list of str: List of file paths matching the patterns.
    """
    if exclude_patterns is None:
        exclude_patterns = []

    all_files = []
    for pattern in patterns:
        if recursive:
            all_files.extend(glob.glob(f'**/{pattern}', recursive=True))
        else:
            all_files.extend(glob.glob(pattern))

    excluded_files = set()
    for pattern in exclude_patterns:
        if recursive:
            excluded_files.update(glob.glob(f'**/{pattern}', recursive=True))
        else:
            excluded_files.update(glob.glob(pattern))

    # Exclude directories and their contents
    excluded_dirs = {Path(p).resolve() for p in exclude_patterns if Path(p).is_dir()}
    result_files = []
    for file in all_files:
        file_path = Path(file).resolve()
        if file_path not in excluded_files and not any(file_path.is_relative_to(d) for d in excluded_dirs):
            result_files.append(file)
    
    return result_files

def main():
    """
    Main function to parse arguments and execute file concatenation.
    """
    usage_example = """\
    Usage example:
        python quick-cat.py "*.py" "*.js" "*.html" -o my_files_combined.md --copy --recursive --skip-prompt --exclude "bootstrap*.*" "./migrations/" "./tools/" "./docker/" --chunk-size 150000 --prompt-file prompt.txt
    """
    description = "Concatenate files with directory structure and content.\n\n" + usage_example

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('patterns', nargs='+', help='List of file patterns to concatenate, put in quotes (ex: "*.py" "*.js" "*.html")')
    parser.add_argument('-o', '--output', default='output.md', help='Output file name (default: output.md)')
    parser.add_argument('-sp', '--skip-prompt', action='store_true', help='Skip adding the LLM prompt content at the beginning')
    parser.add_argument('-pf', '--prompt-file', type=str, help='Path to a file containing the prompt content to include at the beginning')
    parser.add_argument('-c', '--copy', action='store_true', help='Copy the output to the clipboard')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursively search directories for files matching the patterns')
    parser.add_argument('-ex', '--exclude', nargs='+', help='Patterns of files to exclude')
    parser.add_argument('-cs', '--chunk-size', type=int, default=CHUNK_SIZE, help=f'Chunk size for splitting the output file (default: {CHUNK_SIZE})')
    parser.add_argument('-d', '--delete-chunks', action='store_true', help='Delete chunk files after copying to clipboard')

    args = parser.parse_args()

    setup_logging('concatenate_files')
    
    files = collect_files(args.patterns, exclude_patterns=args.exclude, recursive=args.recursive)
    
    if not files:
        logging.error("No files found matching the given patterns.")
        return
    
    concatenate_files(files, args.output, skip_prompt=args.skip_prompt, prompt_file=args.prompt_file)
    logging.info("File concatenation completed successfully.")
    
    # Split the output file into chunks with messages
    chunk_files = split_into_chunks_with_messages(args.output, chunk_size=args.chunk_size)
    logging.info(f"Output file split into {len(chunk_files)} chunks.")

    # Ask the user if they want to copy the contents to the clipboard
    if args.copy or input("Do you want to copy the contents to the clipboard? ([y]es/no): ").strip().lower() in ['yes', 'y', '']:
        for i, chunk_file in enumerate(chunk_files):
            with open(chunk_file, 'r') as f:
                chunk_content = f.read()
            copy_to_clipboard(chunk_content)
            print(f"Chunk {i + 1} of {len(chunk_files)} copied to clipboard.")
            if i < len(chunk_files) - 1:
                input(f"Press Enter to copy chunk {i + 2} of {len(chunk_files)}...")
            else:
                print("All chunks have been copied.")

        if args.delete_chunks or input("Do you want to delete all the chunk files? ([y]es/no): ").strip().lower() in ['yes', 'y', '']:
            for chunk_file in chunk_files:
                try:
                    os.remove(chunk_file)
                    print(f"Deleted {chunk_file}")
                except Exception as e:
                    print(f"Error deleting {chunk_file}: {e}")

if __name__ == '__main__':
    main()