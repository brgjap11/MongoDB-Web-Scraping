from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars
#from config import dbuser, dbpasswd

app = Flask(__name__)

conn = conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars
collection = db.mars


@app.route('/')
def index():
	mars = collection.find_one()
	mars = scrape_mars.scrape()
	return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrape():
	mars = collection
	mars_data = scrape_mars.scrape()
	mars.update(
		{},
		mars_data,
		upsert=True
	)
	return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)
