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

    entities_dict = {}
    for ent in doc.ents:
        if ent.label_.lower() == 'no_of_people':
            if ent.text.lower() == 'ein':
                int_value = 1
            elif ent.text.lower() == 'eine':
                int_value = 1
            elif ent.text.lower() == 'einen':
                int_value = 1
            elif ent.text.lower() == 'einer':
                int_value = 1
            elif ent.text.lower() == 'zwei':
                int_value = 2
            elif ent.text.lower() == 'drei':
                int_value = 3
            elif ent.text.lower() == 'vier':
                int_value = 4
            elif ent.text.lower() == 'fünf':
                int_value = 5
            elif ent.text.lower() == 'sechs':
                int_value = 6
            elif ent.text.lower() == 'sieben':
                int_value = 7
            elif ent.text.lower() == 'acht':
                int_value = 8
            else:
                int_value = 1

            entities_dict[ent.label_.lower()] = int_value

        else:
            text_value = ent.text.lower()
            entities_dict[ent.label_.lower()] = text_value

    if "no_of_people" not in entities_dict:
        entities_dict["no_of_people"] = 1

    if "no_of_people" in entities_dict:
        if isinstance(entities_dict["no_of_people"], str):
            try:
                entities_dict["no_of_people"] = int(
                    entities_dict["no_of_people"])
            except ValueError:
                entities_dict["no_of_people"] = 1
    else:
        entities_dict["no_of_people"] = 1

    result = jsonify(entities_dict)
    print(entities_dict)
    return result


if __name__ == "__main__":
    app.run(debug=True)
