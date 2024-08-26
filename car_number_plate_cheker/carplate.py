# -*- coding: utf-8 -*-
"""carplate.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1d2ms-4P1FVxCtZbiNZuEKMPkLwDewnaR
"""

!nvcc --version

!pip install easyocr

!pip install imutils

!pip install opencv-python-headless==4.1.2.30

!pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

!pip install matplotlib

import easyocr
import cv2
from matplotlib import pyplot as plt
import imutils
import numpy as np

img = cv2.imread("/content/WhatsApp Image 2024-08-23 at 12.23.08_3ca5120f.jpg")
grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
plt.imshow(cv2.cvtColor(grey,cv2.COLOR_BGR2RGB))

bfilter = cv2.bilateralFilter(grey, 11, 17, 17) #Noise reduction
edged = cv2.Canny(bfilter, 30, 200) #Edge detection
plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break
print(location)

mask = np.zeros(grey.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], 0,255, -1)
new_image = cv2.bitwise_and(img, img, mask=mask)
#

plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

(x,y) = np.where(mask==255)
(x1,y1) = (np.min(x), np.min(y))
(x2,y2) = (np.max(x), np.max(y))
crop_image = grey[x1:x2+1,y1:y2+1]

plt.imshow(cv2.cvtColor(crop_image,cv2.COLOR_BGR2RGB))

reader = easyocr.Reader(["en"])
result = reader.readtext(crop_image)
result

text = result[0][-2]
font = cv2.FONT_HERSHEY_SIMPLEX
res = cv2.putText(img,text = text,org = (200,300),fontFace = font,fontScale=1,color=(0,255,0),thickness = 2, lineType = 1)
res = cv2.rectangle(img,tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0), 3)
plt.imshow(cv2.cvtColor(res,cv2.COLOR_BGR2RGB))

