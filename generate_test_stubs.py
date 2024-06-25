# generate_test_stubs.py

"""
This script generates unit test stubs for functions in a Flask application.
It scans through the .py files in the specified source directory, extracts function names,
and creates corresponding test stubs in the test directory.
"""

import os
import ast
import logging
import argparse
from pathlib import Path

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
    return log_file

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def extract_functions_from_file(file_path):
    """
    Extract function names from a Python file.

    Parameters:
        file_path (str): Path to the Python file.
    
    Returns:
        list: List of function names.
    """
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def generate_test_stub(function_name):
    """
    Generate a test stub for a given function name.

    Parameters:
        function_name (str): Name of the function to generate a test for.
    
    Returns:
        str: Test stub string.
    """
    return f'''
def test_{function_name}():
    \"\"\"
    Test {function_name} function.
    \"\"\"
    # TODO: Write test for {function_name}
    pass
'''

def save_to_file(output_lines, output_path):
    """
    Save the test stubs to a file.

    Parameters:
        output_lines (list): The lines of test stubs.
        output_path (str): The path where the test stubs will be saved.
    """
    # Ensure the directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(output_path, 'w') as f:
            for line in output_lines:
                f.write(line + '\n')
        logging.info(f"Output saved to {output_path}")
    except Exception as e:
        logging.error(f"Error writing to file: {e}")

def get_user_input(prompt_message, default_value):
    """Prompt the user for input, providing a default value."""
    return input(f"\033[32m{prompt_message} (default: {default_value}): \033[0m").strip() or default_value

def generate_section_separator(filename):
    """
    Generate a section separator for the given filename.

    Parameters:
        filename (str): The name of the file.
    
    Returns:
        str: The section separator string.
    """
    line_length = len(filename) + 6  # 2 spaces on each side plus # symbols
    separator = "#" * line_length
    return f"{separator}\n#  {filename}  #\n{separator}\n"

def log_processed_functions(log_file, processed_functions):
    """Log the processed functions to avoid duplicates."""
    try:
        with open(log_file, 'a') as log:
            for function in processed_functions:
                log.write(f"{function}\n")
    except Exception as e:
        logging.error(f"Error writing to log file: {e}")

def get_logged_functions(log_file):
    """Retrieve already logged functions to avoid duplicates."""
    logged_functions = set()
    if os.path.exists(log_file):
        with open(log_file, 'r') as log:
            logged_functions = set(log.read().splitlines())
    return logged_functions

def main():
    """Main function to generate test stubs."""
    parser = argparse.ArgumentParser(description="Generate test stubs for Flask app functions.")
    parser.add_argument("--source_dir", help="Path to the source directory containing the Flask app.")
    parser.add_argument("--test_dir", help="Path to the directory where test stubs will be saved.")
    args = parser.parse_args()

    if not args.source_dir:
        clear_screen()
        source_dir = get_user_input("Enter the path to the source directory containing the Flask app", os.getcwd())
    else:
        source_dir = os.path.expanduser(args.source_dir)

    if not args.test_dir:
        test_dir = get_user_input("Enter the path to the directory where test stubs will be saved", './tests')
    else:
        test_dir = os.path.expanduser(args.test_dir)

    combined_output = get_user_input("Do you want one large test file (yes/no)?", "yes").lower() == 'yes'

    script_name = os.path.basename(__file__)
    log_file = setup_logging(script_name)
    logged_functions = get_logged_functions(log_file)

    stubs_created = 0
    all_test_stubs = []

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                functions = extract_functions_from_file(file_path)
                
                new_functions = [func for func in functions if func not in logged_functions]

                if new_functions:
                    if combined_output:
                        all_test_stubs.append(generate_section_separator(file))
                        for function in new_functions:
                            all_test_stubs.append(generate_test_stub(function))
                            stubs_created += 1
                    else:
                        test_file_path = os.path.join(test_dir, f'test_{os.path.splitext(file)[0]}.py')
                        test_stubs = [f"# Auto-generated test stubs for {file}"]
                        for function in new_functions:
                            test_stubs.append(generate_test_stub(function))
                            stubs_created += 1
                        save_to_file(test_stubs, test_file_path)

                    log_processed_functions(log_file, new_functions)

    if combined_output:
        parent_dir_name = os.path.basename(os.path.normpath(source_dir))
        combined_test_file_name = f"{parent_dir_name}-combined-tests.py"
        combined_test_file_path = os.path.join(test_dir, combined_test_file_name)
        save_to_file(all_test_stubs, combined_test_file_path)

    print(f"\nGenerated {stubs_created} test stubs.")
    logging.info(f"Generated {stubs_created} test stubs.")

if __name__ == "__main__":
    main()

