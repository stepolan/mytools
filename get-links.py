# get-links.py

# This script extracts links from a given webpage URL.
# It prompts the user for the URL, retrieves the webpage,
# and extracts all hyperlinks, saving them to a specified output file.

import os
import logging
import argparse
import requests
from bs4 import BeautifulSoup

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

def extract_links(url):
    """
    Extract links from a given webpage URL.
    
    Parameters:
        url (str): The URL of the webpage to extract links from.
    
    Returns:
        list: A list of extracted hyperlinks.
    """
    try:
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        logging.info(f"Extracted {len(links)} links from {url}")
        return links
    except requests.RequestException as e:
        logging.error(f"Error retrieving {url}: {e}")
        return []

def sanitize_filename(filename):
    """
    Sanitize the filename to make it suitable for saving to the filesystem.
    
    Parameters:
        filename (str): The original filename.
    
    Returns:
        str: The sanitized filename.
    """
    return "".join(c if c.isalnum() or c in (' ', '.', '_') else '_' for c in filename)

def save_links_to_file(links, script_name, url):
    """
    Save extracted links to a file.
    
    Parameters:
        links (list): A list of hyperlinks.
        script_name (str): The name of the script.
        url (str): The URL the links were extracted from.
    """
    sanitized_url = sanitize_filename(url)
    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{script_name}-{sanitized_url}.txt')
    try:
        with open(output_file, 'w') as file:
            for link in links:
                file.write(link + '\n')
        logging.info(f"Links saved to {output_file}")
    except Exception as e:
        logging.error(f"Error writing to file: {e}")

def main():
    script_name = os.path.basename(__file__).split('.')[0]
    setup_logging(script_name)
    clear_screen()

    parser = argparse.ArgumentParser(description="Extract links from a given webpage URL.")
    parser.add_argument("url", nargs='?', help="The URL of the webpage to extract links from.")
    args = parser.parse_args()

    if not args.url:
        print("\033[32mYou can pass the URL as a command-line argument.\033[0m")
        url = input(f"\033[32mEnter the URL of the webpage to extract links from: \033[0m").strip()
    else:
        url = args.url

    links = extract_links(url)
    if links:
        save_links_to_file(links, script_name, url)

if __name__ == "__main__":
    main()