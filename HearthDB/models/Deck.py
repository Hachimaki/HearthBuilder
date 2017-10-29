from hearthstone.deckstrings import Deck as HSDeck
from mongoengine import *
from Card import Card

class Deck(Document):

    deckcode = StringField()
    cards = ListField(ReferenceField(Card))

    def __init__(self, deckcode, self_init=True):
        self.deckcode = deckcode

        if self_init:
            hsdeck = HSDeck.from_deckstring(deckcode)
            for dbfId, count in hsdeck.cards:
                card = Card.make_card(dbfId)
                for i in range(count):
                    cards.append(card)
