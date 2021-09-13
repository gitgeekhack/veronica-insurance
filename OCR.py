import pytesseract as tess
import cv2
import os
import time
import numpy as np
from constants import path

tess.pytesseract.tesseract_cmd = path.tess_path
target = path.target+"/7647503_3ecc47c6e1d74602a1e4026b14aee152.jpeg"
print(target)

def preprocess(img):
    img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    cv2.imshow("before:",img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 100, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    kernel = np.ones((2, 2), np.uint8)
    img = cv2.dilate(img, kernel, iterations=3)
    kernel = np.ones((2, 2), np.uint8)
    img = cv2.erode(img, kernel, iterations=3)
    img = cv2.medianBlur(img, 5)
    cv2.imshow("img",img)
    return img

def gettext(filename):
    img = cv2.imread(filename)
    img = preprocess(img)
    config = "--psm 6 --oem 1 "
    text = tess.image_to_string(img,config=config)
    cv2.imshow("img", img)
    cv2.waitKey()
    return text


for (root, dirs, files) in os.walk(target, topdown=True):
    for name in files:
        fullName = os.path.join(root, name)
        label = os.path.basename(root)
        print(label, ": ", gettext(fullName))


