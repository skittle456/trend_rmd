
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

def cnn_model_fn(features, labels, mode):
  """Model function for CNN."""
  # Input Layer
  # Reshape X to 4-D tensor: [batch_size, row, colum, channels]
  # MNIST images are 28x28 pixels, and have one color channel
  input_layer = tf.reshape(features["x"], [-1, 64 , 400])
  print(input_layer)
  
  #25600
  # Convolutional Layer #1
  # Computes 32 features using a 5x5 filter with ReLU activation.
  # Padding is added to preserve width and height.
  # Input Tensor Shape: [batch_size, 64, 400, 1]
  # Output Tensor Shape: [batch_size, 64, 400, 32]
  conv1 = tf.layers.conv1d(
      inputs=input_layer,
      filters=200,
      kernel_size=4,
      padding="same",
      activation=tf.nn.relu)
  #25600
  print(conv1)
  # Pooling Layer #1
  # Second max pooling layer with a 2x2 filter and stride of 2
  # Input Tensor Shape: [batch_size, 64, 400, 64]
  # Output Tensor Shape: [batch_size, 32, 200, 64]
  pool1 = tf.layers.max_pooling1d(inputs=conv1, pool_size=2, strides=2)
  #12800
  print(pool1)
  # Convolutional Layer #2
  # Computes 64 features using a 32x200 filter.
  # Padding is added to preserve width and height.
  # Input Tensor Shape: [batch_size, 32, 200, 32]
  # Output Tensor Shape: [batch_size, 32, 200, 64]
  conv2 = tf.layers.conv1d(
      inputs=pool1,
      filters=100,
      kernel_size=4,
      padding="same",
      activation=tf.nn.relu)
  #12796
  print(conv2)
  # Pooling Layer #2
  # Second max pooling layer with a 2x2 filter and stride of 2
  # Input Tensor Shape: [batch_size, 32, 200, 64]
  # Output Tensor Shape: [batch_size, 16, 100, 64]
  pool2 = tf.layers.max_pooling1d(inputs=conv2, pool_size=2, strides=2)
  #6388
  print(pool2)

  conv3 = tf.layers.conv1d(
      inputs=pool2,
      filters=25,
      kernel_size=4,
      padding="same",
      activation=tf.nn.relu)

  pool3 = tf.layers.max_pooling1d(inputs=conv3, pool_size=2, strides=2)
  # Flatten tensor into a batch of vectors
  # Input Tensor Shape: [batch_size, 16, 100, 64]
  # Output Tensor Shape: [batch_size, 16 * 100 * 64]
  pool3_flat = tf.reshape(pool3, [-1, 8 * 25])
  print(pool3_flat)
  # Dense Layer
  # Densely connected layer with 256 neurons
  # Input Tensor Shape: [batch_size, 16 * 100 * 64]
  # Output Tensor Shape: [batch_size, 256]
  dense = tf.layers.dense(inputs=pool3_flat, units=200, activation=tf.nn.relu)

  # Add dropout operation; 0.6 probability that element will be kept
  dropout1 = tf.layers.dropout( inputs=dense, rate=0.5, training=mode == tf.estimator.ModeKeys.TRAIN)
  print(dropout1)
  # Logits layer
  # Input Tensor Shape: [batch_size, 256]
  # Output Tensor Shape: [batch_size, 10]
  dense2 = tf.layers.dense(inputs=dropout1, units=100, activation=tf.nn.relu)
  logits1 = tf.layers.dense(inputs=dense2, units=10)

  print(logits1)
  predictions = {
      # Generate predictions (for PREDICT and EVAL mode)
      "classes": tf.argmax(input=logits1, axis=1),
      # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
      # `logging_hook`.
      "probabilities": tf.nn.softmax(logits1, name="softmax_tensor")
  }
  if mode == tf.estimator.ModeKeys.PREDICT:
    return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

  # Calculate Loss (for both TRAIN and EVAL modes)
  loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits1)

  # Configure the Training Op (for TRAIN mode)
  if mode == tf.estimator.ModeKeys.TRAIN:
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
    train_op = optimizer.minimize(
        loss=loss,
        global_step=tf.train.get_global_step())
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

  # Add evaluation metrics (for EVAL mode)
  eval_metric_ops = {
      "accuracy": tf.metrics.accuracy(
          labels=labels, predictions=predictions["classes"])}
  return tf.estimator.EstimatorSpec(
      mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

