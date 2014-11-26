"""View handler.

.. module:: views

.. module authors:: Mattias Nasman, s132062
					Glebs Rjabovs, s107142
"""
from flask import render_template,request
#from django.shortcuts import render
from app import app
#from django.http import HttpResponseRedirect

@app.route('/', methods=['POST', 'GET'])
@app.route('/index')

def index():
    input_string = None
    if request.method == 'POST':
        input_string = request.form['input_string']
    return render_template("index.html", title='Home', input=input_string)