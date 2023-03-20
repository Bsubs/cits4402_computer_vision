#Joo Kai Tay, 22489437, lab01, week 02
import cv2 
import numpy as np
import math
import matplotlib.pyplot as plt
from skimage import io, color
import scipy

#Read image
file_name = 'lego1.png' 
im = cv2.imread(file_name)

#Display image with file title
cv2.imshow(file_name, im)

#Convert image to greyscale and display
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
cv2.imshow(file_name + " in grayscale", gray)

# #Display histogram
# plt.hist(gray.ravel(), 256, [0, 256])
# plt.title('Greyscale histogram of ' + file_name)
# plt.show()

# #Threshold the image
# ret, bw = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)

# #Display black and white image
# plt.title(file_name + ' in black and white THRESHOLD_VALUE = 160')
# plt.imshow(bw, cmap='gray')
# plt.show()

# #Apply morphological operation of errosion and dilation

# #Get kernel used to perform the operations. In this case, a rectangle of size 3x3
# element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

# #Erode the image and display
# erosion = cv2.erode(bw, element)
# plt.title(file_name + ' with morphological operation of erosion')
# plt.imshow(erosion, cmap='gray')
# plt.show()

# #Dilate the image and display
# dilation = cv2.dilate(bw, element)
# plt.title(file_name + ' with morphological operation of dilation')
# plt.imshow(dilation, cmap='gray')
# plt.show()

# #Count and print the number of objects in the image
# L, num = scipy.ndimage.label(erosion, structure=np.ones((3,3)))
# print("Number of objects in " + file_name + " : " + str(num))

# waits for user to press any key
# (this is necessary to avoid Python kernel form crashing)
cv2.waitKey(0)
  
# closing all open windows
cv2.destroyAllWindows()