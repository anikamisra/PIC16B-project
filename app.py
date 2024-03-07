from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scraper1', methods=['GET', 'POST'])
def scraper1():
    if request.method == 'POST':
        # Run scraper 1
        subprocess.run(['scrapy', 'crawl', 'chord_scraper', '-o', 'scraper1_output.csv', '-a', 'url_of_song=' + request.form['url']])
        return redirect(url_for('scraper1_result'))
    return render_template('scraper1.html')

@app.route('/scraper2', methods=['GET', 'POST'])
def scraper2():
    if request.method == 'POST':
        # Modify the user input for scraper command
        artist = request.form['artist'].lower().replace(' ', '')
        # Run scraper 2
        subprocess.run(['scrapy', 'crawl', 'chord_scraper', '-o', 'scraper2_output.csv', '-a', 'artistname=' + artist])
        return redirect(url_for('scraper2_result'))
    return render_template('scraper2.html')

@app.route('/scraper1/result')
def scraper1_result():
    # Read scraper 1 output file and display its contents
    with open('scraper1_output.csv', 'r') as file:
        result = file.read()
    return result

@app.route('/scraper2/result')
def scraper2_result():
    # Read scraper 2 output file and display its contents
    with open('scraper2_output.csv', 'r') as file:
        result = file.read()
    return result

if __name__ == '__main__':
    app.run(debug=True)
