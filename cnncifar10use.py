import tflearn
from tflearn.data_utils import shuffle, to_categorical
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import numpy as np


def read_img_crop(img_file):
    from PIL import Image, ImageOps
    import numpy as np
    img = Image.open(img_file).convert('RGB')
    img = ImageOps.fit(img, ((32, 32)), Image.ANTIALIAS)

    img_arr = np.array(img)
    imgarr2 = img_arr

    assert img_arr.shape == ((32, 32, 3)), "expected (32,32,3)"
    img_arr = img_arr.reshape(1, 32, 32, 3).astype("float")  # .transpose(0,3,1,2)\
    print((img_arr == imgarr2).all())
    return img_arr

def predict(img):

    img_prep = ImagePreprocessing() # Real-time data preprocessing
    img_prep.add_featurewise_zero_center()
    img_prep.add_featurewise_stdnorm()

    # Real-time data augmentation
    img_aug = ImageAugmentation()
    img_aug.add_random_flip_leftright()
    img_aug.add_random_rotation(max_angle=25.)

    # Convolutional network building
    network = input_data(shape=[None, 32, 32, 3],
                         data_preprocessing=img_prep,
                         data_augmentation=img_aug
                         )
    network = conv_2d(network, 32, 3, activation='relu')
    network = max_pool_2d(network, 2)
    network = conv_2d(network, 64, 3, activation='relu')
    network = conv_2d(network, 64, 3, activation='relu')
    network = max_pool_2d(network, 2)
    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, 0.5)
    network = fully_connected(network, 10, activation='softmax')
    network = regression(network, optimizer='adam',
                         loss='categorical_crossentropy',
                         learning_rate=0.001)

    # Train using classifier
    model = tflearn.DNN(network, tensorboard_verbose=0)
    model.load("cnncifar10first.tfl")

    image = read_img_crop(img)
    pred = model.predict(image)
    return (pred[0]),(np.argmax(pred) + 1)