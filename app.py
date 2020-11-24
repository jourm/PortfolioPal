from flask import Flask, render_template, redirect, request, url_for, session, flash
import yfinance as yf
import os
from flask_pymongo import PyMongo, pymongo
from secret import MONGO_URI
from os import path


stocks = [
    ["MSFT", 10, 175],
    ["TSLA", 2, 475],
    ]




app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MONGO_DBNAME'] = 'portfoliopal'
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)

@app.route('/')
def home():
    for i in range(0, len(stocks)):
        stock = yf.Ticker(stocks[i][0])
        price = stock.info['regularMarketPrice']
        stocks[i].append(price)

    return render_template('dashboard.html', stocks=stocks)

@app.route('/add_symbol', methods=['GET', 'POST'])
def add_symbol():
    if request.method == 'GET':
        return render_template('add_symbol.html')

    elif request.method == 'POST':
        symbol = request.form['symbol']
        amount = request.form['amount']
        purchase_date = request.form['purchase_date']

if __name__ == '__main__':
    app.run(host=os.environ.get("IP", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")), 
        debug=True,)