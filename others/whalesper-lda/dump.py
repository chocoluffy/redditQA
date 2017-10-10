import json
import pickle
def load_data():
    data = pickle.load(open("whalesper.pkl", "rb"))
    new_data = map(lambda x: {"body": x["body"], "title": x["title"], "author": x["author"]}, data)
    return new_data

data = load_data()
with open('whalesper.json', 'w') as outfile:
    json.dump(data, outfile)