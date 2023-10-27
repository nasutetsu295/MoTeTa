import numpy as np
import cv2 as cv
from PIL import Image

#image
# image = np.array(
#     [ [0,0,   0,   0,   0,   0,   0,   0,   0,   0, 255,   0,   0,   0,   0,   0,  255,   0,0,0],
#       [0,0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,0,0],
#       [0,0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,0,0],
#       [0,0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,0,0],
#       [0,0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,0,0],
#       [0,0, 255, 255, 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255, 255,0,0],
#       [0,0, 255, 255, 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255, 255,0,0],
#       [0,0, 255, 255, 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255, 255,0,0],
#       [0,255, 255, 255, 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255, 255,0,0],
#       [0,0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,0,0],
#       [0,0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,0,0],
#       [0,0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,0,0],
#       [0,0,   0,   0,   0,   0,   0,   0,   0, 255,   0,   0,   0,   0,   0,   0,   0,   0,0,0],
#       [0,0,   0,   0,   0,   0,   0,   0, 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,0,0],      
#     ],
#     dtype = np.uint8
# )


image_O = cv.imread('real_H.jpg')

gray = cv.cvtColor(image_O, cv.COLOR_BGR2GRAY)
gray2 = gray.copy() 

change = Image.fromarray(np.uint8(gray))
image = np.asarray(change.resize((300, 300)))

image2 = cv.blur(gray2, (101,101))
# image[3,2] = 0

# width = image.shape[1]
# hight = image.shape[0]
# m, n = 0, 0

# while True:

#     if(n < 2 or n > 11):
#         image[n, m] = 0
#     elif(m < 2 or m > 17):
#         image[n,m] = 0
#     m = m + 1

#     if(m == width):
#         m = 0
#         n = n + 1
    
#     if(n == hight):
#         break


# contours, hierarchy = cv.findContours(image, cv.RETR_LIST, cv.CHAIN_APPROX_TC89_L1,)


#caculation of S
# for i, countor in enumerate(contours):
    
#     area = cv.contourArea(countor, True)
#     if(area < 0):
#         area = area * -1
    
#     print(f"面積[{i}]: {area}")


#color = cv.cvtColor(image, cv.COLOR_GRAY2BGR)


print(image_O.shape[0])
print(image_O.shape[1])
# print(image.shape[0])
# print(image.shape[1])
# print(type(color))
# print(type(image))

# for moji in contours:
#     x, y, w, h = cv.boundingRect(moji)
#     red = (0, 0, 255)
#     cv.rectangle(color, (x, y), (x+w-1, y+h-1), red, 1)

#cv.imshow("image", color)
cv.namedWindow('in_image', cv.WINDOW_NORMAL)
cv.namedWindow('out_image', cv.WINDOW_NORMAL)
cv.namedWindow('out_image2', cv.WINDOW_NORMAL)
cv.imshow('in_image', image_O)
cv.imshow('out_image', image)
cv.imshow('out_image2', image2)
cv.waitKey(0)
