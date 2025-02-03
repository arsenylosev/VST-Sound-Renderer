# VST Sound Renderer

This project is focused on the automatic render of sounds via VST plugins. Main objective: creation a one-shot sounds of virtual synthesizers that can be used for audio datasets.

## Existing scripts

**autorender_drafts.ipynb** ― raw sketch code for interacting with files: checking duplicates, filtering MP3-s from folders, etc.

**calculate_hashes.py** ― script for checking the duplicates in the file folder.

**folder_splitter.py** ― script for splitting the folder into several subfolders with the desired file quantity.

**remove_duplicates.py** ― script for removing the duplicated files based on the MD5 hash checking.

**render_launch.bat** ― batch script for launching the render and setting the initial parameters for files.

**render_wav.py** ― major script for render plugin presets into audio files. Detailed explanation of parameters is described below.

**serum_render_slow.py** ― old version of render script. Deprecated for now, uses single-threading, but some ideas can be useful in the future.