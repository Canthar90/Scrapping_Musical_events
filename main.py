import requests
import selectorlib
import smtplib, ssl
import os
from dotenv import load_dotenv
import time
import sqlite3



load_dotenv("env.env")

USERNAME = os.getenv('EMAIL_USERNAME')
PASS = os.getenv("EMAIL_PASS")
HOST = "smtp.gmail.com"
PORT = 465 
reciver = USERNAME

URL = "http://programmer100.pythonanywhere.com/tours/"
ID = "displaytimer"


class Event:
    def scrape(self, url):
        """Scrape the page source form the URL"""
        response =  requests.get(url)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email():
    def __init__(self, password, email) -> None:
        self.username = email
        self.password = password
        pass
    
    def send(self, message):
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(HOST, PORT, context=context) as server:
            server.login(self.username, self.password)
            server.sendmail(self.username, reciver, message)
        print("Email was sent")



class Database:
    def __init__(self, database_path) -> None:
        self.connetcion =  sqlite3.connect(database_path)
        pass
    
    
    def store(self, extracted):
        row = extracted.split(',')
        row = [item.strip() for item in row]
        cursor = self.connetcion.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connetcion.commit()
            
            
    def read(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connetcion.cursor()

        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                    (band, city, date))
        rows = cursor.fetchall()
        print(rows)
        return rows


if __name__ == "__main__":
    event = Event()
    emailng = Email(password=PASS, email=USERNAME)
    data = Database(database_path="data.db")
    while True:
        time.sleep(5)
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)
        
    
        if extracted != "No upcoming tours":
            row = data.read(extracted)
            if not row:
                emailng.send(message =f"Hey new event was found! {extracted}")
                data.store(extracted)

