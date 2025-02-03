@echo off
for /d %%B in (D:\Serum_Render\Data\Batch_4_presets\*) do (
    python render_wav.py ^
    --plugin "C:\Program Files\Xfer\Serum\Serum_x64.dll" ^
    --note-duration 1.5 ^
    --render-duration 3 ^
    --pitch-low 12 ^
    --pitch-step 12 ^
    --pitch-high 84 ^
    --preset-dir "%%B" ^
    --output-dir "C:\Temp_Storage"

    python dropbox_upload.py --yes Batch_4 C:\Temp_Storage
    for /r %%f in (C:\Temp_Storage\*) do rm %%f
)