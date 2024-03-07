from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import subprocess
import os

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

selected_line = ""

@app.route('/SearchWithArtist', methods=['GET', 'POST'])
def SearchWithArtist():
    if request.method == 'POST':
        # Modify the user input for scraper command
        artist = request.form['artist'].lower().replace(' ', '')
        # Run scraper 2
        subprocess.run(['scrapy', 'crawl', 'chord_scraper', '-o', 'results.csv', '-a', 'artistname=' + artist])
        # Read the contents of the result.csv file, skipping the first line
        result_file_path = os.path.join(os.getcwd(), 'chord_scraper', 'chord_scraper', 'results.csv')
        with open(result_file_path, 'r') as file:
            # Skip the first line
            next(file)
            # Read the rest of the lines
            result_data = file.readlines()
        return render_template('SearchWithArtist.html', result_data=result_data)
    return render_template('SearchWithArtist.html')


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
