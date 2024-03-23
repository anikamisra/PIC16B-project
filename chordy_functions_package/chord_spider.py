import scrapy 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from scrapy.selector import Selector
from scrapy.http import Request
import time 

# HERE IS WHAT TO PUT IN THE TERMINAL: 

# top 10 artists US 
# scrapy crawl chord_scraper -o results.csv -a artistname=dua-lipa
# scrapy crawl chord_scraper -o taylorswift.csv -a artistname=taylor-swift
# scrapy crawl chord_scraper -o badbunny.csv -a artistname=bad-bunny
# scrapy crawl chord_scraper -o theweeknd.csv -a artistname=the-weeknd
# scrapy crawl chord_scraper -o drake.csv -a artistname=drake
# scrapy crawl chord_scraper -o travisscott.csv -a artistname=travi-scott
# scrapy crawl chord_scraper -o beyonce.csv -a artistname=beyonce
# scrapy crawl chord_scraper -o michaeljackson.csv -a artistname=michael-jackson
# scrapy crawl chord_scraper -o ladygaga.csv -a artistname=lady-gaga
# scrapy crawl chord_scraper -o arianagrande.csv -a artistname=ariana-grande


class chord_scraper(scrapy.Spider): 
    name = 'chord_scraper'
    
    def __init__(self, artistname, *args, **kwargs):
        """
        Initializer for chord_scraper. Inherits from scrapy.Spider class
        """ 
        super().__init__(*args, **kwargs)  
        # format artist name properly 
        artistname_formatted = ("-".join(artistname.split())).lower()
        
        # form url of artist page 
        artist_page_url = "https://chordify.net/chords/"+artistname_formatted+"-songs"
        self.start_urls = [artist_page_url]
        
        # firefox option: 
        #options = Options()
        #options.headless = True
        #firefox_profile = webdriver.FirefoxProfile()
        #firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        #self.driver = webdriver.Firefox(options=options)
        
        # chrome option 
        options = ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--headless")

        # set up webdriver with these options 
        self.driver = webdriver.Chrome(options=options)
    def parse(self, response):
        """
        Parses artist's page and returns url for each song. 
        Calls the parse_song_url function for each song page url. 
        """
        
        self.driver.get(response.url) 
        # wait for page to load 
        time.sleep(5)
        html = self.driver.page_source
        sel = Selector(text=html) 
        # select the main html element containing all songs
        main_div = sel.css('div.s1qyqb8i.g1aau9lx')
        # iterate through each song and get the url for each song 
        for link in sel.css('div.s1qyqb8i.g1aau9lx a::attr(href)'):
            song_url = link.get()
            base_url = "https://chordify.net" + song_url # hard-coded url is okay 
            # call next scraper for the songs 
            yield scrapy.Request(url = base_url, callback = self.parse_song_url)
    def parse_song_url(self, response): 
        """
        Parses song page and yields dictionary of chords for each song. 
        Input is the song page from the first parse page. 
        Dictionary output contains bar number as key, and a tuple of (chord, bar length) for each value. 
        """
        self.driver.get(response.url)
        # wait for page to load 
        time.sleep(5)
        html = self.driver.page_source
        sel = Selector(text=html)
        
        # obtain song url 
        song_url = response.url
        # format song name by string slicing from url 
        start = song_url.rfind("/")
        end = len(song_url) - 7 
        song_title = song_url[start+1:end]
        # clean song name url 
        song_title = (song_title.replace('-', ' ')).title()

        # obtain chord elements for song 
        div = sel.css('div.s4xyh0t > div.chords')
        # obtain bar length 
        barlength = div.css('::attr(class)').re_first('barlength-(\d+)')
        tags_with_i_value = div.css('[data-i]')
        # create table of all results 
        table = [{'i-value': tag.css('::attr(data-i)').get(), 'data-handle': tag.css('::attr(data-handle)').get(), 'barlength': barlength} for tag in tags_with_i_value]
        # create dicionary output for each song by iterating through table 
        dict_of_chords = dict()
        for row in table: 
            i_value = row['i-value']
            chord = row['data-handle']
            barlength = row['barlength']
            dict_of_chords[i_value] = (chord, barlength) 
        # yield the result as a dictionary
        yield {
            'song_name': song_title,
            'song_url': song_url,
            'song_chords': dict_of_chords
            }

    def closed(self, reason):
        """
        Closes the web driver. 
        """
        # close webdriver 
        self.driver.quit()
        

