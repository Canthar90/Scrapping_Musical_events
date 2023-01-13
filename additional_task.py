import requests
import selectorlib
import datetime as dt


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
    content = f"\n{timestamp},{data}"
    with open("temperatures.txt", "a") as file:
        file.write(content)
    print("saved")


if __name__ == "__main__":
    response = requester(URL)
    scraped = extracting(response)
    saver(scraped)
    
    