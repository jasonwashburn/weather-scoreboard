from typing import Union

import pandas as pd
import pendulum
from bs4 import BeautifulSoup
from pendulum.datetime import DateTime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

WOWT_URL = "https://www.wowt.com/weather"


def create_datetime_from_row_data(
    time_date_str: str, year: int, timezone_str: str = " America/Chicago"
) -> DateTime:
    date_string = str(year) + " " + time_date_str + timezone_str
    return pendulum.from_format(date_string, "YYYY H AM/DD z").in_timezone("UTC")


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)

    return driver


def parse_page_source(page_source) -> list[dict[str, Union[str, int]]]:
    soup = BeautifulSoup(page_source, "html.parser")

    hourly_row_divs = soup.find_all(name="div", attrs="hour")

    current_time = pendulum.now().in_timezone("UTC")
    hourly_data = []

    for row in hourly_row_divs:
        row_data = [child.text for child in row]
        time_and_date_str = row_data[0]
        forecast = {}
        forecast["recorded_time"] = current_time.strftime("%Y-%m-%d %H:%M:%S %z")
        forecast["valid_time"] = create_datetime_from_row_data(
            time_date_str=time_and_date_str, year=current_time.year
        ).strftime("%Y-%m-%d %H:%M:%S %z")

        forecast["temperature"] = int(row_data[1].rstrip("°"))
        forecast["precip_chance"] = int(row_data[3].rstrip("%"))
        forecast["dewpoint_temperature"] = int(row_data[4].rstrip("°"))
        wind_direction, wind_speed, _ = row_data[5].split(" ")
        forecast["wind_direction"] = wind_direction
        forecast["wind_speed"] = wind_speed

        hourly_data.append(forecast)

    return hourly_data


def main():
    with get_driver() as driver:
        driver.get(WOWT_URL)
        page_source = driver.page_source

    hourly_data = parse_page_source(page_source=page_source)

    df = pd.DataFrame.from_dict(hourly_data)
    df["valid_time"] = pd.to_datetime(df["valid_time"])
    df["recorded_time"] = pd.to_datetime(df["recorded_time"])
    print(df)
    records = df.to_json(orient="records")
    print("----")
    print(records)


if __name__ == "__main__":
    main()
