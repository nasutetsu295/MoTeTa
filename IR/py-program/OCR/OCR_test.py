import numpy as num
import cv2 as cv
import os

#print(os.getcwd())

#test H or S or U. we can select from our keybord.
while True:

    print("input H or S or U")
    want = input()

    if want == "H":
        image = cv.imread('robocup_H.png')
        break
    elif want == "S":
        image = cv.imread('robocup_S.png')
        break
    elif want == "U":
        image = cv.imread('robocup_U.png')
        break
    else:
        print("select H or S or U")


gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)    #convert BGR to GRAY

blur = cv.GaussianBlur(gray, (5, 5), 0)         #Gaussian-filter

thresh = cv.adaptiveThreshold(blur, 255, 1, 1, 91, 2)  #convert only 2 color(black or white) iamge


contours = cv.findContours(
    thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

for moji in contours:
    x, y, w, h = cv.boundingRect(moji)
    if h < 20: continue
    red = (0, 0, 255)
    cv.rectangle(image, (x, y), (x+w, y+h), red, 2)


#cv.imwrite('re-moji.png', image)


cv.imshow("image", thresh)
cv.waitKey(0)

