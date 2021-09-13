import torch
from constants import DL_path
import time
# Model
model = torch.hub.load(DL_path.yolo_path, 'custom', path=DL_path.model_path)
model.conf = 0.7

imgs = "D:/Office/veronica/data/Driver_License/test-images/DL-Khushbu-1.jpg"
start_time = time.time()
# Inference
results = model(imgs)
print("--- %s seconds ---" % (time.time() - start_time))
save_folder = imgs.split("/")[-1].split(".")[0]

results.crop(save_dir=DL_path.save_dir+save_folder)
results.save(save_dir=DL_path.save_dir+save_folder)
