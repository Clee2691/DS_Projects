from flask import Flask
from config import Config

ds_blog_inst = Flask(__name__)
ds_blog_inst.config.from_object(Config) # Get config information from the Config class


from ds_blog import routes