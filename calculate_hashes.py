import os
import hashlib
from collections import Counter

from tqdm import tqdm

PRESETS_FOLDER = r"D:\Serum_Render\Data\Batch 4 - Presets 0-50k"

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_filenames_and_paths(directory):
    path = os.path.abspath(directory)
    abspaths = [entry.path for entry in os.scandir(path) if entry.is_file()]
    return abspaths

if __name__ == "__main__":
    files = get_filenames_and_paths(PRESETS_FOLDER)
    file_hashes = []
    for file in tqdm(files, desc="Calculating hashes for files"):
        checksum = md5(file)
        file_hashes.append(checksum)
    count_files = Counter(file_hashes)
    duplicates = [sum for sum, number in count_files.items() if number > 1]
    if duplicates == []:
        print("No duplicates found!")
    else:
        print(f"Found {len(duplicates)} duplicates!")
        print(f"The duplication of files is {round(len(duplicates) / len(file_hashes) * 100, 2)}%!")
