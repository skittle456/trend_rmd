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

    pickle_in = open("X.pickle","rb")
    train_data = pickle.load(pickle_in)
    train_data = np.float32(train_data)

    pickle_in = open("y.pickle","rb")
    train_labels = pickle.load(pickle_in)
    train_labels = np.asarray(train_labels)
    # Create the Estimator
    mnist_classifier = tf.estimator.Estimator(
        model_fn=cnn_model_fn, model_dir="saved")

    # Set up logging for predictions
    # Log the values in the "Softmax" tensor with label "probabilities"
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=50)

    # Train the model
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=10,
        num_epochs=None,
        shuffle=True)
    mnist_classifier.train(
        input_fn=train_input_fn,
        steps=20000,
        hooks=[logging_hook])


    # Evaluate the model and print results
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        num_epochs=1,
        shuffle=False)
    eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)


if __name__ == "__main__":
    tf.app.run()