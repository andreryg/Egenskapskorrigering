# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 09:01:47 2023

@author: andryg
"""

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/view/')
def view():
    return render_template('view.html')
    