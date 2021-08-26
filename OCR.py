import pytesseract as tess
import cv2
import os
import time
from constants import path

tess.pytesseract.tesseract_cmd = path.tess_path
target = path.target


def gettext(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    text = tess.image_to_string(img)
    return text


for (root, dirs, files) in os.walk(target, topdown=True):
    for name in files:
        fullName = os.path.join(root, name)
        label = os.path.basename(root)
        if label != "sign":
            print(label, ": ", gettext(fullName))

