from flask import Flask
import flask as fl

app = Flask(__name__)

@app.route('/')
def index():
	return fl.render_template('index.html')
