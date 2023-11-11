import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding
import random
import os

model_path = "./model.dat"

if os.path.exists(model_path):
    nlp = spacy.load(model_path)
else:
    nlp = spacy.load("de_core_news_sm")  

    def find_entity_positions(sentence, entity):
        start = sentence.find(entity)
        if start == -1:  # Entity not found
            return None
        end = start + len(entity)
        return (start, end)

    sentences = [
        "Bitte buchen Sie ein Taxi von Sankt Ulrich nach Santa Christina für zwei Personen",
        "Bitte buchen Sie ein Taxi von Santa Christina nach Wolkenstein für drei Personen",
        "Bitte buchen Sie ein Taxi von Wolkenstein nach Sankt Ulrich für eine Person",
        "Kann ich ein Taxi von Sankt Ulrich nach Bozen für vier Personen bekommen?",
        "Ich brauche ein Taxi von Bozen nach Santa Christina für zwei Fahrgäste.",
        "Buchen Sie ein Taxi von Wolkenstein nach Brixen für fünf Personen.",
        "Reservieren Sie ein Taxi von Brixen nach Wolkenstein für drei Gäste.",
        "Organisieren Sie ein Taxi von Santa Christina nach Meran für zwei Personen.",
        "Könnten Sie ein Taxi für mich von Meran nach Sankt Ulrich für vier Personen buchen?",
        "Ich möchte ein Taxi von Sankt Ulrich nach Klausen für eine Person buchen.",
        "Brauche ein Taxi von Klausen nach Santa Christina für drei Personen.",
        "Planen Sie ein Taxi von Wolkenstein nach Sankt Ulrich für zwei Personen.",
        "Ich möchte ein Taxi von Sankt Ulrich nach Wolkenstein für vier Personen.",
        "Taxi von Sankt Ulrich nach Santa Christina für zwei Personen",
        "Taxi von Santa Christina nach Wolkenstein für drei Personen",
        "Taxi von Wolkenstein nach Sankt Ulrich für einen",
        "Taxi von Sankt Ulrich nach Bozen für vier",
        "Taxi von Bozen nach Santa Christina für zwei.",
        "Taxi von Wolkenstein nach Brixen für fünf.",
        "Taxi von Brixen nach Wolkenstein für drei.",
        "Taxi von Santa Christina nach Meran für zwei.",
        "Taxi für mich von Meran nach Sankt Ulrich für vier Personen",
        "Taxi von Sankt Ulrich nach Klausen für eine Person.",
        "Taxi von Klausen nach Santa Christina für drei.",
        "Taxi von Wolkenstein nach Sankt Ulrich für zwei.",
        "Taxi von Sankt Ulrich nach Wolkenstein für vier."
    ]

    entities_info = [
        {"DEPARTURE": "Sankt Ulrich", "DESTINATION": "Santa Christina", "NO_OF_PEOPLE": "zwei"},
        {"DEPARTURE": "Santa Christina", "DESTINATION": "Wolkenstein", "NO_OF_PEOPLE": "drei"},
        {"DEPARTURE": "Wolkenstein", "DESTINATION": "Sankt Ulrich", "NO_OF_PEOPLE": "eine"},
        {"DEPARTURE": "Sankt Ulrich", "DESTINATION": "Bozen", "NO_OF_PEOPLE": "vier"},
        {"DEPARTURE": "Bozen", "DESTINATION": "Santa Christina", "NO_OF_PEOPLE": "zwei"},
        {"DEPARTURE": "Wolkenstein", "DESTINATION": "Brixen", "NO_OF_PEOPLE": "fünf"},
        {"DEPARTURE": "Brixen", "DESTINATION": "Wolkenstein", "NO_OF_PEOPLE": "drei"},
        {"DEPARTURE": "Santa Christina", "DESTINATION": "Meran", "NO_OF_PEOPLE": "zwei"},
        {"DEPARTURE": "Meran", "DESTINATION": "Sankt Ulrich", "NO_OF_PEOPLE": "vier"},
        {"DEPARTURE": "Sankt Ulrich", "DESTINATION": "Klausen", "NO_OF_PEOPLE": "eine"},
        {"DEPARTURE": "Klausen", "DESTINATION": "Santa Christina", "NO_OF_PEOPLE": "drei"},
        {"DEPARTURE": "Wolkenstein", "DESTINATION": "Sankt Ulrich", "NO_OF_PEOPLE": "zwei"},
        {"DEPARTURE": "Sankt Ulrich", "DESTINATION": "Wolkenstein", "NO_OF_PEOPLE": "vier"},
        {"DEPARTURE": "Sankt Ulrich", "DESTINATION": "Santa Christina", "NO_OF_PEOPLE": "zwei"},
        {"DEPARTURE": "Santa Christina", "DESTINATION": "Wolkenstein", "NO_OF_PEOPLE": "drei"},
        {"DEPARTURE": "Wolkenstein", "DESTINATION": "Sankt Ulrich", "NO_OF_PEOPLE": "eine"},
        {"DEPARTURE": "Sankt Ulrich", "DESTINATION": "Bozen", "NO_OF_PEOPLE": "vier"},
        {"DEPARTURE": "Bozen", "DESTINATION": "Santa Christina", "NO_OF_PEOPLE": "zwei"},
        {"DEPARTURE": "Wolkenstein", "DESTINATION": "Brixen", "NO_OF_PEOPLE": "fünf"},
        {"DEPARTURE": "Brixen", "DESTINATION": "Wolkenstein", "NO_OF_PEOPLE": "drei"},
        {"DEPARTURE": "Santa Christina", "DESTINATION": "Meran", "NO_OF_PEOPLE": "zwei"},
        {"DEPARTURE": "Meran", "DESTINATION": "Sankt Ulrich", "NO_OF_PEOPLE": "vier"},
        {"DEPARTURE": "Sankt Ulrich", "DESTINATION": "Klausen", "NO_OF_PEOPLE": "eine"},
        {"DEPARTURE": "Klausen", "DESTINATION": "Santa Christina", "NO_OF_PEOPLE": "drei"},
        {"DEPARTURE": "Wolkenstein", "DESTINATION": "Sankt Ulrich", "NO_OF_PEOPLE": "zwei"},
        {"DEPARTURE": "Sankt Ulrich", "DESTINATION": "Wolkenstein", "NO_OF_PEOPLE": "vier"}
    ]

    TRAIN_DATA = []
    for sentence, entity_info in zip(sentences, entities_info):
        entities = []
        for entity_label, entity in entity_info.items():
            position = find_entity_positions(sentence, entity)
            if position:
                entities.append((position[0], position[1], entity_label))
        TRAIN_DATA.append((sentence, {"entities": entities}))

    # Update the model
    ner = nlp.get_pipe("ner")

    # Add new entity labels to the NER pipeline
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # Disable other pipelines during training
    disabled_pipelines = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

    with nlp.disable_pipes(*disabled_pipelines):
        optimizer = nlp.resume_training()
        for iteration in range(100): # You can adjust the number of iterations
            random.shuffle(TRAIN_DATA)
            losses = {}
            batches = minibatch(TRAIN_DATA, size=compounding(4., 32., 1.001))
            for batch in batches:
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    nlp.update([example], drop=0.5, losses=losses)
            print("Losses at iteration", iteration, ":", losses)

    nlp.to_disk(model_path)

# test_text = "Bitte ein Taxi von Armentarola zur Lagazuoi Seilbahn für zwei."
# doc = nlp(test_text)
# print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])

