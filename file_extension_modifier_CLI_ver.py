#! /usr/bin/env python3

import img2pdf
import os
from PyPDF2 import PdfReader
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
					files_counter += convert_to_pdf(element, old, new)
				elif old == '.pdf':
					files_counter += convert_to_img(element, new)
				else:
					files_counter += modify_extension(element, old, new)

		print_summary(file_path, files_counter, old, new)
	return files_counter


def convert_to_pdf(element, old, new):
    # NOTE: conversion will be unsuccessful for broken files
    filename = element.path
    root, ext = os.path.splitext(filename)

    if ext.lower() != old:
        return 0

    try:
        # Open the image file
        image = Image.open(filename)
        pdf_bytes = img2pdf.convert(image.filename)

        # Save as PDF
        pdf_filename = root + new
        with open(pdf_filename, "wb") as f:
            f.write(pdf_bytes)
        print(f"Converted {filename} to {pdf_filename}")
        return 1
    except Exception as e:
        print(f"Error converting {filename} to PDF: {e}")
        return 0

def convert_to_img(element, new):
    filename = element.path
    root, ext = os.path.splitext(filename)

    # must skip if given element is not a pdf
    if ext.lower() != ".pdf":
        return 0

    try:
        reader = PdfReader(filename)
    except Exception as e:
        print(f"Error reading PDF {filename}: {e}")
        return 0

    page = reader.pages[0]

    for image_file_object in page.images:
        with open(root + new, "wb") as fp:
            fp.write(image_file_object.data)
    
    return 1

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
		