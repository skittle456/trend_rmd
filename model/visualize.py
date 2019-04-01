from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import numpy as np
import pickle


def visualize_tsne():
    for i in range(1,11):
        print(i)
        pickle_in = open("x_data5_100000."+str(i)+".pickle","rb")
        train_data = pickle.load(pickle_in)
        train_data = np.float32(train_data)[:500]
        train_data = np.array(train_data).reshape(500,400* 64)

        pickle_in = open("y_data5_100000."+str(i)+".pickle","rb")
        train_labels = pickle.load(pickle_in)
        train_labels = np.asarray(train_labels)[:500]

        if(i==1):
            l = train_labels
            d = train_data
        else:
            d = np.concatenate((d,train_data))
            l = np.append([l],[train_labels])


        
        

    tsne = TSNE(n_components=2, random_state=0)
    X_2d = tsne.fit_transform(d)
    plt.figure(figsize=(6, 5))
    colors = 'r', 'g', 'b', 'c', 'm', 'y', 'k', 'silver', 'orange', 'purple'
    for i, c, label in zip(range(0,10), colors, range(0,10)):
        print("running:",i,c,label)
        plt.scatter(X_2d[l == i, 0], X_2d[l == i, 1], c=c, label=label)
    plt.legend()
    plt.show()
    plt.savefig('visualize_image/visual_64_500from10000.png')

visualize_tsne()
