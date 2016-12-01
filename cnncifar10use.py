import scipy
import tflearn
from tflearn.data_utils import shuffle, to_categorical
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import os
import numpy as np

def read_img_crop(img_file):
    # from PIL import Image, ImageOps
    # img = Image.open(img_file).convert('RGB')
    # img = ImageOps.fit(img, ((32, 32)), Image.ANTIALIAS)
    # img_arr = np.array(img)
    # imgarr2 = img_arr
    # assert img_arr.shape == ((32, 32, 3)), "expected (32,32,3)"
    # img_arr = img_arr.reshape(1, 32, 32, 3).astype("float")  # .transpose(0,3,1,2)\

    image = scipy.ndimage.imread(img_file, mode='RGB')
    image_arr = scipy.misc.imresize(image, (32, 32), interp='bicubic').astype(np.float32, casting='unsafe')
    return image_arr

def predict(img, root):

    # cnn
    network = input_data(shape=[None, 32, 32, 3])
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
    model.load(os.path.join(root, "cnncifar10.tfl"))
    image = read_img_crop(img)
    pred = model.predict([image])
    model = None
    return pred[0],np.argmax(pred)

import sys

if len(sys.argv) > 1:
    path_to_img = sys.argv[1]
    (p),(pm) = predict(path_to_img, "./")
    classes = ['plane','car','bird','cat','deer','dog','frog','horse','ship','truck']
    print classes[pm]
else:
    print "Usage: python cnncifar10use.py path_to_image_file"