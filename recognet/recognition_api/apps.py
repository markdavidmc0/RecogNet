"""RecogNet initialiser - model init upon deployment, ready for fast predictions."""

import tensorflow as tf
from keras import backend as K

from recognition_api.helpers.inception_blocks_v2 import faceRecoModel
from recognition_api.helpers.fr_utils import load_weights_from_FaceNet

from django.apps import AppConfig


class RecognitionApiConfig(AppConfig):
    name = 'recognition_api'
    verbose_name = "Recognition API"

    def ready(self):
        # load prediction model from saved weights
        # K.set_image_data_format('channels_first')
        # FRmodel = faceRecoModel(input_shape=(3, 96, 96))
        # self.load_weights(FRmodel)
        pass

    def triplet_loss(self, y_true, y_pred: list, alpha=0.2) -> float:
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

    def load_weights(self, FRmodel) -> None:
        """Load weights from FaceNet model to avoid training cost.

        Argeuments:
        FRmodel -- """
        FRmodel = faceRecoModel(input_shape=(3, 96, 96))
        FRmodel.compile(optimizer='adam', loss=self.triplet_loss, metrics=['accuracy'])
        load_weights_from_FaceNet(FRmodel)
