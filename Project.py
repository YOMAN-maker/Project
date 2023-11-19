import pandas as pd
import requests
from bs4 import BeautifulSoup
from alpha_vantage.timeseries import TimeSeries

url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
response = requests.get(url)
soup = BeautifulSoup(response.text,"html.parser")
table = soup.find('table',{"class":"wikitable"})
rows = table.find_all('tr')[1:]
print(rows)
stocks = []
for row in rows:
  cols = row.findAll(['td','th'])
  stock = cols[2].text.strip()
  stocks.append(stock)

portolio = {}
print("Available Stocks: ")
for index,stock in enumerate(stocks):
  print(f"{stock}", end="\t")
  if index%5==4:
    print()
print()

while True:
  symbol = input(f"Please select your desired stock symbol (q to quit): ")
  if symbol.lower() == "q":
    break
  quantity = int(input(f"Please enter the number of {symbol} stocks in your portfolio: "))
  portolio[symbol] = quantity

print("\nYour portolio: ")
for symbol,quantity in portolio.items():
  print(f'{symbol}: {quantity}')

start_date = "2020-01-01"
end_date = "2023-01-01"
API_KEY = "0A29SXY10C7S3RXJ"

ts = TimeSeries(key=API_KEY,output_format='pandas')
totalSum = 0

for symbol,quantity in portolio.items():
  data, meta_data = ts.get_daily(symbol=symbol,outputsize='full')
  data = data[(data.index >= start_date) & (data.index <= end_date)]
  data['return'] = (data['4. close'] - data['1. open'])*quantity
  totalSum += data["return"].sum()
  print(f'{quantity} {symbol} stock daily return:\nMean: {data["return"].mean() :.3f}\nSTD: {data["return"].std() :.3f}\nSUM: {data["return"].sum() :.3f}\n')
  del data
print(f'Total return in the given interval is {totalSum :.3f}')

