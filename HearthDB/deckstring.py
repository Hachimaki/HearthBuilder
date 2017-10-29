#!/usr/bin/env python2

import click

from models import Deck

@click.command()
@click.argument("code", type=str)
def decode(code):
    deck = Deck(code)

    for card in deck.cards:
        print card.name


if __name__ == '__main__':
    decode()
