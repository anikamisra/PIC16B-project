from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask import jsonify
from flask_cors import CORS
import subprocess
import os
import difflib
from dotenv import load_dotenv
from .db import Database, User
from midiutil import MIDIFile
from mingus.core import chords
import ast
import pandas as pd
from pychord import Chord

app = Flask(__name__)
app.secret_key = os.urandom(24)

CORS(app, supports_credentials=True)
load_dotenv(".env")
database = Database(os.getenv("DB_PSWD"))

def musicpackage():

    OCTAVES = list(range(11))

    errors = {
        'error!!!'
    }

    ########
    # ATHENA THIS IS WHERE WE EDIT
    def read_csvpath_from_file():
        with open('config.txt', 'r') as file:
            for line in file:
                if line.startswith('csv_path'):
                    variable_value = line.split('=')[1].strip().strip('"')
                    return variable_value
        return None

    def read_index_from_file():
        with open('config.txt', 'r') as file:
            for line in file:
                if line.startswith('user_song'):
                    variable_value = line.split('=')[1].strip().strip('"')
                    return variable_value
        return None

    csvpath = read_csvpath_from_file()
    df = pd.read_csv(csvpath)
    df.head()
    df = pd.read_csv(csvpath)
    index = read_index_from_file()
    index = int(index)
    song_name = df.iloc[index, 0]
    chords_string = df.loc[df['song_name'] == song_name, 'song_chords'].values[0]
    # DONE WITH EDITS
    ###############
    NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    OCTAVES = list(range(11))
    NOTES_IN_OCTAVE = len(NOTES)

    chords = ast.literal_eval(chords_string)
    extracted_strings = []
    # iterate through dictionary values
    for key, value in chords.items():
        extracted_strings.append(value[0])  # Append the first element of the tuple
    # get barlength
    first_item = list(chords.keys())[0]
    bar_length = chords[first_item][1]

    # clean up webscraper code
    original_list = extracted_strings
    # Remove semicolons from each string
    cleaned_list = [s.replace(':', '') for s in original_list]

    def chords_to_notes(chord_list):
        """
        Given a list of chord names, returns a list of corresponding notes.
        """
        notes_list = []
        for chord_name in chord_list:
            if chord_name == 'N':
                # Handle the special case of a rest
                notes_list.append('')
            else:
                try:
                    chord = Chord(chord_name)
                    notes = chord.components()
                    # Filter out numeric indices (only keep strings)
                    notes = [note for note in notes if isinstance(note, str)]
                    notes_list.extend(notes)
                except ValueError:
                    # Handle invalid chord names gracefully
                    pass
        return notes_list

    chord_names = cleaned_list
    resulting_notes = chords_to_notes(chord_names)

    def swap_accidentals(note):
        if note == 'Db':
            return 'C#'
        if note == 'D#':
            return 'Eb'
        if note == 'E#':
            return 'F'
        if note == 'Gb':
            return 'F#'
        if note == 'G#':
            return 'Ab'
        if note == 'A#':
            return 'Bb'
        if note == 'B#':
            return 'C'

        return note

    def note_to_number(note: str, octave: int) -> int:
        note = swap_accidentals(note)
        assert note in NOTES, errors['notes']
        assert octave in OCTAVES, errors['notes']

        note = NOTES.index(note)
        note += (NOTES_IN_OCTAVE * octave)

        assert 0 <= note <= 127, errors['notes']

        return note

    chord_progression = resulting_notes
    i = 0

    chord_progression = [chord for chord in chord_progression if chord.strip() != '']
    print("chord progresion", chord_progression)
    array_of_notes = []
    for note in chord_progression:
        array_of_notes.append(note)
    print("array of notes", array_of_notes)
    print(type(chord_progression[0]))

    array_of_note_numbers = []
    for note in array_of_notes:
        OCTAVE = 4
        array_of_note_numbers.append(note_to_number(note, OCTAVE))

    track = 0
    channel = 0
    time = 0  # In beats
    duration = 1  # In beats
    tempo = 120 * int(bar_length)  # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i, pitch in enumerate(array_of_note_numbers):
        MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

    with open("chord_scraper/test.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
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
    musicpackage()
    # Provide the path to the file you want to serve
    file_path = 'chord_scraper/test.mid'
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
            new_df = df.iloc[:, :1].copy()
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
