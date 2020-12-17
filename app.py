from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Initialize flask app and connect to MongoDB database mars_db
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'
mongo = PyMongo(app)

@app.route('/')
def index():
    # Pull out the first listing that is stored in the database
    mars_data = mongo.db.data.find_one()
    # Render html page using Mars data that was scraped
    return render_template('index.html', mars_data=mars_data)

# This route scrapes webpages for data and then stores it in MongoDB
@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape()
    # Puts this data into the Mars data collection as the only object
    mongo.db.data.update({}, mars_data, upsert=True)
    # Redirect back to main page
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)