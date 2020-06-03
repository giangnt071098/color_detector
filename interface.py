import serial
import cv2
import numpy as np
color = np.ones((100,100,3), dtype=np.uint8)

ser = serial.Serial()
ser.port = 'COM9'
ser.baurate = 9600
ser.open()

while(1):
	line = ser.readline()
	line = line.strip().decode('utf-8')
	print(line)
	if len(line) > 20:
		value_RGB = [int(s) for s in line.split() if s.isdigit()]
		print(value_RGB)
		value_RGB[0], value_RGB[2] = value_RGB[2], value_RGB[0]
		if (len(value_RGB) ==3):
			color_predict= color*np.array(value_RGB, dtype=np.uint8)
			cv2.imshow('image', color_predict)
			cv2.waitKey(1000)