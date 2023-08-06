# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 09:01:47 2023

@author: andryg
"""

from flask import Flask, render_template, request, redirect, url_for, session
import nvdbapiv3
import pandas as pd
from flask_session import Session
import json
#from createJSON import createEgenskapJSON
from whitenoise import WhiteNoise
        
app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
    nvdbObjekter = [37, 46, 103] #ADD NVDB ID
    print('egenskap:'+request.form['filter'])
    objekter = nvdbapiv3.nvdbFagdata((nvdbObjekter[int(request.form['objekt'])]))
    
    if request.form['kommune'] != "":
        objekter.filter({'kommune':int(request.form['kommune'])})
    elif request.form['fylke'] != "0":
        objekter.filter({'fylke':int(request.form['fylke'])})
    if request.form['vegkategori'] != "0":
        objekter.filter({'vegsystemreferanse':request.form['vegkategori']+request.form['vegnummer']})
    if request.form['filter'] != "":
        objekter.filter({'egenskap':request.form['filter']})
    objekterDF = pd.DataFrame(objekter.to_records()).sort_values(by=['vref']).reset_index(drop=True)
    print(objekterDF['vegkategori'].head())
    #objekterDF = objekterDF.assign(geometri = lambda x: str(x['geometri']).strip("POINTZ()")[3:].split(" "))
    print(objekterDF.columns.values.tolist())
    objekter_array = objekterDF[['nvdbId', 'versjon', 'startdato', 'geometri']].to_numpy()
    
    for x in objekter_array:
        x[-1] = x[-1].strip("POINTZ()")[3:].split(" ")[0:2]
    print(objekter_array[0])
    objekt = "objekt" + request.form['objekt']
    egenskaper = [request.form['objekt']]
    egenskaper += request.form.getlist(objekt)
    session["egenskaper"] = egenskaper
    session["objekter"] = objekter_array
    if request.method == "POST":
        return redirect(url_for('view'))
    
@app.route('/view')
def view():
    objekter = session["objekter"]
    egenskaper = session["egenskaper"]
    
    return render_template('view.html', objekter=json.dumps({'list':objekter.tolist()}), egenskaper=egenskaper)

@app.route('/view', methods=['POST', 'GET'])
def createJSONs():
    session.clear()
    print("inside function")
    data = eval(request.form["JSvar"])
    print(data)
    egenskaperIds = data.pop(0)
    print(data)
    jsons = []
    """for i in data:
        jsons.append(createEgenskapJSON(i, egenskaperIds))"""
    json_dict = {
        "delviskorriger": {
            "vegobjekter": jsons
        },
        "datakatalogversjon": "2.33"
    }
    fil = open("kanalisering.json", "w")
    fil.write(json.dumps(json_dict, indent=4))
    fil.close()

    return redirect('/')
"""
if __name__=="__main__":
    app.run(debug=True)
"""