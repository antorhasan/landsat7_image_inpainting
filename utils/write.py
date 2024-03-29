
import random
import glob
import sys
import cv2
import numpy as np
import tensorflow as tf


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

mean = np.load("/media/antor/Files/main_projects/gitlab/Landsat7_image_inpainting/train_mean.npy")

def createDataRecord(out_filename, addrs_y, addrs_m):
    writer = tf.python_io.TFRecordWriter(out_filename)
    for i in range(len(addrs_y)):
        print(i)
        img_y = cv2.imread(addrs_y[i], cv2.IMREAD_GRAYSCALE)
        #img_y = cv2.fastNlMeansDenoising(img_y, h=24, templateWindowSize=7, searchWindowSize=21)

        img_y = np.asarray(img_y)
        #img_y = np.asarray(cv2.imread(addrs_y[i], cv2.IMREAD_GRAYSCALE))
        img_m = np.asarray(cv2.imread(addrs_m[i], cv2.IMREAD_GRAYSCALE))


        last_y = np.reshape(img_y, (256,256,1))
        last_y = last_y/255
        last_y = last_y-mean

        #print(last_y)
        last_m = np.reshape(img_m,(256,256,1))
        last_m = np.where(last_m>230,1,0)
        last_m = last_m.astype(float)

        #last_x = np.multiply(last_y,last_m)

        feature = {
            'image_y': _bytes_feature(last_y.tostring()),
            'image_m': _bytes_feature(last_m.tostring())
            #'image_x': _bytes_feature(last_x.tostring())
        }

        example = tf.train.Example(features=tf.train.Features(feature=feature))

        writer.write(example.SerializeToString())

    writer.close()
    sys.stdout.flush()



trainY = "/media/antor/Files/ML/Papers/slc_inpainting/Data/last_gt/*.jpg"
trainY_list = glob.glob(trainY)

trainM = "/media/antor/Files/ML/Papers/slc_inpainting/Data/last_mk/*.jpg"
trainM_list = glob.glob(trainM)

random.seed(3)
random.shuffle(trainY_list)
random.seed(3)
random.shuffle(trainM_list)

train_Y = trainY_list[0:19488]
train_M = trainM_list[0:19488]
val_Y = trainY_list[19488:21376]
val_M = trainM_list[19488:21376]

# train_Y = trainY_list[0:10]
# train_M = trainM_list[0:10]
# val_Y = trainY_list[10:20]
# val_M = trainM_list[10:20]



createDataRecord("/media/antor/Files/ML/tfrecord/slc_inpainting/train.tfrecords", train_Y, train_M)
createDataRecord("/media/antor/Files/ML/tfrecord/slc_inpainting/val.tfrecords", val_Y, val_M)
