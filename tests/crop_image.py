import numpy as np
import cv2
import sys

filename = sys.argv[1]

image = cv2.imread('images/' + filename)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
# check to see if we should apply thresholding to preprocess the
# image
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 
gray = cv2.medianBlur(gray, 3)

image = gray

height,width = image.shape
image_area = width*height
largest_area=0;
largest_contour_index=0
bounding_rect=0

# find contours
_, contours, hierarchy = cv2.findContours(image.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
cnts=[]
for i in contours:
    cnt=i
    area = cv2.contourArea(cnt)
    if (area>largest_area and area < (image_area - 20000)):
        largest_area=area
        largest_contour_index=i
        bounding_rect=cnt

x,y,w,h = cv2.boundingRect(bounding_rect)

screenName = image[0:y,0:width]
actions = image[y+h:height, 0:width]
out = image[y:y+h,x:x+w]

# Show the output image
cv2.imwrite('screens/screen_' + filename, out)
cv2.imwrite('boundaries/actions_' + filename, actions)
cv2.imwrite('boundaries/screen_name_' + filename, screenName)