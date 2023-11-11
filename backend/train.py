import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding
import random
import os
import shutil

model_path = "./model.dat"

if os.path.exists(model_path):
    shutil.rmtree(model_path)
    
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
    "Taxi von Sankt Ulrich nach Wolkenstein für vier.",
    "Bitte buchen Sie ein Taxi von Sankt Ulrich nach Santa Christina für zwei Personen um 08:15 Uhr."
    "Bitte buchen Sie ein Taxi von Santa Christina nach Wolkenstein für drei Personen um 09:30 Uhr."
    "Bitte buchen Sie ein Taxi von Wolkenstein nach Sankt Ulrich für eine Person um 11:00 Uhr."
    "Kann ich ein Taxi von Sankt Ulrich nach Bozen für vier Personen um 13:45 Uhr bekommen?"
    "Ich brauche ein Taxi von Bozen nach Santa Christina für zwei Fahrgäste um 15:20 Uhr."
    "Buchen Sie ein Taxi von Wolkenstein nach Brixen für fünf Personen um 16:35 Uhr."
    "Reservieren Sie ein Taxi von Brixen nach Wolkenstein für drei Gäste um 18:00 Uhr."
    "Organisieren Sie ein Taxi von Santa Christina nach Meran für zwei Personen um 19:15 Uhr."
    "Könnten Sie ein Taxi für mich von Meran nach Sankt Ulrich für vier Personen um 20:30 Uhr buchen?"
    "Ich möchte ein Taxi von Sankt Ulrich nach Klausen für eine Person um 21:45 Uhr buchen."
    "Brauche ein Taxi von Klausen nach Santa Christina für drei Personen um 07:00 Uhr morgens."
    "Planen Sie ein Taxi von Wolkenstein nach Sankt Ulrich für zwei Personen um 10:10 Uhr."
    "Ich möchte ein Taxi von Sankt Ulrich nach Wolkenstein für vier Personen um 12:25 Uhr."
    "Taxi von Sankt Ulrich nach Santa Christina für zwei Personen um 14:40 Uhr."
    "Taxi von Santa Christina nach Wolkenstein für drei Personen um 17:05 Uhr."
    "Taxi von Wolkenstein nach Sankt Ulrich für einen um 22:15 Uhr."
    "Taxi von Sankt Ulrich nach Bozen für vier um 23:30 Uhr."
    "Taxi von Bozen nach Santa Christina für zwei um 06:45 Uhr."
    "Taxi von Wolkenstein nach Brixen für fünf um 08:30 Uhr."
    "Taxi von Brixen nach Wolkenstein für drei um 09:50 Uhr."
    "Taxi von Santa Christina nach Meran für zwei um 11:10 Uhr."
    "Taxi für mich von Meran nach Sankt Ulrich für vier Personen um 12:55 Uhr."
    "Taxi von Sankt Ulrich nach Klausen für eine Person um 14:10 Uhr."
    "Taxi von Klausen nach Santa Christina für drei um 15:30 Uhr."
    "Taxi von Wolkenstein nach Sankt Ulrich für zwei um 16:45 Uhr."
    "Taxi von Sankt Ulrich nach Wolkenstein für vier um 18:20 Uhr.",
    "Bitte buchen Sie ein Taxi von Sankt Ulrich nach Santa Christina für zwei Personen morgen um 08:15 Uhr.",
    "Bitte buchen Sie ein Taxi von Santa Christina nach Wolkenstein für drei Personen am 15. November um 09:30 Uhr.",
    "Bitte buchen Sie ein Taxi von Wolkenstein nach Sankt Ulrich für eine Person übermorgen um 11:00 Uhr.",
    "Kann ich ein Taxi von Sankt Ulrich nach Bozen für vier Personen am 17. Dezember um 13:45 Uhr bekommen?",
    "Ich brauche ein Taxi von Bozen nach Santa Christina für zwei Fahrgäste morgen um 15:20 Uhr.",
    "Buchen Sie ein Taxi von Wolkenstein nach Brixen für fünf Personen übermorgen um 16:35 Uhr.",
    "Reservieren Sie ein Taxi von Brixen nach Wolkenstein für drei Gäste am 16. Jänner um 18:00 Uhr.",
    "Organisieren Sie ein Taxi von Santa Christina nach Meran für zwei Personen morgen um 19:15 Uhr.",
    "Könnten Sie ein Taxi für mich von Meran nach Sankt Ulrich für vier Personen am 15. Februar um 20:30 Uhr buchen?",
    "Ich möchte ein Taxi von Sankt Ulrich nach Klausen für eine Person übermorgen um 21:45 Uhr buchen.",
    "Brauche ein Taxi von Klausen nach Santa Christina für drei Personen morgen um 07:00 Uhr.",
    "Planen Sie ein Taxi von Wolkenstein nach Sankt Ulrich für zwei Personen am 17. März um 10:10 Uhr.",
    "Ich möchte ein Taxi von Sankt Ulrich nach Wolkenstein für vier Personen übermorgen um 12:25 Uhr.",
    "Taxi von Sankt Ulrich nach Santa Christina für zwei Personen am 16. April um 14:40 Uhr.",
    "Taxi von Santa Christina nach Wolkenstein für drei Personen morgen um 17:05 Uhr.",
    "Taxi von Wolkenstein nach Sankt Ulrich für einen am 15. Mai um 22:15 Uhr.",
    "Taxi von Sankt Ulrich nach Bozen für vier übermorgen um 23:30 Uhr.",
    "Taxi von Bozen nach Santa Christina für zwei morgen um 06:45 Uhr.",
    "Taxi von Wolkenstein nach Brixen für fünf am 16. Juni um 08:30 Uhr.",
    "Taxi von Brixen nach Wolkenstein für drei am 17. Juli um 09:50 Uhr.",
    "Taxi von Santa Christina nach Meran für zwei morgen um 11:10 Uhr.",
    "Taxi für mich von Meran nach Sankt Ulrich für vier Personen übermorgen um 12:55 Uhr.",
    "Taxi von Sankt Ulrich nach Klausen für eine Person am 15. August um 14:10 Uhr.",
    "Taxi von Klausen nach Santa Christina für drei morgen um 15:30 Uhr.",
    "Taxi von Wolkenstein nach Sankt Ulrich für zwei am 16. September um 16:45 Uhr.",
    "Taxi von Sankt Ulrich nach Wolkenstein für vier am 5. Oktober um 18:20 Uhr."
]

