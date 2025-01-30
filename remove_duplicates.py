import os 
import stat
import hashlib 
from pathlib import Path 
 
file_path = "D:\Serum_Render\BASS_presets_filtered" 

list_of_files = os.walk(file_path) 
 
unique_files = dict() 

for root, folders, files in list_of_files: 

	# Running a for loop on all the files 
	for file in files: 

		# Finding complete file path 
		file_path = Path(os.path.join(root, file)) 

		# Converting all the content of 
		# our file into md5 hash. 
		Hash_file = hashlib.md5(open(file_path, 'rb').read()).hexdigest() 

		# If file hash has already
		# been added we'll simply delete that file 
		if Hash_file not in unique_files: 
			unique_files[Hash_file] = file_path 
		else:
			os.chmod(file_path, stat.S_IWRITE)
			os.remove(file_path)
			print(f"{file_path} has been deleted") 
