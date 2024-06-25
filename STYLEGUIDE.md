# Style Guide for Writing Tools

## 1. **Code Formatting**

- **Script Name Comment**: Include the name of the script at the top as a comment. This helps identify the log and output files.

    ```python
    # script_name.py
    ```

- **Consistent Indentation**: Use 4 spaces for indentation.
- **Function Definitions**: Clearly defined functions with specific purposes.
- **Modular Code**: Break down tasks into small, reusable functions.
- **Docstrings**: Use docstrings for all functions to explain their purpose, parameters, and return values.

## 2. **Commenting**

- **Function Docstrings**: Provide a clear explanation of the function's purpose, parameters, and return values.

  ```python
  def example_function(param1, param2):
      """
      Brief description of the function.

      Parameters:
          param1 (type): Description of param1.
          param2 (type): Description of param2.
      
      Returns:
          return_type: Description of the return value.
      """
  ```

- **Inline Comments**: Use comments to explain complex logic or important sections of code.

    ```python
    # This loop processes each file in the directory
    for file in files:
    ...
    ```

## 3. **Prompts and Clear Screens**

- **User Interaction**: Provide clear, concise prompts for user input.

  ```python
  startpath = input(f"\033[32mEnter the directory path to list (default: {os.getcwd()}, e.g., ~/dev/): \033[0m").strip() or os.getcwd()
  ```

- **Clear Screens**: Clear the terminal screen to improve readability before displaying new information.

  ```python
  def clear_screen():
      """Clear the terminal screen."""
      os.system('cls' if os.name == 'nt' else 'clear')
  ```

## 4. **Logging**

- **Setup Logging**: Configure logging to output to both the console and a log file in the `./logs` directory. The log file should be named according to the script name.

  ```python
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
  ```

- **Logging Levels**: Use appropriate logging levels (`DEBUG`, `INFO`, `ERROR`) to provide detailed and useful log messages.

  ```python
  logging.debug(f"Processing file: {file_path}")
  logging.info("Operation completed successfully.")
  logging.error(f"Error processing file: {e}")
  ```

## 5. **Output**

- **Formatted Output**: Use clear and well-formatted output to display information to the user.

  ```python
  print("\033[34mDirectory structure:\033[0m\n")
  for line in output_lines:
      print(line)
  ```

- **Save to File**: Ensure output is saved to a file in the `./output` directory, creating directories as needed. Name the output file based on the script and function names.

  ```python
  def save_to_file(output_lines, script_name, function_name):
      """
      Save the directory structure to a file.

      Parameters:
          output_lines (list): The lines of directory structure.
          script_name (str): The name of the script.
          function_name (str): The name of the function generating the output.
      """
      output_dir = './output'
      os.makedirs(output_dir, exist_ok=True)
      output_file = os.path.join(output_dir, f'{script_name}.{function_name}.txt')
      
      try:
          with open(output_file, 'w') as f:
              for line in output_lines:
                  f.write(line + '\n')
          logging.info(f"Output saved to {output_file}")
      except Exception as e:
          logging.error(f"Error writing to file: {e}")
  ```

## 6. **Error Handling**

- **Try-Except Blocks**: Use try-except blocks to handle potential errors gracefully.

  ```python
  try:
      # code that may raise an exception
  except Exception as e:
      logging.error(f"An error occurred: {e}")
  ```

## 7. **Configuration Management**

- **Configuration Files**: Use configuration files for storing settings that might change frequently. This can help make your scripts more flexible and easier to manage.

  ```python
  import json

  def load_config(config_file):
      """Load configuration settings from a file."""
      with open(config_file, 'r') as f:
          config = json.load(f)
      return config
  ```

## 8. **Command-Line Arguments**

- **Argument Parsing**: Use argparse for handling command-line arguments to make your scripts more versatile.

  ```python
  parser = argparse.ArgumentParser(description="Script description")
  parser.add_argument("--config", help="Path to configuration file", default="config.json")
  args = parser.parse_args()
  config = load_config(args.config)
  ```

## 9. **Testing and Debugging**

- **Unit Tests**: Write unit tests for your functions to ensure they work correctly.

  ```python
  import unittest

  class TestExampleFunction(unittest.TestCase):
      def test_example_function(self):
          self.assertEqual(example_function(param1, param2), expected_result)

  if **name** == '**main**':
      unittest.main()
  ```

## 10. **Script Summary**

- **Summary Comment**: Include a brief summary of the script's purpose and functionality in comments at the top, after the filename and a line break.

  ```python
  # script_name.py

  # This script combines multiple text files into a single text file.
  # It prompts the user for the directory containing the text files,
  # reads each file, and writes their contents into an output file.
  ```
  