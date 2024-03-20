from midiutil import MIDIFile
from mingus.core import chords
import ast
import pandas as pd
from pychord import Chord


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
tempo = 120*int(bar_length)  # In BPM
volume = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
# automatically)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(array_of_note_numbers):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

with open("chord_scraper/test.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)