from crawling import fetch_and_store_multiple_periods, crawl_gold_price_blogs

if __name__ == "__main__":
    period_list = [
        "DAY_1",
        "WEEK_1",
        "MONTH_1",
        "YTD",
        "YEAR_1",
        "YEAR_3",
        "MAX",
        "CUSTOM",
    ]
    fetch_and_store_multiple_periods(period_list, "26-05-2023", "26-05-2024")
    crawl_gold_price_blogs("https://www.bullionstar.com/charts/gold-price-today")
