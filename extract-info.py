import torch
import cv2
from constants import path
import time
# Model
model = torch.hub.load(path.yolo_path, 'custom', path=path.model_path)
model.conf = 0.70

imgs = "DrivingLicenses/7647503_3ecc47c6e1d74602a1e4026b14aee152.jpeg"
start_time = time.time()
# Inference
results = model(imgs)
print("--- %s seconds ---" % (time.time() - start_time))
results.crop(path.save_folder+"/"+imgs.split("/")[1])


