from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

from model import cnn_model_fn

import pickle

tf.logging.set_verbosity(tf.logging.INFO)

def main(unused_argv):
    # Load training and eval data
    #mnist = tf.contrib.learn.datasets.load_dataset("mnist")
    #train_data = mnist.train.images  # Returns np.array
    #train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
    #eval_data = mnist.test.images  # Returns np.array
    #eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

    pickle_in = open("X_article.pickle","rb")
    article = pickle.load(pickle_in)
    article = np.float32(article)

    # Create the Estimator
    tag_classifier = tf.estimator.Estimator(
        model_fn=cnn_model_fn, model_dir="saved")

    # Set up logging for predictions
    # Log the values in the "Softmax" tensor with label "probabilities"
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=50)

    predicted = tag_classifier.predict(article)
    


if __name__ == "__main__":
    tf.app.run()