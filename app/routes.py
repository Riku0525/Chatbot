from flask import redirect, url_for, request
from app import app

@app.route('/')
def index():
	return redirect(url_for('main.index'))