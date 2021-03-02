
import requests
import time
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.mars_collection


@app.route("/")
def index ():

    mars_db = mongo.db.mars_db.find_one()
    return render_template("index.html", scrapeoutput=mars_db)


@app.route("/scrape")
def scrape():
    mars_db = mongo.db.mars_db
    scrape_data = scrape_mars.scrape()
    mars_db.update({}, scrape_data, upsert=True)
    return redirect("/", code= 302)

client.close()

if __name__ == "__main__":
    app.run(debug=True)
