import requests
import selectorlib


URL = "http://programmer100.pythonanywhere.com/tours/"
ID = "displaytimer"


def scrape(url):
    """Scrape the page source form the URL"""
    response =  requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email():
    print("Email was sent!")


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")
        
        
def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    content = read(extracted)
    
    if extracted != "No upcoming tours":
        if extracted not in content:
            send_email()
            store(extracted)
