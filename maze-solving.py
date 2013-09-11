#!/usr/bin/python

"""
Maze Solving Robot (rapsberry pi + arduino)
"""

import cv2
import sys
import time
import math
import numpy as np

##
# Opens a video capture device with a resolution of 800x600 at 12 FPS.
##
def open_camera( cam_id = 0 ) :
	cap = cv2.VideoCapture( cam_id )
	cap.set( cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 600 );
	cap.set( cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 800 );
	cap.set( cv2.cv.CV_CAP_PROP_FPS, 12 );
	return cap

##
# Gets a frame from an open video device, or returns None
# if the capture could not be made.
##
def get_frame( device ) :
	ret, img = device.read()
	if( ret == False ) : # failed to capture
		#print >> sys.stderr, "Error capturing from video device."
		return None
	return img

##
# Closes all OpenCV windows and releases video capture device
# before exit.
##
def cleanup( cam_id = 0 ) : 
	cv2.destroyAllWindows()
	cv2.VideoCapture( cam_id ).release()

def count( threshold ) :
	width = 11
	height = 8
	size = 5
	threshold_level = 16
	for i in range( height ):
		o = '';
		for j in range( width ):
			crop_img = threshold[ i * size : ( i * size ) + size, j * size : ( j * size ) + size ]
			o += " %s " % ( ' ' if cv2.countNonZero( crop_img ) > threshold_level else 'X' )
		print o;
	return None

SIZE = 5
WIDTH = 11
HEIGHT = 8

########### Main Program ###########

start_time = time.time()

camera_id = 0
dev = open_camera( camera_id ) # open the camera as a video capture device

image = get_frame( dev ) # Get a frame from the camera
if image is None : # if we failed to capture (camera disconnected?)
	#image = cv2.imread( '1_calibration.jpg', cv2.cv.CV_LOAD_IMAGE_COLOR )
	image = cv2.imread( '2_calibration.jpg', cv2.cv.CV_LOAD_IMAGE_COLOR )

# Coordinates of quadrangle vertices in the source image.
#pts_src = np.float32( [ [ 56, 65 ], [ 368, 52 ], [ 28, 387 ], [ 389, 390 ] ] )
pts_src = np.float32( [ [ 69, 86 ], [ 710, 53 ], [ 82, 549 ], [ 728, 519 ] ] )

# Coordinates of the corresponding quadrangle vertices in the destination image.
pts_dst = np.float32( [ [  0,  0 ], [ ( WIDTH * SIZE ),  0 ], [  0, ( HEIGHT * SIZE ) ], [ ( WIDTH * SIZE ), ( HEIGHT * SIZE ) ] ] )

# Calculate the perspective transform from 4 pairs of the corresponding points.
matrix = cv2.getPerspectiveTransform( pts_src, pts_dst )
dst = cv2.warpPerspective( image, matrix, ( ( WIDTH * SIZE ), ( HEIGHT * SIZE ) ) )

img = cv2.cvtColor( dst, cv2.COLOR_BGR2GRAY )
img = cv2.medianBlur( img, 5 )
threshold = cv2.adaptiveThreshold( img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2 )

cv2.imwrite( '2_threshold.png', threshold )

count( threshold )

end_time = time.time() - start_time
print "time", end_time

cleanup( camera_id )
sys.exit()
