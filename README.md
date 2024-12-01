# VK Subtitle Downloader and Cleaner

This Python script automates the process of extracting, downloading, and cleaning subtitles from VK video pages. It was created to simplify working with subtitles by removing unnecessary timestamps and blank lines for a compact and readable format.

## Features
- Automatically fetches subtitle URLs from VK video pages.
- Generates unique filenames for downloaded subtitles to prevent overwriting existing files.
- Cleans subtitles by removing timestamps and empty lines, leaving only meaningful text.

## Why I Created This
I developed this tool to help me with the Samsung innovation campus because i wanted to summraize the videos, save time when working with VK subtitles, making them more concise and easier to use. This is especially useful for language learning or content analysis, where cluttered subtitles can be distracting.

## How It Works
1. **Fetch the Subtitle URL**: The script uses Selenium to open the VK video page and find the subtitle URL.
2. **Download and Clean**: Subtitles are downloaded from the URL and cleaned of timestamps and unnecessary lines.
3. **Save Output**: Cleaned subtitles are saved in a uniquely named file (e.g., `subtitles.vtt1`, `subtitles.vtt2`, etc.).

## Usage
1. Install the dependencies:
   ```bash
   pip install selenium webdriver-manager requests
2. Run the script:
    python script.py
3. Enter the VK video URL when prompted.
4. Find the cleaned subtitle file in the script's directory.

## Screenshots
![alt text](image.png)

## Customization
    To keep timestamps in the output:
        Remove the following block in the clean_subtitles function:

            if not timestamp_pattern.match(line) and not line.startswith("<c>"):
    To allow blank lines:
        Remove or modify this section:
            stripped_line = line.strip()
            if stripped_line:
                cleaned_lines.append(stripped_line)
    To keep subtitles unaltered:
        Skip the clean_subtitles function in download_subtitles:
        cleaned_content = clean_subtitles(response.content)
    Replace with:
        cleaned_content = response.content

## License
This project is open-source. Feel free to modify and use it.

### 3. Explanation for Changes
- To **keep timestamps**, the `if` condition in `clean_subtitles` that filters out timestamp lines should be removed.
- To **allow blank lines**, the `stripped_line` logic can be bypassed.
- To **keep subtitles unaltered**, skip the `clean_subtitles` step entirely. This involves changing how `response.content` is handled in `download_subtitles`.
