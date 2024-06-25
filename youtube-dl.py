# youtube_downloader.py

"""
This script downloads YouTube videos.
It prompts the user for the YouTube video URL and the directory to save the video,
and then downloads the video using the highest resolution available.
"""

import os
import logging
from pytube import YouTube

def setup_logging(script_name):
    """
    Setup logging configuration.

    Parameters:
        script_name (str): Name of the script for log file naming.
    """
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

def download_video(url, path):
    """
    Download the YouTube video from the provided URL.

    Parameters:
        url (str): The URL of the YouTube video.
        path (str): The directory path to save the downloaded video.
    """
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=path)
        logging.info(f"Downloaded: {yt.title}")
    except Exception as e:
        logging.error(f"Error: {e}")

def main():
    """
    Main function to execute the script.
    Prompts the user for the YouTube video URL and the save directory,
    then downloads the video.
    """
    clear_screen()
    url = input("Enter the YouTube video URL: ")
    path = input("Enter the directory to save the video (default: ./output): ").strip() or './output'
    os.makedirs(path, exist_ok=True)
    download_video(url, path)

if __name__ == "__main__":
    setup_logging('youtube_downloader')
    main()
