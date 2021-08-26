import torch
import cv2
from constants import path
import time
# Model
model = torch.hub.load(path.yolo_path, 'custom', path=path.model_path)

# Images
imgs = "test data/uk-fake-id.jpg"
start_time = time.time()
# Inference
results = model(imgs)
print("--- %s seconds ---" % (time.time() - start_time))
results.crop(path.save_folder)
results.save(path.save_folder)

