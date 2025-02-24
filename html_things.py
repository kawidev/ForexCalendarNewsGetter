

import datetime
import json
import os
import re

from bs4 import BeautifulSoup


def get_url(date: datetime.date) -> str:
    """
    Formats a date into the URL format used by ForexFactory and returns the corresponding link.

    Args:
        date (datetime.date): The date to format (e.g., datetime.date(2025, 1, 1)).

    Returns:
        str: The URL in the format "https://www.forexfactory.com/calendar?day=jan1.2025".

    Example:
        >>> get_url(datetime.date(2025, 1, 1))
        'https://www.forexfactory.com/calendar?day=jan1.2025'
    """

    formatted_month = date.strftime("%b").lower()
    formatted_date = f"{formatted_month}{date.day}.{date.year}"

    return f"https://www.forexfactory.com/calendar?day={formatted_date}"


def find_latest_downloaded_file(folder: str) -> datetime.date:
    """
    Get the latest downloaded file in the folder according to the date modified.
    This method prevents downloading the same file multiple times.
    
    Args: 
        folder (str): The folder path where the files are downloaded.
    
    Returns:
        datetime.date: The latest date as a datetime.date object (e.g., datetime.date(2025, 1, 1)).
    """
    pattern = re.compile(r"^EVENT_(\d{4})_(\d{2})_(\d{2})\.json$")

    latest_date = None

    for file in os.listdir(folder):
        match = pattern.match(file)
        if match:
            year, month, day = match.groups()
            date = datetime.date(int(year), int(month), int(day))

            if latest_date is None or date > latest_date:
                latest_date = date
    
    return latest_date

def parse_events_from_html(html):
    """
    Parse the events from the HTML page and return them as a list of dictionaries.

    Args:
        html (str): The HTML content of the page.

    Returns:
        list[dict]: A list of dictionaries containing the event details.
    """
    soup = BeautifulSoup(html, "html.parser")
    events = []
    previous_time = None  # To keep track of the last known time
    rows = soup.find_all("tr", {"data-event-id": True})
    
    impact_dict = {
        "icon--ff-impact-red": "High",
        "icon--ff-impact-ora": "Medium",
        "icon--ff-impact-yel": "Low",
    }

    for row in rows:
        time_td = row.find("td", class_="calendar__time")
        currency_td = row.find("td", class_="calendar__currency")
        impact_td = row.find("td", class_="calendar__impact")
        event_td = row.find("td", class_="calendar__event")

        event_time = time_td.get_text(strip=True) if time_td else None

        # If the time is missing, it means it's the same as the previous event
        if not event_time:
            event_time = previous_time
        else:
            previous_time = event_time

        currency = currency_td.get_text(strip=True) if currency_td else None

        impact = None

        if impact_td:
            span = impact_td.find("span")
            if span:
                classes = span.get("class", [])

                for cls in classes:
                    if cls in impact_dict:
                        impact = impact_dict[cls]
                        break
        event_name = None

        if event_td:
            title_span = event_td.find("span", class_="calendar__event-title")

        if title_span:
            event_name = title_span.get_text(strip=True)

        events.append({
            "time": event_time,
            "currency": currency,
            "impact": impact,
            "event": event_name

        })


    return events