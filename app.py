import json
import csv
import requests

from flask import Flask, render_template, request, redirect

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()[0]['rates']

print(data)


with open("currencies.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    headers = (k for k, v in data[0].items())
    writer.writerow(headers)
    for currency in data:
        row = currency.values()
        writer.writerow(row)

@app.route('/index', methods=['GET', 'POST'])
def message():
   if request.method == 'GET':
        print("We received GET")
        return render_template("index.html")
    elif request.method == 'POST':
        print("We received POST")
        print(request.form)
        return render_template("result.html")


