#! /usr/bin/env python3

import img2pdf
import os
import PyPDF2
from PIL import Image
import sys

def type_converter(file_path, old, new):
	# start by assuming user will input extensions that actually exist
	if old == new:
		print('The current file extension is equal to the new extension')
		return

	files_counter = 0 # TODO: determine what to do with this

	# if not pdf, simply modiying the file name is sufficient
	
	with os.scandir(file_path) as files_and_folders:
		for element in files_and_folders:
			if element.is_file():
				# if pdf, must do the conversion differently
				if new == '.pdf':
					files_counter += convert_to_pdf(element)
				elif old == '.pdf':
					# TODO: call convert_to_img
					return # TODO: delete
				else:
					files_counter += modify_extension(element, old, new)

		print_summary(file_path, files_counter, old, new)
	return files_counter


def convert_to_pdf(img):
	# TODO: handle case when new == .pdf
	with Image.open(img) as image:
		success_modif = 0
		# convert image to pdf
		pdf = img2pdf.convert(image.filename)
		with open(f"/Users/hajinjang/Downloads/Airdrop/{image.filename}.pdf", "wb") as file:
			if (file.write(pdf) > 0):
				success_modif = 1
		return success_modif

def convert_to_img():
	# TODO: handle case when old == .pdf

def modify_extension(element, old, new):
	success_modif = 0
	root, ext = os.path.splitext(element.path)
	if ext == old:
		new_path = root + new
		os.rename(element.path, new_path)
		success_modif = 1
	return success_modif

def print_summary(file_path, files_counter, old, new):
	print('** SUMMARY **')
	print()
	print('File path used: {}'.format(file_path))
	print()
	print('Old extension: {}'.format(old))
	print('New extension: {}'.format(new))
	print()
	print('Number of files processed: {}'.format(files_counter))


if __name__ == "__main__":
	path = r'/Users/hajinjang/Downloads/Airdrop'
	if len(sys.argv) > 2: # since we need old and new extensions
		type_converter(path, '.'+sys.argv[1], '.'+sys.argv[2])
	else:
		print('Please provide the old and new file extensions, separated by a space')
