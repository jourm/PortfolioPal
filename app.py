from flask import Flask, render_template, redirect, request, url_for, session, flash
import yfinance as yf
import os
from os import path

stocks = [
    ["MSFT", 10, 175],
    ["TSLA", 2, 475],
    ]




app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def home():
    for i in range(0, len(stocks)):
        stock = yf.Ticker(stocks[i][0])
        price = stock.info['regularMarketPrice']
        stocks[i].append(price)

    return render_template('dashboard.html', stocks=stocks)


if __name__ == '__main__':
    app.run(host=os.environ.get("IP", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")), 
        debug=True,)