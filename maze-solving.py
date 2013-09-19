#!/usr/bin/python

"""
Maze Solving Robot (rapsberry pi + arduino)
"""

import cv2
import sys
import math
import numpy as np

from AStarPathFinding import *

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
	
	game = AStarPathFinding()
	game.initMap( 12, 8, 0, 4, 11, 3 )
	
	width = 12
	height = 8
	size = 5
	threshold_level = 16
	for i in range( height ):
		o = '';
		for j in range( width ):
			crop_img = threshold[ i * size : ( i * size ) + size, j * size : ( j * size ) + size ]
			o += " %s " % ( ' ' if cv2.countNonZero( crop_img ) > threshold_level else 'X' )
			if cv2.countNonZero( crop_img ) <= threshold_level :
				game.drawWall( j, i )
		print o;
	
	game.findPath()
	game.drawMap()
	game.getCommands()
	
	return None

SIZE = 5
WIDTH = 12
HEIGHT = 8

########### Main Program ###########

camera_id = 0
dev = open_camera( camera_id ) # open the camera as a video capture device

image = get_frame( dev ) # Get a frame from the camera
if image is None : # if we failed to capture (camera disconnected?)
	image = cv2.imread( 'calibration5.jpg', cv2.cv.CV_LOAD_IMAGE_COLOR )

# Coordinates of quadrangle vertices in the source image.
pts_src = np.float32( [ [ 105, 96 ], [ 754, 97 ], [ 113, 520 ], [ 742, 522 ] ] )

# Coordinates of the corresponding quadrangle vertices in the destination image.
pts_dst = np.float32( [ [  0,  0 ], [ ( WIDTH * SIZE ),  0 ], [  0, ( HEIGHT * SIZE ) ], [ ( WIDTH * SIZE ), ( HEIGHT * SIZE ) ] ] )

# Calculate the perspective transform from 4 pairs of the corresponding points.
matrix = cv2.getPerspectiveTransform( pts_src, pts_dst )
dst = cv2.warpPerspective( image, matrix, ( ( WIDTH * SIZE ), ( HEIGHT * SIZE ) ) )

img = cv2.cvtColor( dst, cv2.COLOR_BGR2GRAY )
img = cv2.GaussianBlur( img, ( 5, 5 ), 0 )
ret,threshold = cv2.threshold( img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU )

cv2.imwrite( 'threshold.png', threshold )

count( threshold )

#cleanup( camera_id )
