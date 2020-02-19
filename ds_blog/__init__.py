from flask import Flask

app = Flask(__name__)

from ds_blog import routes

