#!/usr/bin/env python2

import os
import json
import requests
import base64
import click

db_url = "https://api.hearthstonejson.com/v1/18336/enUS/cards.collectible.json"
db_path = "./db.json"

if os.path.exists(db_path):
    with open(db_path, "r") as f:
        db = json.loads(f.read())
else:
    response = requests.get(db_url)
    if response.status_code == 200:
        with open(db_path, "w") as f:
            f.write(response.text.encode("utf-8"))
            db = response.json()
    else:
        raise RuntimeError("Couldn't download cards database: %s"
                           % response.text)


@click.group()
def hsd():
    return


@hsd.command()
@click.argument("code", type=str)
def decode(code):
    bytes = map(ord, base64.b64decode(code))
    header, bytes = bytes[:5], bytes[5:]

    def read_cards(amount):
        n = bytes.pop(0)
        cards = []
        for _ in xrange(n):
            low, high = bytes.pop(0), bytes.pop(0)
            card_id = (high << 8) + low
            dbf_id = (card_id >> 8) << 7 | (card_id % 128)
            card = get_card(dbf_id)
            card["amount"] = amount
            cards.append(get_card(dbf_id))
        return cards

    singles = read_cards(1)
    doubles = read_cards(2)

    cards = sorted(singles + doubles,
                   key=lambda card: (card["cost"], card["name"]))

    click.echo("\n".join(map(format_card, cards)))

def get_card(dbf_id):
    return next(card for card in db if card["dbfId"] == dbf_id)


def format_card(card):
    return "%dx (%d) %s" % (card["amount"], card["cost"], card["name"])


if __name__ == "__main__":
    hsd()
