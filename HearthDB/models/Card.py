from mongoengine import *
import sys, os, json
import requests

# Make sure we have the database
db = None
db_url = "https://api.hearthstonejson.com/v1/20970/enUS/cards.collectible.json"
db_path = "./db.json"

def init_db():
    global db
    tmp = dict()
    if os.path.exists(db_path):
        # print "Database already downloaded."
        with open(db_path, "r") as f:
            db = json.loads(f.read())
    else:
        print "Downloading card database..."
        response = requests.get(db_url)
        if response.status_code == 200:
            with open(db_path, "w") as f:
                f.write(response.text.encode("utf-8"))
                db = response.json()
                print "Download complete."
        else:
            raise RuntimeError("Couldn't download cards database: %s"
                               % response.text)

    for card in db:
        tmp[card['dbfId']] = card

    db = tmp

init_db()

class Card(Document):

    dbfId = StringField(primary_key=True)
    name = StringField()

    def __init__(self, dbfId):
        self.dbfId = dbfId
        self.name = db[dbfId]['name']
