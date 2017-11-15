from database import new_session, Base, Edge
from database import Node as DeckItem

import json


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

        # str -> int


if __name__ == '__main__':

    db = new_session()

    with open('database/decks.json') as json_data:
        data = json.load(json_data)
        data = data['series']['data']

        for hero, decks in data.items():
            print(hero)

            for deck in decks:
                model = DeckModel(**deck)

                items = []
                for dbfId, count in model.deck_list:
                    item = DeckItem(dbfId=dbfId,
                                    count=count,
                                    archetype=model.archetype_id)

                    edges = [Edge(node1=item, node2=i) for i in items]
                    [db.add(edge) for edge in edges]
                    items.append(item)
                    db.add(item)
                    db.commit()

                exit()
