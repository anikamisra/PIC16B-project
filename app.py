from flask import Flask, render_template, request, redirect, url_for
from scrapy.crawler import CrawlerProcess
from chord_scraper import chord_scraper

app = Flask(__name__)

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# First scraper page route
@app.route('/scraper1', methods=['GET', 'POST'])
def scraper1():
    if request.method == 'POST':
        url = request.form['url']
        process = CrawlerProcess(settings={})
        process.crawl(chord_scraper, url_of_song=url)
        process.start()
        return redirect(url_for('index'))
    return render_template('scraper1.html')

# Second scraper page route
@app.route('/scraper2', methods=['GET', 'POST'])
def scraper2():
    if request.method == 'POST':
        artistname = request.form['artistname']
        process = CrawlerProcess(settings={})
        process.crawl(chord_scraper, artistname=artistname)
        process.start()
        return redirect(url_for('index'))
    return render_template('scraper2.html')

if __name__ == '__main__':
    app.run(debug=True)
