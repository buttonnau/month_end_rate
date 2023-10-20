from flask import Flask, render_template, request
import requests
import datetime
import time
import sqlite3

app = Flask (__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
def buy():
    return render_template("buy.html")

@app.route("/buy", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("buy.html")
    else:
         # Ensure coin_fullname was submitted
        if not request.form.get("coin_fullname"):
            return render_template("buy.html")
        # Ensure start_date was submitted
        if not request.form.get("start_date"):
            return render_template("buy.html")
        # Ensure end_date was submitted
        if not request.form.get("end_date"):
            return render_template("buy.html")
        stringArray = request.form.get("coin_fullname").split("\n");
        stringArray = [s.replace("\r", "") for s in stringArray];

        # get start_date
        form_start_date = request.form.get('start_date') # in format 2012-10-25 or in Python String formatting %Y-%m-%d

        # get end_date
        form_end_date = request.form.get('end_date') # in format 24 hour, eg 1:30PM = 13:30

        # create Python date from form_date and form_time. We use the python datetime string formmatting to describe how the date is built YYYY-MM-DD HH:MM

        start_year=int(form_start_date[:4])
        start_month=int(form_start_date[5:7])
        start_day=int(form_start_date[8:10])
        hour=00
        min=00
        end_year=int(form_end_date[:4])
        end_month=int(form_end_date[5:7])
        end_day=int(form_end_date[8:10])

        start_d = datetime.datetime(start_year,start_month,start_day,hour,min)
        start_date = str(int(time.mktime(start_d.timetuple())))

        end_d = datetime.datetime(end_year,end_month,end_day,hour,min)
        end_date = str(int(time.mktime(end_d.timetuple())))



        hashs = []

        for j in stringArray:
            url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert=USD&slug=" + j + "&time_end=" + end_date + "&time_start=" + start_date
            #url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert=USD&slug=bitcoin&time_end=1606262400&time_start=1603324800"
            response = requests.get(url)
            stock = response.json()
            hash = stock["data"]
            hashs.append(hash)



        #db.execute("INSERT INTO hello (address, currency, balance) VALUES (:address, :currency, :balance)", address=stock["address"], currency="ETH", balance=stock["ETH"]["balance"])

        #for i in stock["tokens"]:
        #    db.execute("INSERT INTO hello (address, currency, balance) VALUES (:address, :currency, :balance)", address=stock["address"], currency=i["tokenInfo"]['symbol'], balance=i['balance']/1000000000000000000)

        #old = db.execute("SELECT * FROM hello")

        return render_template("index.html", hashs=hashs)