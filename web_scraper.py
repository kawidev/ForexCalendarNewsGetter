"""


Documentation


"""

import datetime
import json
import os
import re
import time

from selenium import webdriver
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