import requests
import selectorlib
import smtplib, ssl
import os
from dotenv import load_dotenv
import time
import sqlite3


"INSERT INTO events VALUES ('Tigers', 'Tiger City', '2088.10.14')"
"SELECT*FROM events WHERE date='2088.10.14'"
'DELETE FROM events WHERE band="Tigers"'

connetcion =  sqlite3.connect("data.db")

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
    print("Email was sent")



def store(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    cursor = connetcion.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connetcion.commit()
        
        
def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connetcion.cursor()

    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows

if __name__ == "__main__":
    while True:
        time.sleep(5)
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        
    
        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                send_email(message =f"Hey new event was found! {extracted}")
                store(extracted)

