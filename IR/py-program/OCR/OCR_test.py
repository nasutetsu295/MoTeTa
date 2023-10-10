import numpy as np
import cv2 as cv
import os

#print(os.getcwd())

#test H or S or U. we can select from our keybord.
while True:

    print("input H or S or U")
    want = input()

    if want == "H":
        image = cv.imread('realW_H.jpg')
        break
    elif want == "S":
        image = cv.imread('realW_S.jpg')
        break
    elif want == "U":
        image = cv.imread('realW_U.jpg')
        break
    else:
        print("select H or S or U")


#Preprocess
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)    #convert BGR to GRAY

blur = cv.GaussianBlur(gray, (5, 5), 0)         #Gaussian-filter

#thresh = cv.adaptiveThreshold(blur, 255, 1, 1, 91, 2)  #convert only 2 color(black or white) iamge
A, thresh = cv.threshold(blur, 75, 255, cv.THRESH_BINARY_INV)


contours = cv.findContours(
    thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]


for i, countor in enumerate(contours):

    area = cv.contourArea(countor, True)
    if(area < 0):
        area = area * -1

    if area < 250000: continue         #if area is less than 500 pixel, Remove
    
    x, y, w, h = cv.boundingRect(countor)
    red = (0, 0, 255)
    cv.rectangle(image, (x, y), (x+w, y+h), red, 10)

    print(f"面積[{i}]: {area}")


#for moji in contours:
#    x, y, w, h = cv.boundingRect(moji)
#    if h < 20: continue
#    red = (0, 0, 255)
#    cv.rectangle(image, (x, y), (x+w, y+h), red, 2)



cv.imwrite('re-moji.png', image)
#print(image.shape)

cv.namedWindow('out_image', cv.WINDOW_NORMAL)
cv.namedWindow('in_image', cv.WINDOW_NORMAL)
#height = image.shape[0]
#width = image.shape[1]
#Rimage = cv.resize(image, (width/2, height/2))
cv.imshow('in_image', image)
cv.imshow('out_image', thresh)
cv.waitKey(0)
