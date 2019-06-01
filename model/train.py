from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt

from model64_english import cnn_model_fn
#from model32 import cnn_model_fn

import pickle

tf.logging.set_verbosity(tf.logging.INFO)

name=""

def main(unused_argv):
    # Load training and eval data
    #mnist = tf.contrib.learn.datasets.load_dataset("mnist")
    #train_data = mnist.train.images  # Returns np.array
    #train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
    #eval_data = mnist.test.images  # Returns np.array
    #eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)
    for i in range(1,10):
        pickle_in = open("x_data9eng_fil_mix."+str(i)+".pickle","rb")
        train_data = pickle.load(pickle_in)
        train_data = np.float32(train_data)

        pickle_in = open("y_data9eng_fil_mix."+str(i)+".pickle","rb")
        train_labels = pickle.load(pickle_in)
        train_labels = np.asarray(train_labels)     
        
        pickle_in1 = open("x_test9eng_fil_mix."+str(i)+".pickle","rb")
        test_data = pickle.load(pickle_in1)
        test_data = np.float32(test_data)

        pickle_in1 = open("y_test9eng_fil_mix."+str(i)+".pickle","rb")
        test_labels = pickle.load(pickle_in1)
        test_labels = np.asarray(test_labels)

        
        if(i==1):
            l = train_labels
            d = train_data

            td = test_data
            tl = test_labels
            
        else:
            d = np.concatenate((d,train_data))
            l = np.append([l],[train_labels])

            td = np.concatenate((td,test_data))
            tl = np.append([tl],[test_labels])
        

        
        print(len(d))
        print(len(l))
        print(len(td))
        print(len(tl))
    # Create the Estimator

    tag_classifier = tf.estimator.Estimator(
        model_fn=cnn_model_fn, model_dir="saved")


    
    

    # Set up logging for predictions
    # Log the values in the "Softmax" tensor with label "probabilities"
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=50)
    # Train the model

    accuracy=[]
    loss=[]
    global_step=[]
    logfile = open("logfile_"+"data9eng_fil_mix"+".txt",mode="a")
    for j in range(1,9501):
        train_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": d},
            y=l,
            batch_size=500,
            num_epochs=1,
            shuffle=True)
        tag_classifier.train(
            input_fn=train_input_fn,
            steps=None,
            hooks=[logging_hook])
    
    
        

        '''
        # Evaluate the model and print results
        eval_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": test_data},
            y=test_labels,
            num_epochs=1,
            shuffle=False,
            batch_size=10
            )
        eval_results = tag_classifier.evaluate(input_fn=eval_input_fn)
        print(eval_results)
        '''
        

        eval_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": td},
            y=tl,
            num_epochs=1,
            shuffle=False,
            batch_size=10
            )
        # Create the Estimator
        tag_classifier = tf.estimator.Estimator(
            model_fn=cnn_model_fn, model_dir="saved")
        
        '''
        predictions = list(tag_classifier.predict(input_fn=eval_input_fn,predict_keys="probabilities"))
        for i in predictions:
            print(i["probabilities"])
        '''
        
        
        predictions = list(tag_classifier.predict(input_fn=eval_input_fn))
        predicted_classes = [p["classes"] for p in predictions]
        for i in range(len(predicted_classes)):
            #print("Label:",test_labels[i]," Predict:",predicted_classes[i])
            print("Label:",tl[i]," Predict:",predicted_classes[i])
            logfile.write(str("Label:"+str(tl[i])+" Predict:"+str(predicted_classes[i])+"\n"))
            
        eval_results = tag_classifier.evaluate(input_fn=eval_input_fn)
        print(eval_results)
        accuracy.append(eval_results["accuracy"])
        loss.append(eval_results["loss"])
        global_step.append(eval_results["global_step"]/9)
        logfile.write(str(eval_results)+"\n")
        logfile.write("Avg_acc:"+str(np.mean(accuracy))+"\t")
        logfile.write("Max:"+str(max(accuracy))+"\t")
        logfile.write("Avg_loss:"+str(np.mean(loss))+"\t")
        logfile.write("epoch:"+str(global_step[-1])+"\n")
    logfile.close()

    plt.plot(global_step, accuracy, 'b', global_step, loss , 'r')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Model Accuracy')
    plt.show()
    
    
    

if __name__ == "__main__":
    tf.app.run()