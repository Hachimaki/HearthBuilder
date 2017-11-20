from sqlalchemy.orm.session import Session

from database import new_session, Edge, Node, Archetype, Card
from database import Base as BaseModel


import json, itertools


class DeckModel:
    """
    This doesn't get used persistently, it's just
    an ease-of-use model for this script.

    "deck_id": "9pyGuklWyjzoFvRvKyJnEg",
    "deck_list": "[[40523,2],[38718,1], ... ,
    "archetype_id": 147,
    "digest": "d527d61b32ec5ee374af83a43cf697ff",
    "total_games": 1937,
    "win_rate": 58.18,
    "avg_game_length_seconds": 500,
    "avg_num_player_turns": 10
    """
    def __init__(self, **attrs):
        for key, value in attrs.items():
            try:
                v = int(value)
                setattr(self, key, v)
            except ValueError:
                setattr(self, key, value)

        # str -> [] of []
        self.deck_list = eval(str(self.deck_list))

        # [] of [] -> [] of ()
        self.deck_list = [tuple(l) for l in self.deck_list]

        # str -> int ???


def find_or_create_archetype(session, kwargs):
    instance = session.query(Archetype).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = Archetype(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def find_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance


def get_card(card_db: dict, dbf_id: int) -> dict:
    """
    Returns dict representing a card. Useful attribute is the
    name.
    :param dbf_id: Int ID of the card you're looking for.
    :return: A dict representing a card.
    """
    return next(card for card in card_db if card["dbfId"] == dbf_id)


if __name__ == '__main__':

    db = new_session()

    with open('database/decks.json') as deck_data, open('database/cards.json') as card_data:
        data = json.load(deck_data)
        data = data['series']['data']

        card_db = json.load(card_data)

        for hero, decks in data.items():
            print(hero)

            num_decks = len(decks)
            counter = 1
            for deck in decks:
                print(counter, "/", num_decks)
                counter += 1

                model = DeckModel(**deck)
                print(model.deck_id)

                arch = find_or_create(db, Archetype, id=model.archetype_id)
                nodes = [find_or_create(db, Node, dbfId=dbfId, count=count) for dbfId, count in model.deck_list]

                for n in nodes:
                    card = get_card(card_db, n.dbfId)
                    card_model = find_or_create(db, Card, id=n.dbfId, name=card['name'])
                    if arch not in n.archetype:
                        n.archetype.append(arch)
                        card_model.archetype.append(arch)

                edges = itertools.combinations(nodes, 2)

                for n1, n2 in edges:

                    new_edge = None
                    if n1.id <= n2.id:
                        new_edge = find_or_create(db, Edge, node1=n1, node2=n2, weight=1)
                    else:
                        new_edge = find_or_create(db, Edge, node1=n2, node2=n1, weight=1)
                    db.add(new_edge)

                db.commit()

            exit()
