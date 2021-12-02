import tensorflow as tf
from tensorflow.keras.models import load_model

img_size = 150
image_path = 'Sign3.png'
model_path = './models/20211202_0446/model.h5'


class Verification:

    def __preprocess(self, path):
        img = tf.keras.utils.load_img(path, target_size=(150, 150))
        img_array = tf.keras.utils.img_to_array(img) / 255
        img_array = tf.expand_dims(img_array, 0)
        return img_array

    def predict(self, path):
        data = self.__preprocess(path)
        return "Signature" if model.predict(data) > 0 else "No_Signature"


v = Verification()
model = load_model(model_path)
print(v.predict(image_path))
