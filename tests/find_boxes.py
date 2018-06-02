import cv2, sys

filename = sys.argv[1]

def threshold(im, method):
    # make it grayscale
    im_gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    if method == 'fixed':
        threshed_im = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY)

    elif method == 'mean':
        threshed_im = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 7)

    elif method == 'gaussian':
        threshed_im = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 12)

    else:
        return None

    return threshed_im


image = cv2.imread('screens/' + filename)

# threshold it
thresh = threshold(image, 'mean')
height,width,channels = image.shape
image_area = width*height
largest_area=image_area;
largest_contour_index=0
bounding_rect=0
# find contours
_, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
cnts=[]
for i in contours:
    cnt=i
    area = cv2.contourArea(cnt)
    (x,y,w,h) = cv2.boundingRect(cnt)
    if ((w > 1000 and w < 2000) and (h > 50 and h < 1000)):
        cnts.append(cnt)
    
cv2.drawContours(image, cnts, -1, (0, 255, 0), 10)
cv2.imwrite('screens/finished/output_' + filename, image)