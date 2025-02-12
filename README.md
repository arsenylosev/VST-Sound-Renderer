# VST Sound Renderer

This project is focused on the automatic render of sounds via VST plugins. Main objective: creation a one-shot sounds of virtual synthesizers that can be used for audio datasets.

## Render Launch

Please, note that this pipeline **works only on Windows machines**, it hasn't been tested on other platforms. You will need a proper setup of adjacent software to run, test and debug the pipeline.

### Required dependencies

* [Xfer Serum](https://xferrecords.com/products/serum) virtual synthesizer;
* [Miniconda](https://docs.anaconda.com/miniconda/install/#quick-command-line-install) environment manager for Python;
* [7Zip](https://www.7-zip.org) file archiver;
* DAW for testing the Serum via GUI that can support VST3 synthesizers.

Be cautious that this pipeline is oriented on working with Serum, but it can be implemented in other synths.

### Executing the commands

1. Ensure that all the dependencies are installed;
2. Open Miniconda prompt, navigate to the directory with scripts;
```cmd
cd your\path\to\Vst-Sound-Renderer
```
3. Install the Miniconda environment from `environment.yml` file:
```cmd
conda deactivate
conda env create -f environment.yml
```
4. Download your presets archive to the local drive, unpack it to the desired folder;
5. Activate your environment:
```cmd
conda activate midi2audio_byvst
```
6. Break down your presets folder into several subfolders *001*, *002*, etc.:
```cmd
python folder_splitter.py <your_folder>
```
7. Modify the `render_launch.bat` script for your needs. This script is just the useful way to send some macro-parameters to render engine. Here is the in-depth review of the script content:

```bat
python render_wav.py ^ & :: launching the render script
--plugin "C:\Program Files\Xfer\Serum\Serum_x64.dll" ^ &:: Path to Serum instance, .dll version is required
--note-duration 1.5 ^ & :: Note duration in seconds
--render-duration 3 ^ & :: File duration in seconds
--pitch-low 12 ^ & :: The lowest rendered note in midi
--pitch-step 12 ^ & :: The desired step between notes in semitones 
--pitch-high 84 ^ & :: The highest rendered note in midi
--preset-dir "" ^ & :: Path to the folder with presets
--output-dir "" & :: Path to the output directory for audio files
```

8. Archive the achieved files and send it to your cloud storage (Dropbox, for example);
9. Clear the `--output-dir` folder, change the `--preset-dir` folder to next folder (*001* to *002*, for example) and launch the `render_launch.bat` again for rendering next presets, repeat steps 7, 8 and 9 until all the presets are rendered.

## Existing scripts

**autorender_drafts.ipynb** ― raw sketch code for interacting with files: checking duplicates, filtering MP3-s from folders, etc.

**calculate_hashes.py** ― script for checking the duplicates in the file folder.

**folder_splitter.py** ― script for splitting the folder into several subfolders with the desired file quantity.

**remove_duplicates.py** ― script for removing the duplicated files based on the MD5 hash checking.

**render_launch.bat** ― batch script for launching the render and setting the initial parameters for files.

**render_wav.py** ― major script for render plugin presets into audio files. Detailed explanation of parameters is described below.

**serum_render_slow.py** ― old version of render script. Deprecated for now, uses single-threading, but some ideas can be useful in the future.
