import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.models import load_model

from constants import MODEL_PATH, IMG_SIZE, BATCH_SIZE, DATASET_PATH

model = load_model(MODEL_PATH)


def format_example(pair):
    image, label = pair['image'], pair['label']
    image = tf.cast(image, tf.float32)
    image = image / 255.
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
    return image, label


# test the model on test dataset
model = load_model(MODEL_PATH)
builder = tfds.folder_dataset.ImageFolder(DATASET_PATH)
test_set = builder.as_dataset(split='test', shuffle_files=True)
test = test_set.map(format_example)
test_batches = test.batch(BATCH_SIZE)

print(model.evaluate(test_batches))
