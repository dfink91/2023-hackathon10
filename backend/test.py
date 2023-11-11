import requests
import json

def call_chatgpt(prompt):
    url = "https://api.openai.com/v1/engines/text-davinci-003/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
        "max_tokens": 150
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

text = "Taxi von Bozen nach Meran am 12.11. um 15 Uhr für vier Personen"
prompt = f"Extrahiere die Entitäten Abfahrtsort, Zielort, Personen, Datum und Uhrzeit im Text '{text}'. Gebe als Ergebnis nur das json zurück. Konvertiere Uhrzeiten in das Format HH:mm. Konvertiere das Datum in das Format yyyy-mm-dd. Fülle das Feld Personen nur mit einem Integer aus. Falls keine Person angegeben ist, nimm 1 an. Wenn kein Datum oder morgen angegeben ist, schreibe 'heute'."
response = call_chatgpt(prompt)
result = response["choices"][0]["text"]
print(result)
json = json.loads(result)

converted_json = {
    "departure": json['Abfahrtsort'],
    "destination": json['Zielort'],
    "no_of_people": json['Personen'],
    "when": {
        "date": json['Datum'],
        "time": json['Uhrzeit']
    }
}


print(converted_json)