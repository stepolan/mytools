import os
import argparse
import logging
from pathlib import Path

# concatenate_files.py

"""
This script concatenates multiple files, adds a directory structure, and formats the content for markdown.

It takes multiple file paths as arguments, generates a directory structure, and writes the content to an output file
with appropriate formatting.
"""

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
        '.php': 'php'
    }
    return file_types.get(ext, '')

def concatenate_files(files, output_file):
    """
    Concatenates the content of multiple files, adds directory structure and file type annotations.

    Parameters:
        files (list of str): List of file paths to concatenate.
        output_file (str): The name of the output file.
    """
    with open(output_file, 'w') as out_file:
        # Write the directory structure
        out_file.write('├── ./\n')
        directory_structure = generate_directory_structure(files)
        for line in directory_structure:
            out_file.write(line + '\n')
        out_file.write('\n')
        
        # Concatenate the contents of each file
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

def main():
    """
    Main function to parse arguments and execute file concatenation.
    """
    parser = argparse.ArgumentParser(description="Concatenate files with directory structure and content.")
    parser.add_argument('files', nargs='+', help='List of files to concatenate')
    parser.add_argument('-o', '--output', default='output.md', help='Output file name (default: output.md)')
    
    args = parser.parse_args()
    
    setup_logging('concatenate_files')
    
    concatenate_files(args.files, args.output)
    logging.info("File concatenation completed successfully.")

if __name__ == '__main__':
    main()
