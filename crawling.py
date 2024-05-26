import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from urllib.parse import urlencode

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from constants import GOLD_PRICE_API_HEADERS, GOLD_PRICE_API_URL


def format_custom_time_period(start_date_str: str, end_date_str: str):
    """
    Format the custom time period for URL parameters.

    Args:
        start_date_str (str): Start date string in 'dd-mm-yyyy' format.
        end_date_str (str): End date string in 'dd-mm-yyyy' format.

    Returns:
        str: URL-encoded time range parameters.

    Raises:
        ValueError: If the start date is not earlier than the end date.
    """
    start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
    end_date = datetime.strptime(end_date_str, "%d-%m-%Y")

    if start_date >= end_date:
        raise ValueError("Start date must be earlier than end date")

    start_date_formatted = start_date.strftime("%d-%m-%Y 00:00")
    end_date_formatted = end_date.strftime("%d-%m-%Y 23:59")

    params = {
        "fromDateString": start_date_formatted,
        "toDateString": end_date_formatted,
    }
    encoded_period = urlencode(params)

    return encoded_period


def crawl_gold_prices(
    currency: str,
    period: str,
    time_range: str = "",
):
    """
    Crawl gold prices data from the API.

    Args:
        currency (str): The currency type (e.g., 'USD', 'BTC').
        period (str): The period for which to fetch data (e.g., "DAY_1", "WEEK_1").
        time_range (str, optional): URL-encoded time range parameters for custom periods.

    Returns:
        dict: The JSON response from the API.
    """
    url = GOLD_PRICE_API_URL.format(
        currency=currency, period=period, time_range=time_range
    )
    response = requests.get(url, headers=GOLD_PRICE_API_HEADERS)
    return response.json()


def convert_to_dataframe(
    crawled_gold_prices: list[dict], value_column_name: str, start_date: int
):
    """
    Convert crawled gold prices data to a pandas DataFrame.

    Args:
        crawled_gold_prices (list[dict]): List of dictionaries containing the crawled data.
        value_column_name (str): The name of the column for the values (e.g., 'Cost (USD)').
        start_date (int): The start date in epoch milliseconds for the timestamp conversion.

    Returns:
        pd.DataFrame: DataFrame with the converted data.
    """
    dataframe = pd.DataFrame(crawled_gold_prices)
    dataframe.rename(columns={"d": "Date", "v": value_column_name}, inplace=True)
    dataframe["Date"] = pd.to_datetime(
        dataframe["Date"] * 100000 + start_date, unit="ms"
    )
    return dataframe


def store_gold_prices(
    usd_dataframe: pd.DataFrame,
    bitcoin_dataframe: pd.DataFrame,
    period: str,
):
    """
    Store the gold prices data in a CSV file.

    Args:
        usd_dataframe (pd.DataFrame): DataFrame containing USD gold prices.
        bitcoin_dataframe (pd.DataFrame): DataFrame containing Bitcoin gold prices.
        period (str): The period for which the data was fetched (e.g., "DAY_1", "WEEK_1").

    Saves:
        CSV file: The merged DataFrame saved as a CSV file named '{period}.csv'.
    """
    merged_dataframe = pd.merge(
        usd_dataframe, bitcoin_dataframe, on="Date", how="outer"
    )
    merged_dataframe.to_csv(f"data/{period}.csv", index=False)


def fetch_and_store_gold_prices(
    period: str, start_date: str = None, end_date: str = None
):
    """
    Fetch and store gold prices data for a specific period.

    Args:
        period (str): The period for which to fetch data (e.g., "DAY_1", "WEEK_1", 'CUSTOM').
        start_date (str, optional): Start date string for custom periods.
        end_date (str, optional): End date string for custom periods.

    Raises:
        ValueError: If the start date and end date are not provided for custom periods.
    """
    time_range = ""
    if period == "CUSTOM":
        if start_date is None or end_date is None:
            raise ValueError("Start date and end date must be provided")
        time_range = format_custom_time_period(start_date, end_date)

    gold_prices = crawl_gold_prices("USD", period, time_range)
    time_series = gold_prices["dataSeries"]
    start_datetime = gold_prices["startDate"]
    usd_data = convert_to_dataframe(time_series, "Cost (USD)", start_datetime)

    gold_prices = crawl_gold_prices("BTC", period, time_range)
    time_series = gold_prices["dataSeries"]
    start_datetime = gold_prices["startDate"]
    bitcoin_data = convert_to_dataframe(time_series, "Cost (Bitcoin)", start_datetime)

    store_gold_prices(usd_data, bitcoin_data, period)


def fetch_and_store_multiple_periods(
    periods: list[str], start_date: str, end_date: str
):
    """
    Fetch and store gold prices data for multiple periods concurrently.

    Args:
        periods (list[str]): List of periods for which to fetch data (e.g., ["DAY_1", "WEEK_1", 'CUSTOM']).
        start_date (str): Start date string for custom periods.
        end_date (str): End date string for custom periods.

    Raises:
        ValueError: If the start date and end date are not provided for custom periods.

    Prints:
        Success or failure message for each period after fetching and storing the data.
    """
    with ThreadPoolExecutor(max_workers=len(periods)) as executor:
        futures = {
            executor.submit(
                fetch_and_store_gold_prices, period, start_date, end_date
            ): period
            for period in periods
        }
        for future in as_completed(futures):
            period = futures[future]
            try:
                future.result()
                print(f"Successfully fetched and stored data for period: {period}")
            except Exception as exception:
                print(
                    f"Failed to fetch and store data for period: {period} due to {exception}"
                )


def crawl_gold_price_blogs(url: str):
    """
    Crawl and save gold price blog content from the specified URL.

    Args:
        url (str): The URL of the blog page to crawl.

    This function uses Selenium WebDriver to navigate to the provided URL, extract
    the content of the blog, format it, and save it into a text file named
    'gold_price_blogs.txt'. The titles (h2 elements) and paragraphs (p elements)
    are separated by specific formatting rules.
    """
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    blogs_container = driver.find_element(By.CLASS_NAME, "bottom-content")
    children = blogs_container.find_elements(By.XPATH, ".//h2 | .//p")

    content = []

    for child in children:
        if child.tag_name == "h2":
            content.append("\n" + child.text.strip() + "\n")
        elif child.tag_name == "p":
            content.append(child.text.strip() + "\n")

    driver.quit()

    with open("data/gold_price_blogs.txt", "w", encoding="utf-8") as file:
        file.writelines(content)
