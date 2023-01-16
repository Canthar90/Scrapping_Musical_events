import requests
import selectorlib
import datetime as dt
import sqlite3
import time


connection = sqlite3.connect("data.db")
URL = "http://programmer100.pythonanywhere.com"


def requester(url):
    response = requests.get(url).text
    # response = response
    return response


def extracting(response):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(response)["temp"]
    return value


def saver(data):
    now = dt.datetime.now()
    timestamp = now.strftime("%y-%m-%d-%H-%M-%S")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO temperatures VALUES(?, ?)", (timestamp, data))
    connection.commit()
    print("saved")


if __name__ == "__main__":
    while True:
        time.sleep(5)
        response = requester(URL)
        scraped = extracting(response)
        print(scraped)
        saver(scraped)
    
    