import scrapy

class DeckSpider(scrapy.Spider):
    name = 'decks'
    start_urls = ['https://hsreplay.net/decks/#page=1']

    def parse(self, response):
        for tile in response.css('div.deck-tile'):
            print tile.css('span.deck-name').extract_first()
