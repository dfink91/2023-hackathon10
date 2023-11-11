from flask import Flask, request
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

apikey = os.environ.get('API_KEY')
print(apikey)

def call_chatgpt(prompt):
    url = "https://api.openai.com/v1/engines/text-davinci-003/completions"
    headers = {
    "Authorization": f"Bearer {apikey}",
    "Content-Type": "application/json",
}
    data = {
        "prompt": prompt,
        "max_tokens": 150
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

@app.route('/recognize')
def hello():
    text = request.args.get('text', '')
    
    prompt = f"Extrahiere die Entitäten Abfahrtsort, Zielort, Personen, Datum und Uhrzeit im Text '{text}'. Gebe als Ergebnis nur das json zurück. Konvertiere Uhrzeiten in das Format HH:mm. Konvertiere das Datum in das Format yyyy-mm-dd. Fülle das Feld Personen nur mit einem Integer aus. Falls keine Person angegeben ist, nimm 1 an. Wenn kein Datum oder morgen angegeben ist, schreibe 'heute'."
    response = call_chatgpt(prompt)
    result = response["choices"][0]["text"]
    print(result)
    result_as_json = json.loads(result)

    if not result_as_json.get('Datum') and not result_as_json.get('Uhrzeit'):
        when_value = "now"
    else:
        when_value = {
            "date": result_as_json['Datum'],
            "time": result_as_json['Uhrzeit']
        }

    converted_json = {
        "departure": result_as_json['Abfahrtsort'],
        "destination": result_as_json['Zielort'],
        "no_of_people": result_as_json['Personen'],
        "when": when_value
    }
    
    return converted_json

if __name__ == "__main__":
    app.run(debug=True)
