# dl-transcripts.py

# This script downloads transcripts from a given list of URLs.
# It prompts the user for the file containing the URLs,
# reads each URL, downloads the transcript, and saves it to the specified directory.

import os
import logging
import argparse
import requests

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

def download_transcript(url, save_dir):
    """
    Download a transcript from the given URL and save it to the specified directory.
    
    Parameters:
        url (str): The URL to download the transcript from.
        save_dir (str): The directory to save the downloaded transcript.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        transcript_name = os.path.basename(url).split('?')[0]
        save_path = os.path.join(save_dir, transcript_name)
        with open(save_path, 'w') as file:
            file.write(response.text)
        logging.info(f"Downloaded transcript: {save_path}")
    except requests.RequestException as e:
        logging.error(f"Error downloading {url}: {e}")

def main():
    script_name = os.path.basename(__file__).split('.')[0]
    setup_logging(script_name)
    clear_screen()

    parser = argparse.ArgumentParser(description="Download transcripts from a list of URLs.")
    parser.add_argument("url_file", nargs='?', help="The file containing the list of URLs.")
    parser.add_argument("output_dir", nargs='?', default='./output', help="The directory to save the downloaded transcripts (default: ./output).")
    args = parser.parse_args()

    if not args.url_file:
        print("\033[32mYou can pass the URL file as a command-line argument.\033[0m")
        url_file = input(f"\033[32mEnter the path to the file containing the URLs: \033[0m").strip()
    else:
        url_file = args.url_file

    if not os.path.exists(url_file):
        logging.error("The specified URL file does not exist.")
        return

    os.makedirs(args.output_dir, exist_ok=True)

    with open(url_file, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        if url:
            download_transcript(url, args.output_dir)

if __name__ == "__main__":
    main()