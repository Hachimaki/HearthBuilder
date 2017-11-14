import json

from hearth_db import HearthDB

counter = 0

hearthdb = HearthDB()

with open('dataset.json') as json_data:
    data = json.load(json_data)
    data = data['series']['data']

    for _class, decks in data.items():
        print(_class)

        for deck in decks:

            cards = eval(deck['deck_list'])

            meta = {
                'archtype': deck['archetype_id'],
                'total_games': deck['total_games'],
                'win_rate': deck['win_rate']
            }

            deck = hearthdb.create_deck(_class, cards)
            deck = hearthdb.add_metadata(deck, _class, **meta)

            print(deck.deckcode)
            # exit()
