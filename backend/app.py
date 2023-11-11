from flask import Flask, request, jsonify
import spacy
import os

app = Flask(__name__)

model_path = "./model.dat"
if os.path.exists(model_path):
    nlp = spacy.load(model_path)

@app.route('/recognize')
def hello():    
    text_to_parse = request.args.get('text', '')
    doc = nlp(text_to_parse)

    # Create a dictionary to store entities
    entities_dict = {}
    for ent in doc.ents:
        if ent.label_.lower() == 'no_of_people':
            if ent.text.lower() == 'ein':
                text_value = '1'
            elif ent.text.lower() == 'eine':
                text_value = '1'
            elif ent.text.lower() == 'einer':
                text_value = '1'
            elif ent.text.lower() == 'zwei':
                text_value = '2'
            elif ent.text.lower() == 'drei':
                text_value = '3'
            elif ent.text.lower() == 'vier':
                text_value = '4'
            elif ent.text.lower() == 'fünf':
                text_value = '5'
            elif ent.text.lower() == 'sechs':
                text_value = '6'
            elif ent.text.lower() == 'sieben':
                text_value = '7'
            elif ent.text.lower() == 'acht':
                text_value = '8'
            elif ent.text.lower() == 'neun':
                text_value = '9'
            elif ent.text.lower() == 'zehn':
                text_value = '10'
            else:
                text_value = ent.text.lower()
        else:
            text_value = ent.text.lower()

        if ent.label_.lower() in entities_dict:
            entities_dict[ent.label_.lower()].append(text_value)
        else:
            entities_dict[ent.label_.lower()] = [text_value]

    # Return the entities as a JSON response
    return jsonify(entities_dict)


if __name__ == "__main__":
    app.run()