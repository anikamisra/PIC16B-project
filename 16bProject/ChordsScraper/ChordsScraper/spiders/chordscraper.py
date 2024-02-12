import scrapy

class ChordsScraperSpider(scrapy.Spider):
    name = 'ChordsScraper'

    def __init__(self, *args, **kwargs):
        self.start_urls = [f"https://www.ultimate-guitar.com/explore"]

    def parse(self, response):
        """
        Function assumes that we are on the home page of website
        Gets individual links for songs
        """
        return(0)
