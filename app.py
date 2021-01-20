from flask import Flask, render_template, redirect, request, url_for, session, flash
import yfinance as yf
import os
from flask_pymongo import PyMongo, pymongo
from secret import MONGO_URI
from os import path
from bson.objectid import ObjectId



app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MONGO_DBNAME'] = 'portfoliopal'
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)

@app.route('/')
def home():
    stocks = mongo.db.stocks.find()
    stonks = mongo.db.stocks.find()
    doughnutdata = [0, 0, 0, 0, 0, 0, 0]
    categories = ['Tech',
                    'Realestate',
                    'Materials',
                    'Crypto',
                    'Funds',
                    'Currency',
                    'Räksallad']  
    for stock in stonks:
        print(stock['category'])
        value = int(stock['price_history'][-1][-1] * float(stock['amount']))
        for i in range(0, len(categories)):
            if categories[i] == stock['category']:
                doughnutdata[i] += value
    print (doughnutdata)
        

    return render_template('dashboard.html', stocks=stocks, doughnutdata=doughnutdata)

@app.route('/add_symbol', methods=['GET', 'POST'])
def add_symbol():
    if request.method == 'GET':
        return render_template('add_symbol.html')

    elif request.method == 'POST':
        symbol = request.form['symbol']
        amount = request.form['amount']
        category = request.form['category']
        purchase_date = request.form['purchase_date']
        
        
        new_doc = {
            'symbol': symbol,
            'amount': amount,
            'category': category,
            'purchase_date': purchase_date,
            'price_history': []
        }
        mongo.db.stocks.insert_one(new_doc)
        return redirect(url_for('update_data'))

@app.route('/update-data')
def update_data():
    stocks = mongo.db.stocks.find()
    for stock in stocks:
        symbol = yf.Ticker(stock['symbol'])
        data = symbol.history(start=stock['purchase_date'])
        data_dict = data['Close'].to_dict()
        price_history = []
        for key, value in data_dict.items():
            price_history.append([key, value])
        print(stock)
        new_doc = {
            'symbol': stock['symbol'],
            'amount': stock['amount'],
            'category': stock['category'],
            'purchase_date': stock['purchase_date'],
            'price_history': price_history
        }
        mongo.db.stocks.replace_one({'_id':  ObjectId(stock['_id'])}, new_doc)

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host=os.environ.get("IP", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")), 
        debug=True,)