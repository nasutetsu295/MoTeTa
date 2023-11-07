import cv2 as cv
import numpy as np
import serial
import time
from PIL import Image


ser = serial.Serial('/dev/ttyAMA0', 9600, timeout = 1.0)


cap = cv.VideoCapture(2)



lower_red = (0, 50, 50)  # 赤色の下限(H, S, V)          red's H = -10~20
upper_red = (14, 255, 255)  # 赤色の上限(H, S, V)
lower_red2 = (170, 50, 50)  # 赤色の下限(H, S, V)
upper_red2 = (179, 255, 255)  # 赤色の上限(H, S, V)

lower_yellow = (15, 50, 50)
upper_yellow = (34, 255, 255)

lower_green = (35, 50, 50)  # 緑色の下限(H, S, V)
upper_green = (85, 255, 255)  # 緑色の上限(H, S, V)



#value

width = 300
hight = 300

blur_block = 3

avaliable = 0                       #avaliable == 1 --> there is letter in frame.

Top_rate_thresh = 5
Bottom_rate_thresh = 5

TwoValue_thresh = 75

area_thresh = 1000

judge = 20                               #If the most color percentage(%) is more than judge, send color to M5
color :int = 0



def check_color(hsv, lower_range, upper_range, color_name):     # print input color percentage
    mask = cv.inRange(hsv, lower_range, upper_range)           # make mask of only white or black. white is color I want to know.
    color_pixels = cv.countNonZero(mask)                       # count white pixels of mask
    total_pixels = mask.shape[0] * mask.shape[1]                # count all pixels of mask
        
    #if color is Red, the range of 170~179(-10~-1) + the other range of 0~20
    if color_name == "Red":
        red_mask = cv.inRange(hsv, lower_red2, upper_red2)
        red_pixels = cv.countNonZero(red_mask)
        color_pixels = color_pixels + red_pixels
        #print(color_pixls)
        
    color_percentage = (color_pixels / total_pixels) * 100      # caculation of color percentage
    
    
    #    print(f"{color_name}: {color_percentage:.2f}%")             # print color percentage. the 2nd decimal place by float.
    return color_percentage



def mksquare(im, x, y, w, h):   #become 0 without inside of square  :  (image, X_origin of square, y_origin of square, width of square, hight of square)

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



# (< loop >)-------------------------------------------------------------------------------------------------------------------------------------------
while True:



    ret, frame = cap.read()
    
    if not ret:
        break
    
    

    #(< Preprocess >)

    change = Image.fromarray(np.uint8(frame))      #change small size of image
    resize = np.asarray(change.resize((width, hight)))
    
    hsv_frame = cv.cvtColor(resize, cv.COLOR_BGR2HSV)           #convert BGR into HSV
    
    gray = cv.cvtColor(resize, cv.COLOR_BGR2GRAY)    #convert BGR into GRAY
    blur = cv.blur(gray, (blur_block, blur_block))
    A, thresh = cv.threshold(blur, TwoValue_thresh, 255, cv.THRESH_BINARY_INV)



    #(< 色の判定を実行 >)
    
    R = check_color(hsv_frame, lower_red, upper_red, "Red")
    Y = check_color(hsv_frame, lower_yellow, upper_yellow, "Yellow")
    G = check_color(hsv_frame, lower_green, upper_green, "Green")
    
    
    #comfirm the most color
    
    if (R > Y and R > G):   #Red is the most
        mount = R
        color = 1
    elif (Y > G):           #yellow is the most
        mount = Y
        color = 2
    else:                   #green is the most
        mount = G
        color = 3
    
    
    
    #(< recognize >)
        
    contours = cv.findContours(
        thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

    
    avaliable = 0
    for i, countor in enumerate(contours):

        area = cv.contourArea(countor, True)
        if(area < 0):
            area = area * -1

        if area < area_thresh: continue         #if area is less than area_thresh pixel, Remove
        
        avaliable = 1
        x, y, w, h = cv.boundingRect(countor)
        
        red = (0, 0, 255)
        cv.rectangle(resize, (x, y), (x+w, y+h), red, 2)
    
    
    if avaliable == 1:

        Top = thresh.copy()     # this is copy, not refer. a copy is different from origin (of memory).
        Bottom = thresh.copy()


        #width,hight of square(mksquare)
        Top_W = w/3
        Top_H = h/3
        Bottom_W = w/3
        Bottom_H = h/3


        mksquare(Top, x+w/3, y, Top_W, Top_H)               # make mask of top region of the letter 
        mksquare(Bottom,x+w/3, y+2*h/3, Bottom_W, Bottom_H) # make mask of bottom region of the letter

        Top_rate = cv.countNonZero(Top) / (Top_W * Top_H) * 100                 # get area percentage of top region of the letter
        Bottom_rate = cv.countNonZero(Bottom) / (Bottom_W * Bottom_H) * 100     # get area percentage of bottom region of the letter


        if (Top_rate < Top_rate_thresh):            # if Top_rate is nothing, the picture is H or U. But, if not, the picture is U(inverted)x or S.

            if(Bottom_rate < Bottom_rate_thresh):    # if Bottom rate is nothing, the picture is H. But , if not, the picture is U
                letter = "H"
    
            else:
                letter = "U"
                
        else:
            
            if (Bottom_rate < Bottom_rate_thresh):  # if Bottom rate is nothing, the picture is U(inverted). But , if not, the picture is S
                letter = "U"

            else:
                letter = "S"
            

    else:
        letter = "none"
        Top_rate = "none"
        Bottom_rate = "none"



    #If the most color is large, connect to M5
    if (mount >= judge):
        ser.write(color)
        print("color : ", color)
        
    else:
        print("color : ", 0)
        ser.write(0)              #neither the three color in camera
    
    
    print("Top rate : ", Top_rate)
    print("Bottom rate : ", Bottom_rate)
    print(letter)
    
    cv.imshow("thresh_frame", thresh)
    cv.imshow("bgr_frame", resize)
    
    key = cv.waitKey(2)
    
    # Escキーを入力されたら画面を閉じる
    if key == 27:
        break

cap.release()

cv.destroyAllWindows()


ser.close()

