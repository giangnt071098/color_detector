import numpy as np
import matplotlib.pyplot as plt
i,j = 0,0
temp_r, temp_g, temp_b=0, 0,0
while(1):
	plt.xlim(i-0.01*150,i+0.01*50)
	f = open("data.txt", "r")
	dat = f.readlines()
	if len(dat)>0:
		data= dat[0][1:-1]
	f.close()
	value_RGB = [int(s) for s in data.split(', ') if s.isdigit()]
	if len(value_RGB)==3:
		plt.plot([i, i+0.01],[temp_r, value_RGB[0]], '-ro', marker = 'None')
		plt.plot([i, i+0.01],[temp_g, value_RGB[1]], '-go', marker = 'None')
		plt.plot([i, i+0.01],[temp_b, value_RGB[2]], '-bo', marker = 'None')
		plt.pause(0.05)
		i+= 0.01
		temp_r= value_RGB[0]
		temp_g= value_RGB[1]
		temp_b= value_RGB[2]
    

plt.show()