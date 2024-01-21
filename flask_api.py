from flask import Flask, jsonify, request 
import json
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests
import firebase_creds_render
from firebase_admin import db
from scrape import run

app = Flask(__name__) 

# on the terminal type: curl http://127.0.0.1:5000/ 
# returns hello world when we use GET. 
# returns the data that we send when we use POST. 
@app.route('/', methods = ['GET', 'POST']) 
def home(): 
	if(request.method == 'GET'): 

		data = "hello world"
		return jsonify({'data': data}) 



@app.route('/home', methods = ['GET']) 
def disp(): 
    print("running")
    run()
    return jsonify({'data': True}) 


# driver function 
if __name__ == '__main__': 

	app.run(debug = True) 
