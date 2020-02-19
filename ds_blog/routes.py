from flask import render_template, url_for
from ds_blog import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')