entities_info = [
    {"departure": "Sankt Ulrich", "destination": "Santa Christina", "no_of_people": "zwei"},
    {"departure": "Santa Christina", "destination": "Wolkenstein", "no_of_people": "drei"},
    {"departure": "Wolkenstein", "destination": "Sankt Ulrich", "no_of_people": "eine"},
    {"departure": "Sankt Ulrich", "destination": "Bozen", "no_of_people": "vier"},
    {"departure": "Bozen", "destination": "Santa Christina", "no_of_people": "zwei"},
    {"departure": "Wolkenstein", "destination": "Brixen", "no_of_people": "fünf"},
    {"departure": "Brixen", "destination": "Wolkenstein", "no_of_people": "drei"},
    {"departure": "Santa Christina", "destination": "Meran", "no_of_people": "zwei"},
    {"departure": "Meran", "destination": "Sankt Ulrich", "no_of_people": "vier"},
    {"departure": "Sankt Ulrich", "destination": "Klausen", "no_of_people": "eine"},
    {"departure": "Klausen", "destination": "Santa Christina", "no_of_people": "drei"},
    {"departure": "Wolkenstein", "destination": "Sankt Ulrich", "no_of_people": "zwei"},
    {"departure": "Sankt Ulrich", "destination": "Wolkenstein", "no_of_people": "vier"},
    {"departure": "Sankt Ulrich", "destination": "Santa Christina", "no_of_people": "zwei"},
    {"departure": "Santa Christina", "destination": "Wolkenstein", "no_of_people": "drei"},
    {"departure": "Wolkenstein", "destination": "Sankt Ulrich", "no_of_people": "einen"},
    {"departure": "Sankt Ulrich", "destination": "Bozen", "no_of_people": "vier"},
    {"departure": "Bozen", "destination": "Santa Christina", "no_of_people": "zwei"},
    {"departure": "Wolkenstein", "destination": "Brixen", "no_of_people": "fünf"},
    {"departure": "Brixen", "destination": "Wolkenstein", "no_of_people": "drei"},
    {"departure": "Santa Christina", "destination": "Meran", "no_of_people": "zwei"},
    {"departure": "Meran", "destination": "Sankt Ulrich", "no_of_people": "vier"},
    {"departure": "Sankt Ulrich", "destination": "Klausen", "no_of_people": "eine"},
    {"departure": "Klausen", "destination": "Santa Christina", "no_of_people": "drei"},
    {"departure": "Wolkenstein", "destination": "Sankt Ulrich", "no_of_people": "zwei"},
    {"departure": "Sankt Ulrich", "destination": "Wolkenstein", "no_of_people": "vier"},
    {"departure": "Sankt Ulrich", "destination": "Santa Christina", "no_of_people": "zwei", "time": "08:15"},
    {"departure": "Santa Christina", "destination": "Wolkenstein", "no_of_people": "drei", "time": "09:30"},
    {"departure": "Wolkenstein", "destination": "Sankt Ulrich", "no_of_people": "eine", "time": "11:00"},
    {"departure": "Sankt Ulrich", "destination": "Bozen", "no_of_people": "vier", "time": "13:45"},
    {"departure": "Bozen", "destination": "Santa Christina", "no_of_people": "zwei", "time": "15:20"},
    {"departure": "Wolkenstein", "destination": "Brixen", "no_of_people": "fünf", "time": "16:35"},
    {"departure": "Brixen", "destination": "Wolkenstein", "no_of_people": "drei", "time": "18:00"},
    {"departure": "Santa Christina", "destination": "Meran", "no_of_people": "zwei", "time": "19:15"},
    {"departure": "Meran", "destination": "Sankt Ulrich", "no_of_people": "vier", "time": "20:30"},
    {"departure": "Sankt Ulrich", "destination": "Klausen", "no_of_people": "eine", "time": "21:45"},
    {"departure": "Klausen", "destination": "Santa Christina", "no_of_people": "drei", "time": "07:00"},
    {"departure": "Wolkenstein", "destination": "Sankt Ulrich", "no_of_people": "zwei", "time": "10:10"},
    {"departure": "Sankt Ulrich", "destination": "Wolkenstein", "no_of_people": "vier", "time": "12:25"},
    {"departure": "Sankt Ulrich", "destination": "Santa Christina", "no_of_people": "zwei", "time": "14:40"},
    {"departure": "Santa Christina", "destination": "Wolkenstein", "no_of_people": "drei", "time": "17:05"},
    {"departure": "Wolkenstein", "destination": "Sankt Ulrich", "no_of_people": "einen", "time": "22:15"},
    {"departure": "Sankt Ulrich", "destination": "Bozen", "no_of_people": "vier", "time": "23:30"},
    {"departure": "Bozen", "destination": "Santa Christina", "no_of_people": "zwei", "time": "06:45"},
    {"departure": "Wolkenstein", "destination": "Brixen", "no_of_people": "fünf", "time": "08:30"},
    {"departure": "Brixen", "destination": "Wolkenstein", "no_of_people": "drei", "time": "09:50"},
    {"departure": "Santa Christina", "destination": "Meran", "no_of_people": "zwei", "time": "11:10"},
    {"departure": "Meran", "destination": "Sankt Ulrich", "no_of_people": "vier", "time": "12:55"},
    {"departure": "Sankt Ulrich", "destination": "Klausen", "no_of_people": "eine", "time": "14:10"},
    {"departure": "Klausen", "destination": "Santa Christina", "no_of_people": "drei", "time": "15:30"},
    {"departure": "Wolkenstein", "destination": "Sankt Ulrich", "no_of_people": "zwei", "time": "16:45"},
    {"departure": "Sankt Ulrich", "destination": "Wolkenstein", "no_of_people": "vier", "time": "18:20"},
    {"departure": "Sankt Ulrich", "destination": "Santa Christina", "no_of_people": "zwei", "time": "08:15", "date": "morgen"},
    {"departure": "Santa Christina", "destination": "Wolkenstein", "no_of_people": "drei", "time": "09:30", "date": "15. November"},
    {"departure": "Wolkenstein", "destination": "Sankt Ulrich", "no_of_people": "eine", "time": "11:00", "date": "übermorgen"},
    {"departure": "Sankt Ulrich", "destination": "Bozen", "no_of_people": "vier", "time": "13:45", "date": "17. Dezember"},
    {"departure": "Bozen", "destination": "Santa Christina", "no_of_people": "zwei", "time": "15:20", "date": "morgen"},
    {"departure": "Wolkenstein", "destination": "Brixen", "no_of_people": "fünf", "time": "16:35", "date": "übermorgen"},
    {"departure": "Brixen", "destination": "Wolkenstein", "no_of_people": "drei", "time": "18:00", "date": "16. Jänner"},
    {"departure": "Santa Christina", "destination": "Meran", "no_of_people": "zwei", "time": "19:15", "date": "morgen"},
    {"departure": "Meran", "destination": "Sankt Ulrich", "no_of_people": "vier", "time": "20:30", "date": "15. Februar"},
    {"departure": "Sankt Ulrich", "destination": "Klausen", "no_of_people": "eine", "time": "21:45", "date": "übermorgen"},
    {"departure": "Klausen", "destination": "Santa Christina", "no_of_people": "drei", "time": "07:00", "date": "morgen"},
    {"departure": "Wolkenstein", "destination": "Sankt Ulrich", "no_of_people": "zwei", "time": "10:10", "date": "17. März"},
    {"departure": "Sankt Ulrich", "destination": "Wolkenstein", "no_of_people": "vier", "time": "12:25", "date": "übermorgen"},
    {"departure": "Sankt Ulrich", "destination": "Santa Christina", "no_of_people": "zwei", "time": "14:40", "date": "16. April"},
    {"departure": "Santa Christina", "destination": "Wolkenstein", "no_of_people": "drei", "time": "17:05", "date": "morgen"},
    {"departure": "Wolkenstein", "destination": "Sankt Ulrich", "no_of_people": "einen", "time": "22:15", "date": "15. Mai"},
    {"departure": "Sankt Ulrich", "destination": "Bozen", "no_of_people": "vier", "time": "23:30", "date": "übermorgen"},
    {"departure": "Bozen", "destination": "Santa Christina", "no_of_people": "zwei", "time": "06:45", "date": "morgen"},
    {"departure": "Wolkenstein", "destination": "Brixen", "no_of_people": "fünf", "time": "08:30", "date": "16. Juni"},
    {"departure": "Brixen", "destination": "Wolkenstein", "no_of_people": "drei", "time": "09:50", "date": "17. Juli"},
    {"departure": "Santa Christina", "destination": "Meran", "no_of_people": "zwei", "time": "11:10", "date": "morgen"},
    {"departure": "Meran", "destination": "Sankt Ulrich", "no_of_people": "vier", "time": "12:55", "date": "übermorgen"},
    {"departure": "Sankt Ulrich", "destination": "Klausen", "no_of_people": "eine", "time": "14:10", "date": "15. August"},
    {"departure": "Klausen", "destination": "Santa Christina", "no_of_people": "drei", "time": "15:30", "date": "morgen"},
    {"departure": "Wolkenstein", "destination": "Sankt Ulrich", "no_of_people": "zwei", "time": "16:45", "date": "16. September"},
    {"departure": "Sankt Ulrich", "destination": "Wolkenstein", "no_of_people": "vier", "time": "18:20", "date": "5. Oktober"}
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

