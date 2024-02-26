import scrapy 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapy.selector import Selector
from scrapy.http import Request

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
        self.driver.quit()
