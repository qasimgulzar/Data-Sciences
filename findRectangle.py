import cv2
import numpy as np

img = cv2.imread('output/car - 2.jpg')
gray_im = cv2.imread('output/car - 2.jpg',0)
gray = cv2.bitwise_not(gray_im)
ret,thresh = cv2.threshold(gray,127,255,1)

(_,contours,_) = cv2.findContours(
    thresh.copy(),
    cv2.RETR_LIST,
    cv2.CHAIN_APPROX_SIMPLE
)
index=0
for cnt in contours:
    (x, y, w, h) = cv2.boundingRect(cnt)
    # if float(h)/float(w) > 0.5 and float(h)/float(w) < .7:
    if w*h > 350 and w*h < 2908:
        index+=1
        cv2.drawContours(gray,cnt,-1,(255,255,255),3)
        roi = img[y:y+h, x:x+w]
        cv2.imwrite("output/rectangles/" + "rect - " + str(index) + '.jpg', roi)
        print("%s x %s"%(w, h),float(h)/float(w))


img = cv2.imread('output/rectangles/rect - 3.jpg',0)
gray = cv2.bitwise_not(img)
cv2.imwrite("output/rectangles/" + "black-rect - " + str(index) + '.jpg', gray)
cv2.imshow('img',gray)
cv2.waitKey(0)
cv2.destroyAllWindows()