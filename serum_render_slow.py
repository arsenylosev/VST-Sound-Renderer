import os

from scipy.io import wavfile
import dawdreamer as daw
from tqdm import tqdm

SAMPLE_RATE = 44100
BUFFER_SIZE = 512
SERUM_PATH = r"D:\Serum_Render\Serum_x64.dll" # Place your Serum .dll here
PRESETS_FOLDER = r"D:\Serum_Render\bass_3\presets" # Place your Serum presets folder here
OUT_FOLDER = r"D:\Serum_Render\bass_3\wav" # Place the folder for your files here
NOTES_DICT = {
    "C0": 12,
    "C1": 24,
    "C2": 36,
    "C3": 48,
    "C4": 60,
    "C5": 72,
    "C6": 84
}

def get_filenames_and_paths(directory):
    path = os.path.abspath(directory)
    abspaths = [entry.path for entry in os.scandir(path) if entry.is_file()]
    return abspaths

def render_preset_in_notes(outpath):
    for note_c, note_num in zip(NOTES_DICT.keys(), NOTES_DICT.values()):
        serum.add_midi_note(note_num, 127, 0.0, 1.5) # arguments - note, velocity, start point, duration
        engine.load_graph([(serum, [])])
        engine.render(3.)
        audio = engine.get_audio()
        wavfile.write(f"{outpath}-{note_c}.wav", SAMPLE_RATE, audio.transpose())
        serum.clear_midi()

def render_presets(filepaths):
    for presetpath in tqdm(filepaths, desc="Rendering Serum presets:"):
        serum.load_preset(presetpath)
        presetname_orig = os.path.basename(presetpath)
        presetname = os.path.splitext(presetname_orig)[0]
        outpath = os.path.join(OUT_FOLDER, presetname)
        render_preset_in_notes(outpath)

if __name__ == "__main__":
    filepaths = get_filenames_and_paths(PRESETS_FOLDER)
    engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
    serum = engine.make_plugin_processor("serum", SERUM_PATH)
    render_presets(filepaths)