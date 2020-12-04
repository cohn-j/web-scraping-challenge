from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from flask_table import Table, Col
import scrape_mars

app = Flask(__name__)

# Or set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route("/")
def index():
    mars_gather = mongo.db.mars.find_one()

    return render_template("index.html", mars=mars_gather)


@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)