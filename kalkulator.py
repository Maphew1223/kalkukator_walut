import requests
from flask import Flask, render_template, request
import csv
import os
script_dir = os.path.dirname(os.path.abspath(__file__)) 
file_path = os.path.join(script_dir, 'rates.csv')  

app = Flask(__name__)


response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0]['rates']

with open(file_path, 'w', newline='') as csvfile:
    saverate = csv.writer(csvfile, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    saverate.writerow(['Currency', 'Code', 'Exchange Rate'])
    
    for rate in rates:
        saverate.writerow([rate['currency'], rate['code'], rate['bid'], rate['ask']])

@app.route('/', methods=['GET', 'POST'])
def index():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    rates = data[0]['rates']
    
    selected_currency = None
    selected_ask = None
    input_value = 0
    result = None

    if request.method == 'POST':
        selected_currency = request.form.get('waluty')
        input_value = request.form.get('wartosc2')

    for rate in rates:
        if rate['code'] == selected_currency:
            selected_ask = rate['ask']
            break

    if selected_ask and input_value:
            try:
                result = float(input_value) * selected_ask 
            except Exception as e:
                result = "Błąd: " + str(e)
    
    return render_template('form.html', rates=rates, selected_currency=selected_currency, selected_ask=selected_ask, input_value=input_value, result=result)

if __name__ == "__main__":
    app.run(debug=True)

    