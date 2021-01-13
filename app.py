from flask import Flask, render_template, redirect, request, url_for, session, flash
import yfinance as yf
import os
from flask_pymongo import PyMongo, pymongo
from secret import MONGO_URI
from os import path




app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MONGO_DBNAME'] = 'portfoliopal'
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)

@app.route('/')
def home():
    stocks = mongo.db.stocks.find()

    return render_template('dashboard.html', stocks=stocks)

@app.route('/add_symbol', methods=['GET', 'POST'])
def add_symbol():
    if request.method == 'GET':
        return render_template('add_symbol.html')

    elif request.method == 'POST':
        symbol = request.form['symbol']
        amount = request.form['amount']
        category = request.form['category']
        purchase_date = request.form['purchase_date']
        sell_date =
        
        new_doc = {
            'symbol': symbol,
            'amount': amount,
            'category': category,
            'purchase_date': purchase_date,
            'sell_date': sell_date,
            'price_history': []
        }
        mongo.db.stocks.insert_one(new_doc)
        return redirect(url_for('home'))

@app.route('/update-data')
def update_data():
    stocks = mongo.db.stocks.find()
    for stock in stocks:
        symbol = yf.Ticker(stock.symbol)
        if stock.sell_date
            data = symbol.history(start=stock.purchase_date, end=stock.sell_date)
            print(data)
        else:
            data = symbol.history(start=stock.purchase_date)
            print(data)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host=os.environ.get("IP", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")), 
        debug=True,)