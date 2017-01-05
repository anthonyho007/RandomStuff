'''**************************************************************************
*
* FILE: q3_cgi_filter.py
*
* BRIEF: Implements load, filter, undo, redo function to the filtering program
*
* USAGE EXAMPLE: 
* 4 cases with different COMMAND
*
* $python q2_filter_with_history.py load <input_image_path>
* $python q2_filter_with_history.py load Mars.bmp
*
* $python q2_filter_with_history.py filter <filter_width> <filter_weights>
* $python q2_filter_with_history.py filter 3 -1 -1 -1 -1 8 -1 -1 -1 -1
*
* $python q2_filter_with_history.py undo 
*
* $python q2_filter_with_history.py redo 
*
* 
* Comments:
* in order to perform any operation a bmp need to be load first 
* can only restore changes up to one step forward or backward
* all results will be save to the result.bmp
*                   
* AUTHOR: Anthony Ho 
* ID: 260501840
*
***************************************************************************'''

import struct
import copy
import cgitb; cgitb.enable()
import cgi
import sys
import ctypes
import Image
import pickle
import os

class History:
	def __init__(self, image, undo, redo):
		self.image = image
		self.undo = undo
		self.redo = redo
	def is_undo (self):
		return self.undo
	def is_redo (self):
		return self.redo
	def get_image(self):
		return self.image


def loadImage ( image_in):
	#load image and save it in result.bmp
	image_data = image_in.read()
	imageType = ctypes.c_ubyte * len(image_data)
	image_data_in_c = (imageType).from_buffer_copy(image_data)
	image_out = open(active, 'wb')
	image_out.write(image_data_in_c)
	image_out.close()
	image_in.close()
	# overwrite any previous history
	open(history, 'w').close()


def filterImage ( weight, width):
	library = ctypes.cdll.LoadLibrary("fast_filter.so")
	# reading image
	image_in = open(active, 'r+')
	image_data = image_in.read()
	imageType = ctypes.c_ubyte * len(image_data)
	image_data_in_c = (imageType).from_buffer_copy(image_data)
	image_data_out_c = (imageType).from_buffer_copy(image_data)
	image_in.close()

	# writing image into pickle file
	temp = open(history, 'wb')
	cacheObj = History( image_data_in_c, False, False)
	pickle.dump(cacheObj, temp)
	temp.close()

	# initialize filtering process
	library.doFiltering(image_data_in_c, weight, width, image_data_out_c)
	image_out = open(active, 'wb')
	image_out.write(image_data_out_c)
	image_out.close()



if __name__ == "__main__":

	#starting the cgi socket
	print "Content-type: text/html"
	# parse query
	form = cgi.FieldStorage()

	if form.has_key('photo'):
		img_in = form['photo'].file





	# predefined params
	active = "result.bmp"
	history = "history.pickle"

	# check for which command to be perform 

	# case 1 loading of the bmp
	if form.getvalue("Load"):
		if not form.has_key('photo'):
			print "Please upload a picture"
		else: 
		# perform save opertation and pickling 
		file_in = form['photo'].file
		loadImage (file_in)


	elif form.getvalue("Redo"):

		#perform undo openration
		if os.stat(history).st_size != 0:
			temp = open(history, 'r+')
			cacheObj = pickle.load(temp)
			temp.close()
			if not cacheObj.is_undo():
				# get current active bmp and replace with cache
				active_image = open(active, 'wb')
				past_image = active_image.read()
				new_cacheObj = History( past_image, True, False)
				active_image.write(cacheObj.get_image())
				active_image.close()
				# write new cache 
				temp = open(history, 'wb')
				pickle.dump(new_cacheObj, temp)
				temp.close()


			else: 
				print "You cant undo from this point"

		else: 
			print "There is not changes yet"

	elif form.getvalue("Undo"):

		#perform undo openration
		if os.stat(history).st_size != 0:
			temp = open(history, 'r+')
			cacheObj = pickle.load(temp)
			temp.close()
			if not cacheObj.is_redo():
				# get current active bmp and replace with cache
				active_image = open(active, 'wb')
				past_image = active_image.read()
				new_cacheObj = History( past_image, False, True)
				active_image.write(cacheObj.get_image())
				active_image.close()
				# write new cache 
				temp = open(history, 'wb')
				pickle.dump(new_cacheObj, temp)
				temp.close()


			else: 
				print "You cant redo from this point"

		else: 
			print "There is not changes yet"

	elif sys.argv[1] == "filter":
		#perform filtering operation
		# initializing params for c 
		width = ctypes.c_int(int(sys.argv[2]))
		filterWeight = []
		for ind in range(3, len(sys.argv)):
			filterWeight.append(ctypes.c_float(float(sys.argv[ind])))
		weightType = ctypes.c_float * len(filterWeight)
		weight = weightType( * filterWeight)
		# start filtering 
		filterImage ( weight, width)


	else:
		print " please enter a valid command"
	print """
	<html>
	<body>
	<form name="input" action="./cgi-bin/q3_cgi_filter.py" method="post" enctype="multipart/form-data">

	  <p>Photo to Upload: <input type="file" name="photo" /></p>
	  <p>First Filter to Apply:</p>
	  <p><input type="text" name="00" value="1"> <input type="text" name="01" value="1"> <input type="text" name="02"  value="1"> </p>
	  <p><input type="text" name="10" value="1"> <input type="text" name="11" value="-7"> <input type="text" name="12" value="1"> </p>
	  <p><input type="text" name="20" value="1"> <input type="text" name="21"  value="1"> <input type="text" name="22" value="1"> </p>
	  <input type="submit" value="Load" name="load">
	  <input type="submit" value="Filter" name="filter">
	  <input type="submit" value="Undo" name="undo">
	  <input type="submit" value="Redo" name="redo">
	</form>
	<img src="result.bmp"/>
	</body>
	</html>