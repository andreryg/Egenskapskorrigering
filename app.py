# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 09:01:47 2023

@author: andryg
"""

from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

"""@app.route('/send/<string:objekt>', methods=['POST'])
def send(objekt):
    objekt = str(object)
    print("aaaaaa", objekt)
    return redirect(url_for('view'))"""

@app.route('/', methods=['POST', 'GET'])
def getData():
    objekt = "objekt" + request.form['objekt']
    egenskaper = request.form.getlist(objekt)
    if request.method == "POST":
        return redirect(url_for('view'))
    
@app.route('/view')
def view():
    print(("dddddd"))
    return render_template('view.html')