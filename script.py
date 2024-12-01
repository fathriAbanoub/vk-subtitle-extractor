import os  # To handle file operations like checking if a file exists
import re  # For working with regular expressions to clean subtitle content
import time  # To add delays for the web page to load
import requests  # To handle HTTP requests for downloading subtitles
from selenium import webdriver  # To automate browser interaction
from selenium.webdriver.common.by import By  # To locate elements on the web page
from selenium.webdriver.chrome.service import Service  # To manage ChromeDriver service
from webdriver_manager.chrome import ChromeDriverManager  # To automatically download and manage ChromeDriver

def get_subtitle_url(video_url):
    """
    Use Selenium to fetch the subtitle URL from a VK video page.
    Args:
        video_url (str): The URL of the VK video.
    Returns:
        str: The URL of the subtitle file if found, else None.
    """
    # Set up the Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        # Open the video URL in the browser
        driver.get(video_url)
        time.sleep(10)  # Wait for the page to load (adjust as needed)

        # Find all <track> elements on the page (these often contain subtitles)
        subtitle_elements = driver.find_elements(By.TAG_NAME, 'track')
        for subtitle in subtitle_elements:
            # Check if the track is a subtitle
            if subtitle.get_attribute('kind') == 'subtitles':
                subtitle_url = subtitle.get_attribute('src')
                print(f"Subtitle URL found: {subtitle_url}")
                return subtitle_url

        print("No subtitles found.")
        return None
    except Exception as e:
        print(f"Error during Selenium process: {e}")
        return None
    finally:
        # Always close the browser
        driver.quit()


def generate_unique_filename(base_name="subtitles.vtt"):
    """
    Generate a unique filename by appending numbers to the base name.
    Args:
        base_name (str): The base name for the file (default is "subtitles.vtt").
    Returns:
        str: A unique file name.
    """
    counter = 1
    while True:
        file_name = f"{base_name}{counter}"
        if not os.path.exists(file_name):  # Check if the file already exists
            return file_name
        counter += 1


def clean_subtitles(content):
    """
    Remove timestamps and unnecessary blank lines to clean subtitle content.
    Args:
        content (bytes): Raw subtitle content in bytes.
    Returns:
        bytes: Cleaned subtitle content in bytes.
    """
    # Regex to match timestamp lines
    timestamp_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}$")

    # Decode content and split it into lines
    lines = content.decode('utf-8').splitlines()
    cleaned_lines = []

    for line in lines:
        # Skip lines with timestamps or starting with "<c>"
        if not timestamp_pattern.match(line) and not line.startswith("<c>"):
            stripped_line = line.strip()
            # Add non-empty lines to the cleaned list
            if stripped_line:
                cleaned_lines.append(stripped_line)

    # Join cleaned lines with a single newline
    return "\n".join(cleaned_lines).encode('utf-8')


def download_subtitles(subtitle_url, output_file):
    """
    Download subtitles from the URL and clean them.
    Args:
        subtitle_url (str): URL of the subtitle file.
        output_file (str): Path to save the cleaned subtitle file.
    """
    # Headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Referer": "https://vk.com",
        "Accept": "application/json",
    }

    response = requests.get(subtitle_url, headers=headers)
    if response.status_code == 200:
        # Clean the downloaded content
        cleaned_content = clean_subtitles(response.content)
        # Write the cleaned content to the output file
        with open(output_file, "wb") as f:
            f.write(cleaned_content)
        print(f"Subtitle file downloaded and cleaned: {output_file}")
    else:
        print(f"Failed to download subtitles. Status code: {response.status_code}")


if __name__ == "__main__":
    # Prompt the user for the VK video URL
    video_url = input("Enter the VK video URL: ")
    subtitle_url = get_subtitle_url(video_url)

    if subtitle_url:
        # Generate a unique file name and download the subtitles
        output_file = generate_unique_filename()
        download_subtitles(subtitle_url, output_file)
    else:
        print("Could not find a valid subtitle URL.")
