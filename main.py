from flask import Flask,request
import requests
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations, it's a web app!"

@app.route("/extract",methods = ["POST"])
def extractor():
    data = request.json
    abs1 =data["abstract"]
    keys =  requests.post("https://ankitgaur2811-confman-key.hf.space/run/predict", json={"data": [abs1]}).json()
    datak = keys["data"][0]
    text1 = datak.split("[")[1].split("]")[0]
    text2 = text1.split(",")
    i=[]
    for x in text2:
        i.append(x.split("'")[1])
    finalkey = i + data["tags"]
    allreviewer = requests.get("https://confman-api.onrender.com/reviewers/all")
    allreviewer1 = allreviewer.json()
    allreviewer2 = jsonify(allreviewer1)
    allrev = allreviewer2.json
    request1 = {"allreviewer":allrev["result"],"allpaperkeywords":finalkey,"assignedreview":[]}
    print(request1)
    payload = json.dumps(request1)
    url = "http://ankitgaur2811.pythonanywhere.com/assignreviewer"
    headers = {
  'Content-Type': 'application/json'
}
    reviewer = requests.request("POST", url, headers=headers, data=payload)
    # print("=========================================================")
    # if reviewer.status_code != 200:
    #     print(reviewer.status_code)
    # else:
    #     try:
    #         data = reviewer.json()
    #         print(data)
    #     except ValueError:
    #         print(reviewer.text)
    return reviewer.text


if __name__ == "__main__":
    app.run(debug = False,host="0.0.0.0")
