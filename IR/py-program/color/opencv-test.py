import cv2
import numpy as py

#print(cv2.__version__)


bgr = cv2.imread('red.jpg')                                 #assign bar image.jpg
hsv_image = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)            #convert BGR into HSV
bar2 = cv2.imread('jason-dent-IaF-D8R5HCA-unsplash.jpg')
hsv_image2 = cv2.cvtColor(bar2, cv2.COLOR_BGR2HSV)

lower_red = (0, 50, 50)  # 赤色の下限(H, S, V)          red's H = -10~20
upper_red = (16, 255, 255)  # 赤色の上限(H, S, V)
lower_red2 = (170, 50, 50)  # 赤色の下限(H, S, V)
upper_red2 = (179, 255, 255)  # 赤色の上限(H, S, V)

lower_yellow = (17, 50, 50)
upper_yellow = (34, 255, 255)

lower_green = (35, 50, 50)  # 緑色の下限(H, S, V)
upper_green = (70, 255, 255)  # 緑色の上限(H, S, V)


def check_color(hsv, lower_range, upper_range, color_name):     # print input color percentage
    mask = cv2.inRange(hsv, lower_range, upper_range)           # make mask of only white or black. white is color I want to know.
    color_pixels = cv2.countNonZero(mask)                       # count white pixels of mask
    total_pixels = mask.shape[0] * mask.shape[1]                # count all pixels of mask
    
    #if color is Red, the range of 170~179(-10~-1) + the other range of 0~20
    if color_name == "Red":
        red_mask = cv2.inRange(hsv, lower_red2, upper_red2)
        red_pixels = cv2.countNonZero(red_mask)
        color_pixels = color_pixels + red_pixels
        #print(color_pixls)
    
    color_percentage = (color_pixels / total_pixels) * 100      # caculation of color percentage
        
    print(f"{color_name}: {color_percentage:.2f}%")             # print color percentage. the 2nd decimal place by float.

# 色の判定を実行
check_color(hsv_image2, lower_red, upper_red, "Red")
check_color(hsv_image2, lower_yellow, upper_yellow, "Yellow")
check_color(hsv_image2, lower_green, upper_green, "Green")

#check_color(hsv_image2, lower_red, upper_red, "Red")
#check_color(hsv_image2, lower_red2, upper_red2, "Red2")
#check_color(hsv_image2, lower_green, upper_green, "Green")

#cv2.imshow("", bgr)
#cv2.waitKey(1000)
#cv2.destroyAllWindows()

