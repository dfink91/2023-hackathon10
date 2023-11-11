from flask import Flask, request, jsonify
import spacy
import os
import openai

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
        if ent.label_ == 'no_of_people':
            if ent.text == 'ein':
                int_value = 1
            elif ent.text == 'eine':
                int_value = 1
            elif ent.text == 'einen':
                int_value = 1
            elif ent.text == 'einer':
                int_value = 1
            elif ent.text == 'zwei':
                int_value = 2
            elif ent.text == 'drei':
                int_value = 3
            elif ent.text == 'vier':
                int_value = 4
            elif ent.text == 'fünf':
                int_value = 5
            elif ent.text == 'sechs':
                int_value = 6
            elif ent.text == 'sieben':
                int_value = 7
            elif ent.text == 'acht':
                int_value = 8
            else:
                int_value = 1

            entities_dict[ent.label_] = int_value

        else:
            text_value = ent.text
            entities_dict[ent.label_] = text_value

    if "no_of_people" not in entities_dict:
        entities_dict["no_of_people"] = 1
    if "when" not in entities_dict:
        entities_dict["when"] = "now"

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
