import requests
import selectorlib
import smtplib, ssl
import os
from dotenv import load_dotenv
import time


load_dotenv("env.env")

USERNAME = os.getenv('EMAIL_USERNAME')
PASS = os.getenv("EMAIL_PASS")
HOST = "smtp.gmail.com"
PORT = 465 
reciver = USERNAME

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


def send_email(message):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(HOST, PORT, context=context) as server:
        server.login(USERNAME, PASS)
        server.sendmail(USERNAME, reciver, message)



def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")
        
        
def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    while True:
        time.sleep(75)
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        content = read(extracted)
    
        if extracted != "No upcoming tours":
            if extracted not in content:
                send_email(message =f"Hey new event was found! {extracted}")
                store(extracted)

