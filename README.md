# Forex Factory Web Scraper

## Description
This project is a web scraper for collecting economic event data from Forex Factory. The scraper uses Selenium to automate browsing and BeautifulSoup to parse the HTML content. The collected data is saved as JSON files in the specified folder.

## Features
- Scrapes historical economic events from Forex Factory.
- Saves events as JSON files with a standardized naming format (`EVENT_YYYY_MM_DD.json`).
- Automatically detects the last downloaded file to avoid duplicates.

## Requirements
- Python 3.8+
- Libraries:
```bash
pip install selenium beautifulsoup4 argparse
```
- WebDriver for your preferred browser (e.g., ChromeDriver for Google Chrome)

## Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd ExampleProject
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download and install the appropriate WebDriver (e.g., [ChromeDriver](https://chromedriver.chromium.org/downloads)). Ensure it is accessible in your system's PATH.

## Usage
```bash
python main.py <folder_path> <start_date> [end_date]
```

### Arguments
- `<folder_path>`: Path to the folder where event files will be stored.
- `<start_date>`: The start date for scraping (format: `YYYY-MM-DD`).
- `[end_date]` (optional): The end date for scraping (format: `YYYY-MM-DD`). Defaults to today if not provided.

### Example
```bash
python main.py "./data" "2025-01-01" "2025-01-10"
```

## How It Works
1. The script checks for the latest downloaded file in the specified folder.
2. It generates URLs for each date in the range.
3. Selenium loads each page, and BeautifulSoup parses the event data.
4. Parsed events are saved as JSON files.

## File Structure
```
ExampleProject/
│
├── html_things.py           # Contains helper functions for URL generation and HTML parsing
├── main.py                  # Main script for running the scraper
├── requirements.txt         # Python dependencies
└── data/                    # Folder where JSON files will be stored
```

## JSON File Format
The scraped data is saved as JSON with the following structure:
```json
[
    {
        "time": "8:30am",
        "currency": "USD",
        "impact": "High",
        "event": "Non-Farm Employment Change"
    },
    ...
]
```

## Troubleshooting
- **WebDriver not found:** Ensure `chromedriver` is in your PATH or provide the full path to the executable.
- **Invalid date format:** Dates must be in `YYYY-MM-DD` format.

## License
This project is licensed under the MIT License.

## Acknowledgments
- [Forex Factory](https://www.forexfactory.com/) for providing the economic calendar.
- [Selenium](https://selenium.dev/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping tools.

