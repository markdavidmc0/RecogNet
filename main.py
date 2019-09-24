"""RecogNet main - training and prediction for overhead open-world images."""

import numpy as np
import tensorflow as tf
from keras import backend as K
from PIL import Image
from resizeimage import resizeimage

from inception_blocks_v2 import faceRecoModel
from fr_utils import img_to_encoding
from fr_utils import load_weights_from_FaceNet


def triplet_loss(y_true, y_pred: list, alpha=0.2) -> float:
    """Implement triplet loss.

    Arguments:
    y_true -- true labels, required when you define a loss in Keras
    y_pred -- python list containing three objects:
            anchor -- the encodings for the anchor images, of shape (None, 128)
            positive -- the encodings for the positive images, of shape (None, 128)
            negative -- the encodings for the negative images, of shape (None, 128)

    Returns:
    loss -- value of the loss
    """

    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]

    # Compute the (encoding) distance between the anchor and the positive
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)), axis=-1)
    # Compute the (encoding) distance between the anchor and the negative
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)), axis=-1)
    # Subtract the two previous distances and add alpha
    basic_loss = pos_dist - neg_dist + alpha
    # Take the maximum of basic_loss and 0.0. Sum over the training examples
    loss = tf.reduce_sum(tf.maximum(basic_loss, 0))

    return loss


def load_weights(FRmodel) -> None:
    """Load weights from FaceNet model to avoid training cost.

    Argeuments:
    FRmodel -- """
    FRmodel = faceRecoModel(input_shape=(3, 96, 96))
    FRmodel.compile(optimizer='adam', loss=triplet_loss, metrics=['accuracy'])
    load_weights_from_FaceNet(FRmodel)


def verify(image_path: str, identity: str, database: dict, model,
           threshold: float) -> tuple:
    """Verify if the person on the "image_path" image is "identity".

    Arguments:
    image_path -- path to an image
    identity -- string, name of the person you'd like to verify the identity
    database -- mapping of allowed people's names to their encodings
    model -- your Inception model instance in Keras
    threshold -- cut-off for positive/negative match

    Returns:
    dist -- distance between the image_path and the image of "identity" in the database
    positive_match -- True, if positive match. False otherwise
    """
    # Compute the encoding for the image
    encoding = img_to_encoding(image_path, model)

    # Compute distance with identity's image
    dist = np.linalg.norm(encoding - database[identity])
    print(dist)

    # Positive match if dist < threshold, else negative match
    if dist < threshold:
        print("It's " + str(identity) + ", welcome home!")
        positive_match = True
    else:
        print("It's not " + str(identity) + ", please go away")
        positive_match = False

    return dist, positive_match


def recognise(image_path: str, database: dict, model, threshold: float) -> tuple:
    """Implement face recognition against a database.

    Arguments:
    image_path -- path to an image
    database -- database containing image encodings along with name of person on the image
    model -- your Inception model instance in Keras
    threshold -- prediction cut-off been positive and negative

    Returns:
    min_dist -- the minimum distance between image_path encoding and encodings from the db
    identity -- string, the name prediction for the person on image_path
    """
    # Compute the target "encoding" for the image
    encoding = img_to_encoding(image_path, model)

    # Initialize "min_dist"
    min_dist = 100

    identity = ""
    # Loop over the database dictionary's names and encodings
    for (name, db_enc) in database.items():
        print(name)

        # Compute L2 distance between the target "encoding" and the current "enc"
        dist = np.linalg.norm(encoding - db_enc)
        print(dist)

        # If distance less than the min_dist, set min_dist to dist, and identity to name
        if dist < min_dist:
            min_dist = dist
            identity = name

    if min_dist > threshold:
        print("Not in the database.")
    else:
        print("it's " + str(identity) + ", the distance is " + str(min_dist))

    return min_dist, identity


def resize_image(url, width, height):
    with open(url, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [width, height])
            cover.save(url, image.format)


if __name__ == '__main__':
    K.set_image_data_format('channels_first')
    FRmodel = faceRecoModel(input_shape=(3, 96, 96))

    load_weights(FRmodel)

    database = dict()

    resize_image("/Users/markmc/Repos/RecogNet/faces/liis_01.jpg", 96, 96)
    resize_image("/Users/markmc/Repos/RecogNet/faces/mark_01.jpg", 96, 96)
    resize_image("/Users/markmc/Repos/RecogNet/faces/liis_02.jpg", 96, 96)
    resize_image("/Users/markmc/Repos/RecogNet/faces/mark_02.jpg", 96, 96)

    database["lisa"] = img_to_encoding("/Users/markmc/Repos/RecogNet/faces/liis_03.jpg", FRmodel)
    database["mark"] = img_to_encoding("/Users/markmc/Repos/RecogNet/faces/mark_05.jpg", FRmodel)

    verify("/Users/markmc/Repos/RecogNet/faces/mark_02.jpg", "lisa", database, FRmodel, 0.1)
    verify("/Users/markmc/Repos/RecogNet/faces/mark_03.jpg", "lisa", database, FRmodel, 0.1)

    print('=============liis_01 image for processing =================')
    recognise("/Users/markmc/Repos/RecogNet/faces/liis_01.jpg", database, FRmodel, 0.2)
    print('=============liis_02 image for processing =================')
    recognise("/Users/markmc/Repos/RecogNet/faces/liis_02.jpg", database, FRmodel, 0.2)
    print('=============liis_03 image for processing =================')
    recognise("/Users/markmc/Repos/RecogNet/faces/liis_03.jpg", database, FRmodel, 0.2)
    print('=============liis_04 image for processing =================')
    recognise("/Users/markmc/Repos/RecogNet/faces/liis_04.jpg", database, FRmodel, 0.2)
    print('=============liis_05 image for processing =================')
    recognise("/Users/markmc/Repos/RecogNet/faces/liis_05.jpg", database, FRmodel, 0.2)
    print('=============mark_01 image for processing =================')
    recognise("/Users/markmc/Repos/RecogNet/faces/mark_01.jpg", database, FRmodel, 0.2)
    print('=============mark_02 image for processing =================')
    recognise("/Users/markmc/Repos/RecogNet/faces/mark_02.jpg", database, FRmodel, 0.2)
    print('=============mark_03 image for processing =================')
    recognise("/Users/markmc/Repos/RecogNet/faces/mark_03.jpg", database, FRmodel, 0.2)
    print('=============mark_04 image for processing =================')
    recognise("/Users/markmc/Repos/RecogNet/faces/mark_04.jpg", database, FRmodel, 0.2)
    print('=============mark_05 image for processing =================')
    recognise("/Users/markmc/Repos/RecogNet/faces/mark_05.jpg", database, FRmodel, 0.2)

