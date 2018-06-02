import cv2

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

def remove_noise_and_background(image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # check to see if we should apply thresholding to preprocess the image
  gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  gray = cv2.medianBlur(gray, 3)

  return gray

def get_largest_contour(contours, image_area):
  largest_contour=[]
  largest_area=0
  for i in contours:
    cnt=i
    area = cv2.contourArea(cnt)
    if (area > largest_area and area < (image_area - 20000)):
        largest_area=area
        largest_contour=cnt

  return largest_contour

def get_inner_boxes(image):
  height,width,channels = image.shape
  image_area = width*height
  largest_area=image_area;
  bounding_rect=0
  # find contours
  _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
  detectedBoxes=[]
  detectedAreas=[]
  for i in contours:
      cnt=i
      area = cv2.contourArea(cnt)
      boundingArea = cv2.boundingRect(cnt)
      (x,y,w,h) = boundingArea
      if ((w > 1000 and w < 2000) and (h > 50 and h < 1000)):
          detectedAreas.append(boundingArea)
          detectedBoxes.append(image[y:y+h,x:x+w])
      
  return (detectedBoxes, boundingArea)

# read original image
image = cv2.imread('screen.jpg')

noiseRemovedImage = remove_noise_and_background(image)

# threshold it
thresh = threshold(noiseRemovedImage, 'mean')
height,width,channels = image.shape
image_area = width*height

# find contours
_, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)


largest_contour = get_largest_contour(contours, image_area)
# Get the bounding rectangle by that largest box/contour
x,y,w,h = cv2.boundingRect(largest_contour)

#Screen name portion will be above big rectangle
screenName = noiseRemovedImage[0:y,0:width]
#screen actions portion will be below big rectangle
actions = noiseRemovedImage[y+h:height, 0:width]
#that box will be screen itself and we take it out
outputImage = image[y:y+h,x:x+w]
outputScreenWithoutNoise = noiseRemovedImage[y:y+h,x:x+w]

get_inner_boxes(outputScreenWithoutNoise)

# Save the output image/screen
cv2.imwrite('output.jpg', outputImage)

