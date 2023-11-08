import numpy as np
import cv2 as cv
import os
from PIL import Image

#print(os.getcwd())



#value
width = 300
hight = 300

blur_block = 5

Top_rate_thresh = 5
Bottom_rate_thresh = 5

TwoValue_thresh = 70

area_thresh = 1000



#test H or S or U. we can select from our keybord.
while True:

    print("input H or S or U")
    want = input()

    if want == "H":
        image_O = cv.imread('IMG_H.jpg')
        break
    elif want == "S":
        image_O = cv.imread('IMG_S.jpg')
        break
    elif want == "U":
        image_O = cv.imread('IMG_U.jpg')
        break
    else:
        print(" you can't select it.")

#print(type(image))     #for debug. this code is for <class 'numpy.ndarray'>

change = Image.fromarray(np.uint8(image_O))      #change small size of image
image_D = np.asarray(change.resize((width, hight)))


#become 0 without inside of square

def mksquare(im, x, y, w, h):   #(image, X_origin of square, y_origin of square, width of square, hight of square)

    width = im.shape[1]
    hight = im.shape[0]
    m, n = 0, 0

    while True:

        if(n < y or n > y+h ):
            im[n, m] = 0
        elif(m < x or m > x+w):
            im[n,m] = 0
        
        m = m + 1

        if(m == width):
            m = 0
            n = n + 1
    
        if(n == hight):
            break

    return im




#(< Preprocess >)

gray = cv.cvtColor(image_O, cv.COLOR_BGR2GRAY)    #convert BGR into GRAY

# blur = cv.GaussianBlur(gray, (5,5), 0)         #Gaussian-filter
change = Image.fromarray(np.uint8(gray))      #change small size of image
resize = np.asarray(change.resize((width, hight)))
blur = cv.blur(resize, (blur_block, blur_block))

#thresh = cv.adaptiveThreshold(blur, 255, 1, 1, 91, 2)  #convert only 2 color(black or white) iamge
A, thresh = cv.threshold(blur, TwoValue_thresh, 255, cv.THRESH_BINARY_INV)



#(< recognize >)

contours = cv.findContours(
    thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]


for i, countor in enumerate(contours):

    area = cv.contourArea(countor, True)
    if(area < 0):
        area = area * -1

    if area < area_thresh: continue         #if area is less than area_thresh pixel, Remove

    x, y, w, h = cv.boundingRect(countor)
    red = (0, 0, 255)
    cv.rectangle(image_D, (x, y), (x+w, y+h), red, 3)

    # print(f"面積[{i}]: {area}")



Top = thresh.copy()     # this is copy, not refer. a copy is different from origin (of memory).
Bottom = thresh.copy()

#width,hight of square(mksquare)
Top_W = w/3
Top_H = h/3
Bottom_W = w/3
Bottom_H = h/3

# if w < h:

#     mksquare(Top, x+w/3, y, Top_W, Top_H)               # make mask of top region of the letter 
#     mksquare(Bottom,x+w/3, y+2*h/3, Bottom_W, Bottom_H) # make mask of bottom region of the letter

# else:

#     mksquare(Top, x, y+h/3, Top_W, Top_H)               # make mask of top region of the letter 
#     mksquare(Bottom,x+2*w/3, y+h/3, Bottom_W, Bottom_H) # make mask of bottom region of the letter

mksquare(Top, x, y+h/3, Top_W, Top_H)               # make mask of top region of the letter 
mksquare(Bottom,x+2*w/3, y+h/3, Bottom_W, Bottom_H) # make mask of bottom region of the letter

Top_rate = cv.countNonZero(Top) / (Top_W * Top_H) * 100                 # get area percentage of top region of the letter
Bottom_rate = cv.countNonZero(Bottom) / (Bottom_W * Bottom_H) * 100     # get area percentage of bottom region of the letter


if (Top_rate < Top_rate_thresh):          # if Top_rate is less than 5%, the picture is H or U. But, if not, the picture is S

    if(Bottom_rate < Bottom_rate_thresh):    # if Bottom rate is less than 5%, the picture is H. But , if not, the picture is U
        letter = "H"
    
    else:
        letter = "U"
    
else:
    letter = "S"



cv.imwrite('re-moji.png', image_O)

cv.namedWindow('in_image', cv.WINDOW_NORMAL)
cv.namedWindow('out_imageO', cv.WINDOW_NORMAL)
cv.namedWindow('out_imageT', cv.WINDOW_NORMAL)
cv.namedWindow('out_imageB', cv.WINDOW_NORMAL)

cv.imshow('in_image', image_D)
cv.imshow('out_imageO', thresh)
cv.imshow('out_imageT', Top)
cv.imshow('out_imageB', Bottom)

# print(thresh.shape[0]," ",image_O.shape[0])
# print(thresh.shape[1]," ",image_O.shape[1])
print(Top_rate)
print(Bottom_rate)
print(letter)

cv.waitKey(0)