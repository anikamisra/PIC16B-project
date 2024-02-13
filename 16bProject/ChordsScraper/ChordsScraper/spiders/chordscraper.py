import scrapy

class ChordsScraperSpider(scrapy.Spider):
    name = 'chord_scraper'

    def __init__(self, subdir=None, *args, **kwargs):
        self.start_urls = [f"http://www.mldb.org/song-250991-dance-the-night.html"]
        
        
    def parse_song_title(self, response):
        song_title = response.css('h1::text').extract()
        song_artist = response.css('a::text').extract()[51]
        song_lyrics = response.css('p.songtext::text').extract() 
        yield {"song" : song_title, "artist" : song_artist, "lyrics" : song_lyrics}
