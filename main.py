from flask import Flask,request
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations, it's a web app!"

@app.route("/extract",methods = ["POST"])
def extractor():
    data = request.json
    abs1 =data["abstract"]
    keys =  requests.post("https://ankitgaur2811-confman-key.hf.space/run/predict", json={"data": [abs1]}).json()
    datak = keys["data"]
    data1=datak[0].split("[")[1]
    data1 = data1.split("]")[0]
    data1 =data1.split(",")
    datak = []
    for x in data1:
        datak.append(x.split("'")[1])
    finalkey = datak + data["tags"]
    allreviewer = requests.get("https://confman-api.onrender.com/reviewers/all")
    allreviewer1 = allreviewer["result"]
    reviewer = requests.post("http://ankitgaur2811.pythonanywhere.com/assignreviewer",data = {"allreviewer":allreviewer1,"allpaperkeywords":finalkey,"assignedreview":[]})
    return reviewer


if __name__ == "__main__":
    app.run(debug = False,host="0.0.0.0")
