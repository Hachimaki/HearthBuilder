#!/usr/bin/env python3

import matplotlib.pyplot as plt
import click

@click.command()
@click.argument('data_file', type=click.File('r'))
@click.option('--hero', is_flag=True)
def main(data_file, hero):

    lines = data_file.readlines()

    values = []
    if hero:
        values = [eval(line.split(',')[0]) for line in lines[1:]]

    plt.plot([i for i in range(len(values))], values, 'b-')
    plt.ylabel("% of decks containing the card")
    plt.xlabel("card ranked by popularity")
    plt.title(data_file.name)
    plt.show()

if __name__ == '__main__':
    main()