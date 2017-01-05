'''**************************************************************************
*
* FILE: q1_image_filter.py
*
* BRIEF: Implements image filtering from from fast_filter.c
*
* USAGE EXAMPLE: Apply an edge detector
* $python q1_image_filter.py utah.bmp utah_edges.bmp 3 -1 -1 -1 -1 8 -1 -1 -1 -1
* 
* COMMAND-LINE ARGUMENTS:
*  1)                   Input filename (must be bmp format).
*  2)                   Output filename (will be bmp format).
*  3)                   Filter width (an odd integer).
*  4 to filter_width^2) The floating point weights that define the filter, 
*                       ordered left->right and top->bottom.
*                   
* AUTHOR: Anthony Ho 
* ID: 260501840
*
***************************************************************************'''
#!/usr/bin/python

import sys
import ctypes
import Image

def filterImage (file_in, file_out, width, weight):
	#reading input file and initialize output
	library = ctypes.cdll.LoadLibrary("fast_filter.so")
	image_in = Image.open(file_in)
	image_data = image_in.read()
	arrayType = ctypes.c_ubyte * len(image_data)
	image_data_c = arrayType(*image_data)
	image_data_out_c = arrayType(*image_data)

	#connecting to the c library
	library.doFiltering(image_data_c, weight, width, image_data_out_c)
	image_out = open(file_out, 'wb')
	image_out.write(image_data_out_c)
	image_in.close()
	image_out.close()


if __name__ == "__main__":
	file_in = sys.argv[1]
	file_out = sys.argv[2]
	#changing input into c compatible input
	width = ctypes.c_int(int(sys.argv[3]))
	filterWeight = []
	for ind in range( 4, len(sys.argv)):
		filterWeight.append(ctypes.c_float(float(sys.argv[ind])))
	weightFormat = ctypes.c_float * len(filterWeight)
	weight = weightFormat(*filterWeight)

	#initialize the library and start passing input
	filterImage(file_in, file_out, width, weight)






