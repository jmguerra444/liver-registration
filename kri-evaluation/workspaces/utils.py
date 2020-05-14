
import json

def getData():
    with open("data.json") as json_file:
        data = json.load(json_file)
    return data

def log(msg, filename):
    with open(filename, "a") as t:
        t.write(msg)
        t.write("\n")