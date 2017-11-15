from mongoengine import connect, Document, StringField, FloatField, LongField, IntField
from mongoengine import errors

from hearthstone.deckstrings import Deck as HSDeck
from hearthstone.enums import FormatType

import json


class Deck(Document):

    deckcode = StringField(unique=True)
    win_rate = FloatField()
    total_games = LongField()
    archtype = IntField()
    _class = IntField()

    def as_cards(self) -> list:
        deck = HSDeck.from_deckstring(self.deckcode)
        return deck.cards


class HearthDB:

    """
    Malfurion: 274
    Rexxar: 31
    Jaina: 637
    Uther: 671
    Anduin: 813
    Valeera: 930
    Thrall: 1066
    Gul'Dan: 893
    Garrosh: 7
    """
    CLASS_DRUID = 274
    CLASS_HUNTER = 31
    CLASS_MAGE = 637
    CLASS_PALADIN = 671
    CLASS_PRIEST = 813
    CLASS_ROGUE = 930
    CLASS_SHAMAN = 1066
    CLASS_WARLOCK = 893
    CLASS_WARRIOR = 7

    heroes = {
        'DRUID' : 274,
        'HUNTER' : 31,
        'MAGE' : 637,
        'PALADIN': 671,
        'PRIEST': 813,
        'ROGUE': 930,
        'SHAMAN': 1066,
        'WARLOCK': 893,
        'WARRIOR': 7
    }

    def __init__(self, host='localhost', port=27017):
        self.mongoclient = connect('hearthdb', host=host, port=port)
        self.card_db = json.load(open('db.json'))

    #
    #   These are for creating new decks. Do not touch
    #

    def create_deck(self, hero, cards, _format=FormatType.FT_STANDARD):
        hsdeck = HSDeck()
        hsdeck.cards = [tuple(card) for card in cards]
        # print(hsdeck.cards)
        hsdeck.heroes = [self.heroes[hero]]
        # print(hsdeck.heroes)
        hsdeck.format = _format
        # print(hsdeck.format)
        deck = Deck(deckcode = hsdeck.as_deckstring)
        try:
            deck.save()
        except errors.NotUniqueError:
            pass

        return deck

    def add_metadata(self, deck, _class, win_rate, total_games, archtype):
        deck._class = self.heroes[_class]
        deck.win_rate = win_rate
        deck.total_games = total_games
        deck.archtype = archtype

        try:
            deck.save()
        except errors.NotUniqueError:
            pass

        return deck

    #
    #   Class methods
    #

    def deck_count(self, hero: int=None) -> int:
        """
        Returns a count of the decks available per Hero, or all if
        no hero specified.
        :param hero: Pass a Deck.CLASS_ constant
        :return: Int number of decks per class.
        """
        if hero is None:
            return Deck.objects.deck_count()
        return Deck.objects.filter(_class=hero).count()

    def get_decks(self, hero: int=None):
        """
        Returns an interable of deck models per Hero, or all if
        no hero specified.
        :param hero: Pass a Deck.CLASS_ constant
        :return: Iterable of decks.
        """
        if hero is None:
            return Deck.objects.all()
        return Deck.objects.filter(_class=hero).all()

    def get_card(self, dbf_id: int) -> dict:
        """
        Returns dict representing a card. Useful attribute is the
        name.
        :param dbf_id: Int ID of the card you're looking for.
        :return: A dict representing a card.
        """
        return next(card for card in self.card_db if card["dbfId"] == dbf_id)
