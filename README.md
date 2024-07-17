# My Tools

This repository contains several simple Python tools designed for various tasks such as file manipulation, web scraping, data generation, and more.

## Tools Included

- **combine-txt-files.py**: Combines multiple text files into one.
- **concatenate-code.py**: Concatenates code files with user confirmation on directories and files.
- **dirfn2txt.py**: Lists all files and directories in a given directory and saves the structure to a file.
- **dl-transcripts.py**: Downloads transcripts from a list of URLs provided in a file.
- **environment.yml**: Specifies the environment configuration for the project, including dependencies like Python version and libraries.
- **fake_data_mysql_multiple_dbs.py**: Generates fake data for multiple MySQL databases and tables.
- **fetch-licenses.py**: Fetches license information for Python packages listed in `environment.yml` and `requirements.txt`.
- **find-imports.py**: Finds and lists import statements in Python files within a specified directory.
- **generate_test_stubs.py**: Generates unit test stubs for functions in a Flask application.
- **get-links.py**: Extracts hyperlinks from a given webpage URL.
- **quick-cat.py**: Concatenates multiple files into a markdown file, preserving the directory structure.
- **scrape-with-links.py**: Scrapes content from a list of URLs and saves the content to a specified directory.
- **scrape.py**: Scrapes content from a single URL and saves the content to a specified output file.
- **show_file_changes.py**: Displays all changes made to a specific file in a Git repository.
- **youtube-dl.py**: Downloads YouTube videos.

## Style Guide

Please refer to the [Style Guide](./STYLEGUIDE.md) for coding consistency.

## Usage Examples

### combine-txt-files.py

Combines multiple text files from a specified directory into a single output file.

Example Usage:

```bash
python combine-txt-files.py output_file.txt
```

### concatenate-code.py

Concatenates code files with user confirmation on directories and files.

Example Usage:

```bash
python concatenate-code.py
```

### dirfn2txt.py

Lists all files and directories in a given directory and saves the structure to a file.

Example Usage:

```bash
python dirfn2txt.py output_file.txt
```

### dl-transcripts.py

Downloads transcripts from a list of URLs provided in a file.

Example Usage:

```bash
python dl-transcripts.py url_file.txt output_dir
```

### fake_data_mysql_multiple_dbs.py

Generates fake data for multiple MySQL databases and tables.

Example Usage:

```bash
python fake_data_mysql_multiple_dbs.py
```

### fetch-licenses.py

Fetches license information for Python packages listed in `environment.yml` and `requirements.txt`.

Example Usage:

```bash
python fetch-licenses.py -d . -e environment.yml -r requirements.txt -o py_pkg_licenses.md
```

### find-imports.py

Finds and lists import statements in Python files within a specified directory.

Example Usage:

```bash
python find-imports.py
```

### generate_test_stubs.py

Generates unit test stubs for functions in a Flask application.

Example Usage:

```bash
python generate_test_stubs.py --source_dir src --test_dir tests
```

### get-links.py

Extracts hyperlinks from a given webpage URL.

Example Usage:

```bash
python get-links.py url
```

### quick-cat.py

Concatenates multiple files into a markdown file, preserving the directory structure.

Example Usage:

```bash
python quick-cat.py file1.py file2.js -o output.md --copy
```

### scrape-with-links.py

Scrapes content from a list of URLs and saves the content to a specified directory.

Example Usage:

```bash
python scrape-with-links.py url_file.txt output_dir
```

### scrape.py

Scrapes content from a single URL and saves the content to a specified output file.

Example Usage:

```bash
python scrape.py url
```

### show_file_changes.py

Displays all changes made to a specific file in a Git repository.

Example Usage:

```bash
python show_file_changes.py file_path
```

### youtube-dl.py

Downloads YouTube videos.

Example Usage:

```bash
python youtube-dl.py
```

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
