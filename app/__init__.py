#!flask/bin/python
from flask import Flask
import chartkick
app = Flask(__name__,static_folder=chartkick.js(), static_url_path='')
from app import views
#app.jinja_env.add_extension("chartkick.ext.charts")
