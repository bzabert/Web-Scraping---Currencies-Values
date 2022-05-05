# Import the libraries
from bs4 import BeautifulSoup
import time
import requests
import csv
import datetime
import pandas as pd


# Obtain URL, headers and create the requets
def check_currencie():
    URL = "https://dolarhoy.com/cotizaciondolarblue"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }

    page = requests.get(URL, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    # Obtain the class of the currencies
    cotizacion = soup2.find_all(class_="tile is-child")

    # Create the header for the CSV file
    header = ["Currencie", "Buy", "Sell", "Date"]
    today = datetime.date.today()
    data = []

    # Obtain information
    for tag in cotizacion:
        try:
            titulo = tag.find(class_="title").get_text()
            titulo = titulo.strip()
            compra = tag.find(class_="compra").get_text()
            compra = float(compra.strip())
            venta = tag.find(class_="venta").get_text()
            venta = float(venta.strip())
            data.append([titulo, compra, venta, today])
        except:
            pass

    # Change the name of a currency
    data[0][0] = "Dolar Ofical"

    # Create the CSV file
    with open("CotizacionDataset.csv", "w", newline="", encoding="UTF8") as Dataset:
        writer = csv.writer(Dataset)
        writer.writerow(header)
        for cotizacion in data:
            writer.writerow(cotizacion)


# Data add every day
while True:
    check_currencie()
    time.sleep(86400)


# Create a DataFrame to see it in python
df = pd.read_csv("/Users/bzabert/Documents/Portfolio/CotizacionDataset.csv")
print(df)
