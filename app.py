
import requests
import time
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

conn = "mongodb://localhost:27017/scrape_db"
client = pymongo.MongoClient(conn)

db = client.mars_data_db
mars = db.mars

@app.route("/")
def index ():
    search_result = mars.find_one()
    return render_template("index.html",search_result=search_result)


@app.route("/scrape")
def scrape_mars():
    collection = mars
    scrape_results = scrape
    collection.update({}, scrape_results, insert=True)
    return redirect("/", code= 302)

client.close()

if __name__ == "__main__":
    app.run(debug=True)
