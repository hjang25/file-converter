#! /usr/bin/env python3

import os

path = r'/Users/hajinjang/Downloads/Airdrop'

print()
print('Path: {}'.format(path))
print()
old_extension = '.' + input('Enter the old file extension (e.g. txt, mp3, etc.) --> ')
new_extension = '.' + input('Enter the new extension --> ')
print()

files_counter = 0

with os.scandir(path) as files_and_folders:
	for element in files_and_folders:
		if element.is_file():
			# multiple assignments
			#splitext splits path name into (root, ext) tuple
			root, ext = os.path.splitext(element.path) 
			if ext == old_extension:
				new_path = root + new_extension
				os.rename(element.path, new_path)
				files_counter += 1

print('** Summary **')
print()
print('# of files processed: {}'.format(files_counter))
print('Extension was modified from {} to {}'.format(old_extension, new_extension))


