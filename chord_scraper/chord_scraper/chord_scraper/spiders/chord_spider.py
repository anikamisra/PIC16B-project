import scrapy 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapy.selector import Selector
from scrapy.http import Request
import time 

# this code parses the song page once you are on it. 
# HERE IS WHAT TO PUT IN THE TERMINAL: 
# if you are using the first scraper: 
# scrapy crawl chord_scraper -o results.csv -a url_of_song=https://chordify.net/chords/ariana-grande-songs/dangerous-woman-chords

# if you are using the second scraper: 
# scrapy crawl chord_scraper -o results.csv -a artistname=dua-lipa
"""
class chord_scraper(scrapy.Spider): 
    name = 'chord_scraper'
    
    def __init__(self, url_of_song, *args, **kwargs): 
        super().__init__(*args, **kwargs)  # don't forget to call the super's __init__
        
        # might not need this code 
        if not url_of_song.startswith(('http://', 'https://')):
            url_of_song = 'http://' + url_of_song
        self.start_urls = [url_of_song]
        
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def parse(self, response):
        self.driver.get(response.url)
        
        # Wait for the page to load, cuz otherwise chords take forever 
        import time
        time.sleep(5) 

        # Now you can access the HTML of the page
        html = self.driver.page_source
        sel = Selector(text=html)

        # Now you can use sel just like the response, how we did with scrapy 
        div = sel.css('div.s4xyh0t > div.chords')
        barlength = div.css('::attr(class)').re_first('barlength-(\d+)')
        tags_with_i_value = div.css('[data-i]')
        table = [{'i-value': tag.css('::attr(data-i)').get(), 'data-handle': tag.css('::attr(data-handle)').get(), 'barlength': barlength} for tag in tags_with_i_value]
        for row in table:
            yield row

    def closed(self, reason):
        self.driver.quit()"""

# this code parses the artist page and returns the list of songs for a given artist. 

class chord_scraper(scrapy.Spider): 
    name = 'chord_scraper'
    
    def __init__(self, artistname, *args, **kwargs): 
        super().__init__(*args, **kwargs)  
        # format artist name properly 
        artistname_formatted = ("-".join(artistname.split())).lower()
        
        # form url of artist page 
        artist_page_url = "https://chordify.net/chords/"+artistname_formatted+"-songs"
        # need to add an error catcher for if this artist page doesn't exist 
        self.start_urls = [artist_page_url]
        
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
    def parse(self, response):
        
        self.driver.get(response.url) 
        time.sleep(5)
        html = self.driver.page_source
        sel = Selector(text=html) 
        # select the main div containing all the songs
        main_div = sel.css('div.s1qyqb8i.g1aau9lx')
        
        for link in sel.css('div.s1qyqb8i.g1aau9lx a::attr(href)'):
        # get the url
            song_url = link.get()

        # get the associated song title
            #song_title_parts = link.xpath('./following-sibling::div[1]/span/text()').getall()
            #song_title = ''.join(song_title_parts)
            start = song_url.rfind("/")
            end = len(song_url) - 7 
            song_title = song_url[start+1:end]
            song_title = (song_title.replace('-', ' ')).title()

        # yield the result as a dictionary
            yield {
                'song_name': song_title,
                'song_url': song_url,
            }
        
    def closed(self, reason): 
        self.driver.quit()