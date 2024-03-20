from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask import jsonify
from flask_cors import CORS
import subprocess
import os
import difflib
from dotenv import load_dotenv
from .db import Database, User
import pandas as pd

app = Flask(__name__)
app.secret_key = os.urandom(24)

CORS(app, supports_credentials=True)
load_dotenv(".env")
database = Database(os.getenv("DB_PSWD"))

def write_variable_to_file(new_value):
    with open('config.txt', 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if line.startswith('csv_path'):
                file.write(f'csv_path = "{new_value}"\n')
            else:
                file.write(line)
        file.truncate()

def write_variable_to_file2(new_value):
    with open('config.txt', 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if line.startswith('user_song'):
                file.write(f'user_song = "{new_value}"\n')
            else:
                file.write(line)
        file.truncate()

def write_variable_to_file3(new_value):
    with open('config.txt', 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if line.startswith('result'):
                file.write(f'result = "{new_value}"\n')
            else:
                file.write(line)
        file.truncate()

def read_csvpath_from_file():
    with open('config.txt', 'r') as file:
        for line in file:
            if line.startswith('csv_path'):
                variable_value = line.split('=')[1].strip().strip('"')
                return variable_value
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if database.verify_user(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/createAccount', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if database.add_user(User(username, password)):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('create_account.html', error="Username already exists.")
    return render_template('create_account.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/SearchSong', methods=['GET', 'POST'])
def SearchSong():
    if request.method == 'POST':
        url = request.form['url']
        write_variable_to_file2(url)
    return render_template('SearchSong.html')

@app.route('/download')
def download_file():
    # Provide the path to the file you want to serve
    file_path = 'pure-edm-fire-arpeggio10.mid'
    # Send the file to the user for download
    return send_file(file_path)


@app.route('/SearchWithArtist', methods=['GET', 'POST'])
def SearchWithArtist():
    if request.method == 'POST':
        # Get the artist name from the form and format it properly
        artist = request.form['artist'].lower().replace(' ', '')
        # Search for the CSV file with the matching artist name
        csv_file_path = os.path.join(os.getcwd(), 'chord_scraper', artist + '.csv')
        if os.path.exists(csv_file_path):
            write_variable_to_file(csv_file_path)
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file_path)
            new_df = df.iloc[:, :2].copy()
            result_data = []
            for index, row in new_df.iterrows():
                result_data.append(row.tolist())
        else:
            # Find the first artist whose name starts with the same character as the input artist's name
            all_csv_files = [f[:-4] for f in os.listdir(os.path.join(os.getcwd(), 'chord_scraper')) if
                             f.endswith('.csv')]
            similar_artist = next((a for a in all_csv_files if a.startswith(artist[0])), None)
            if similar_artist:
                suggestion = similar_artist
                error_message = f"Couldn't find the artist in top 10. Did you mean {suggestion}?"
            else:
                error_message = "Couldn't find the artist in top 10. No similar artist found."
            return render_template('SearchWithArtist.html', error_message=error_message)
        return render_template('SearchWithArtist.html', result_data=result_data)
    return render_template('SearchWithArtist.html')


if __name__ == '__main__':
    app.run(debug=True)
