import scrapy 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapy.selector import Selector
from scrapy.http import Request

class chord_scraper(scrapy.Spider): 
    name = 'chord_scraper'
    
    def __init__(self, url_of_song, *args, **kwargs): 
        super().__init__(*args, **kwargs)  # don't forget to call the super's __init__
        if not url_of_song.startswith(('http://', 'https://')):
            url_of_song = 'http://' + url_of_song
        self.start_urls = [url_of_song]
        
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def parse(self, response):
        self.driver.get(response.url)
        
        # Wait for the page to load
        import time
        time.sleep(5)  # adjust this to a suitable value

        # Now you can access the HTML of the page
        html = self.driver.page_source
        sel = Selector(text=html)

        # Now you can use sel just like the response in your original parse method
        div = sel.css('div.s4xyh0t > div.chords')
        barlength = div.css('::attr(class)').re_first('barlength-(\d+)')
        tags_with_i_value = div.css('[data-i]')
        table = [{'i-value': tag.css('::attr(data-i)').get(), 'data-handle': tag.css('::attr(data-handle)').get(), 'barlength': barlength} for tag in tags_with_i_value]
        for row in table:
            yield row

    def closed(self, reason):
        self.driver.quit()


# import scrapy 
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from scrapy.selector import Selector
# from scrapy.http import Request

# class chord_scraper(scrapy.Spider): 
#     name = 'chord_scraper'
    
#     def __init__(self, url_of_song, *args, **kwargs): 
#         super().__init__(*args, **kwargs)  # call the super's __init__
        
#         # make sure the proper url was passed in. i was having issues with this earlier 
#         if not url_of_song.startswith(('http://', 'https://')):
#             url_of_song = 'http://' + url_of_song
#         self.start_urls = [url_of_song] # scrapy url 
#         self.driver = webdriver.Firefox() # using firefox for selenium 
        
#         options = Options()
#         options.headless = True # this will allow us to automatically close the window after 
#         #options.add_argument("--incognito") # enable incognito mode to bypass number of website limits allowed for a day 
#         self.driver = webdriver.Firefox(options=options)

#     def parse(self, response):
#         self.driver.get(response.url)
        
#         # Wait for the page to load, so that the chords load! 
#         import time
#         time.sleep(5)  # pause code for 5 seconds 

#         html = self.driver.page_source
#         sel = Selector(text=html)

#         # Now you can use sel just like the response how we did scrapy 
#         div = sel.css('div.s4xyh0t > div.chords')
#         barlength = div.css('::attr(class)').re_first('barlength-(\d+)')
#         yield {'hello': 'beginning'}
#         yield {'barlength': barlength}
#         yield {'hello': 'end'}
#         #tags_with_i_value = div.css('[data-i]')
#         #table = [{'i-value': tag.css('::attr(data-i)').get(), 'data-handle': tag.css('::attr(data-handle)').get(), 'barlength': barlength} for tag in tags_with_i_value]
#         #for row in table:
#             #yield row
#     def closed(self, reason):
#         self.driver.quit()

# import scrapy 

# class chord_scraper(scrapy.Spider): 
#     name = 'chord_scraper'
#     def __init__(self, url_of_song, *args, **kwargs): 
#         super().__init__(*args, **kwargs)  # don't forget to call the super's __init__
#         if not url_of_song.startswith(('http://', 'https://')):
#             url_of_song = 'http://' + url_of_song
#         self.start_urls = [url_of_song]
    
    
#     # def __init__(self, url_of_song, *args, **kwargs): 
#         # self.start_urls = url_of_song 
#     def parse(self, response):
#     # Select the div with the specific class
#         div = response.css('div.s4xyh0t > div.chords')

#         # Extract the barlength number
#         barlength = div.css('div.chords::attr(class)').re_first('barlength-(\d+)')

#         # Find all tags with an i-value inside this div
#         tags_with_i_value = div.css('[data-i]')

#         # Create a table (list of dictionaries)
#         table = [{'i-value': tag.css('::attr(data-i)').get(), 'data-handle': tag.css('::attr(data-handle)').get(), 'barlength': barlength} for tag in tags_with_i_value]

#         # Yield each row of the table as a dictionary
#         yield {'hello': 'beginning'}
#         yield {'hello': div.get()}
#         yield {'hello': 'end'}
#         #for row in table:
#             #yield row


