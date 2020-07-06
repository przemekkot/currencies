from flask import Flask, render_template, request, redirect

import json
import csv
import requests


app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()[0]['rates']

#print(data)

with open("currencies.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    headers = (k for k, v in data[0].items())
    writer.writerow(headers)
    for currency in data:
        row = currency.values()
        writer.writerow(row)

codes = []

for row in data:
    codes.append(row["code"])

#print(codes)

codes_currencies = {k: v for (k, v) in zip(codes, data)}

#print(codes_currencies)


@app.route('/', methods=['GET', 'POST'])
def calculate():
    if request.method == 'GET':
        print("We received GET")
        return render_template("index.html")
    elif request.method == 'POST':
        ask = codes_currencies[request.form["currency"]]["ask"]
        value = float(ask) * int(request.form["quantity"])
        print("We received POST")
        return render_template("result.html", result=value)
        


if __name__ == '__main__':
    app.run(debug=True)
