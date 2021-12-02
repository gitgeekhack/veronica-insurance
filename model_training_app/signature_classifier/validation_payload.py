import os

import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model

from constants import MODEL_PATH

model = load_model(MODEL_PATH)
target = '../../data/Signature/dataset/test/'
master_list = []

for root, dirs, files in os.walk(target):
    for dir in dirs:
        for _, _, files in os.walk(os.path.join(target, dir)):
            for file in files:
                path = os.path.join(target, dir, file)
                img = tf.keras.utils.load_img(path, target_size=(150, 150))
                img_array = tf.keras.utils.img_to_array(img) / 255
                img_array = tf.expand_dims(img_array, 0)

                actual = dir
                predict = "Signature" if model.predict(img_array) > 0 else "No_Signature"
                comp = True if actual == predict else False
                data = [f'{dir}/{file}', model.predict(img_array)[0][0], actual, predict, comp]
                master_list.append(data)

df = pd.DataFrame(master_list, columns=['file', 'predict_value', 'Actual', 'Predicted', 'Is-True'])
df.to_csv('prediction_label_debugging.csv', index=False)
