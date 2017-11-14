from .. import HearthDB

if __name__ == '__main__':
    db = HearthDB()

    priest_decks = db.get_decks(hero=HearthDB.CLASS_PRIEST)

    for card, count in priest_decks[0].as_cards():
        print(db.get_card(card)['name'])


