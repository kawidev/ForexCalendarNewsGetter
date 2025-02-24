import argparse
import datetime
import os
import json
import time
from selenium import webdriver
from html_things import get_url, find_latest_downloaded_file, parse_events_from_html

def main(folder_path:str, start_date_arg: str, end_date_arg = None):
    """
    Main function to run the forex scraper.

    Args:
        start_date (str): The start date in the format YYYY-MM-DD.
        folder_path (str): The path to the folder where event files will be stored.
    """

    try:
        start_date = datetime.datetime.strptime(start_date_arg, "%Y-%m-%d").date()

        if end_date_arg is None:
            end_date = datetime.date.today()
        else:
            end_date = datetime.datetime.strptime(end_date_arg, "%Y-%m-%d").date()

        print(f"Start date: {start_date}")
        print(f"Folder path: {folder_path}")

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except ValueError as e:
        print(f"Invalid start date format: {start_date}")
        return
    
    

    existed_date = find_latest_downloaded_file(folder_path)

    if existed_date is not None:
        current_date = existed_date + datetime.timedelta(days=1)
    else:
        current_date = start_date

    while current_date <= end_date:

        _url = get_url(current_date)

        file_name = f"EVENT_{current_date.strftime('%Y_%m_%d')}.json"
        file_path = os.path.join(folder_path, file_name)

        if not os.path.exists(file_path):
            driver = webdriver.Chrome()
            driver.get(_url)
            time.sleep(3)
            page_source = driver.page_source

            driver.quit()

            events = parse_events_from_html(page_source)
            with open(file_path, "w") as file:
                json.dump(events, file, indent=2)
        else:
            print(f"File for {current_date} already exists.")

        current_date += datetime.timedelta(days=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Forex Factory Web Scraper")
    
    # Positional arguments (no 'required=True' needed)
    parser.add_argument("folder_path", type=str, help="The path to the folder where event files will be stored.")
    parser.add_argument("start_date", type=str, help="The start date in the format YYYY-MM-DD.")
    
    # Optional argument for end date
    parser.add_argument("end_date", type=str, nargs="?", help="The end date in the format YYYY-MM-DD.")
    
    args = parser.parse_args()

    main(args.folder_path, args.start_date, args.end_date)