# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 09:01:47 2023

@author: andryg
"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import nvdbapiv3
import pandas as pd
import numpy as np
import json
import time
try: 
    from createJSON import createEgenskapJSON
except ImportError:
    pass
        
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
print(1)
app.config["SESSION_TYPE"] = "filesystem"
print(2)
app.config["SECRET_KEY"] = "topSecret"
print(3)
app.secret_key = "AlsoTopSecret"
print(4)
Session(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def getData():
    nvdbObjekter = [37, 46, 103] #ADD NVDB ID
    objekter = nvdbapiv3.nvdbFagdata((nvdbObjekter[int(request.form['objekt'])]))
    try:
        if request.form['kommune'] != "":
            objekter.filter({'kommune':int(request.form['kommune'])})
        elif request.form['fylke'] != "0":
            objekter.filter({'fylke':int(request.form['fylke'])})
        if request.form['vegkategori'] != "0":
            objekter.filter({'vegsystemreferanse':request.form['vegkategori']+request.form['vegnummer']})
        if request.form['filter'] != "":
            objekter.filter({'egenskap':request.form['filter']})
        objekterDF = pd.DataFrame(objekter.to_records()).sort_values(by=['vref']).reset_index(drop=True)
    except:
        return redirect('/')
        
    objekter_array = objekterDF[['nvdbId', 'versjon', 'startdato', 'geometri']].to_numpy()
    for x in objekter_array:
        x[-1] = x[-1].strip("POINTZ()")[3:].split(" ")[0:2]
        
    session["obj"] = objekter_array
    
    objekt = "objekt" + request.form['objekt']
    egenskaper = [request.form['objekt']]
    egenskaper += request.form.getlist(objekt)
    session["egenskaper"] = egenskaper
    time.sleep(10)
    
    if request.method == "POST":
        print("obj" in session)
        return redirect(url_for('view'))
    
@app.route('/view')
def view():
    objekter_array = session.get("obj")
    egenskaper = session.get("egenskaper")
    if objekter_array.any():
        return render_template('view.html', objekter=json.dumps({'list':objekter_array.tolist()}), egenskaper=egenskaper)
    else:
        redirect('/')

@app.route('/view', methods=['POST', 'GET'])
def createJSONs():
    data = eval(request.form["JSvar"])
    egenskaperIds = data.pop(0)
    jsons = []
    for i in data:
        jsons.append(createEgenskapJSON(i, egenskaperIds))
    json_dict = {
        "delvisKorriger": {
            "vegobjekter": jsons
        },
        "datakatalogversjon": "2.33"
    }
    
    return redirect(url_for('.flash', message=json_dict))

@app.route('/flash')
def flash():
    message = json.dumps(request.args.get("message"), indent=4)
    return render_template('flash.html', message=message)

if __name__=="__main__":
    app.run(debug=True)
