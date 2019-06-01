from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import numpy as np
import pickle
#CATEGORIES = ["Politic","Education","Sport","Music","Plant","Language","Location","Animal","Food","Region"]
#CATEGORIES = ["music","sport"]
CATEGORIES = ["business","entertainment","food","health","music","plant","politics","sport","tech"]
'''
amoumt_value = 1000 #Setup amoumt of value  !!!!!!!!!!!
file_name = "data5_1000_fil_nonaugment"
title_plt = 'Data 5, 1000 filter non-augment'
'''
def visualize_tsne(amoumt_value=1000, file_name=None, title_plt=None, plot_only='r'):
    for i in range(1,10):
        print(i)
        pickle_in = open("x_"+ file_name +"."+str(i)+".pickle","rb") #Setup name here !!!!!!!!!!
        train_data = pickle.load(pickle_in)
        train_data = np.float32(train_data)[:amoumt_value]
        train_data = np.array(train_data).reshape(amoumt_value,300* 64)

        pickle_in = open("y_"+ file_name +"."+str(i)+".pickle","rb") #Setup name here !!!!!!!!!!
        train_labels = pickle.load(pickle_in)
        train_labels = np.asarray(train_labels)[:amoumt_value] 
        if(i==1):
            l = train_labels
            d = train_data
        else:
            d = np.concatenate((d,train_data))
            l = np.append([l],[train_labels])


        
        
    tsne = TSNE(n_components=2, random_state=0)
    X_2d = tsne.fit_transform(d)
    plt.figure(figsize=(6, 5))
    plt.title(title_plt)
    colors = 'r', 'g', 'b', 'c', 'm', 'y', 'k', 'silver', 'orange', 'purple'
    for i, c, label in zip(range(0,10), colors, CATEGORIES):
        #print("running:",i,c,label)
        #if c == plot_only:
            #plt.scatter(X_2d[l == i, 0], X_2d[l == i, 1], c=c, label=label)
        plt.scatter(X_2d[l == i, 0], X_2d[l == i, 1], c=c, label=label)
    plt.legend()
    plt.show()
    #plt.show()
    #'visualize_image/'
    plt.savefig(title_plt+'.png')

sizes = [300]
#sizes = [500, 300, 100, 50]
#names = ['data5_1000_fil_pureaugment', 'data5_1000_unfil', 'data5_1000_unfil_mixing', 'data5_1000_unfil_pureaugment', 'data5_1000_fil_nonaugment']
names = ['data9eng_fil_mix']
#colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'silver', 'orange', 'purple']
#colors = ['r','g']
for name in names:
    for size in sizes:
        #for color in colors:
        try:
            title = name + '_value_' + str(size) #+ '_' + str(color)
            #visualize_tsne(amoumt_value=size, file_name=name, title_plt=title, plot_only=color)
            visualize_tsne(amoumt_value=size, file_name=name, title_plt=title)
            print('success, file_name: '+ name +', size: '+ str(size))
        except:
            print('fail, file_name: '+ name +', size: '+ str(size))
        
