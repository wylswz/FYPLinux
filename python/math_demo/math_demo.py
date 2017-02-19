import numpy as np
import matplotlib.pyplot as plt

def Dirichlet(sparsity,dimension):
    index = np.arange(dimension)
    fig,ax = plt.subplots(nrows=5,ncols=5)
    temp_counter=0
    for i in range(5):
        for j in range(5):
            temp_counter+=2
            alpha = np.ones(dimension)*sparsity*temp_counter
            s = np.random.dirichlet(alpha,dimension)
            bar_plot(ax[i,j],index,s[0],bar_width,alpha)
    plt.show()    
    

def bar_plot(ax,index,number,bar_width,alpha):
    ax.bar(index,number,bar_width)
    ax.set_title('alpha = %d' % int(alpha[0]),fontsize=10)
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)


bar_width = 0.1
sparsity = 1
dimension = 20

while True:
    try:
        ipt = raw_input('option: 1. Dirichlet \n ')
    except IOError:
        print 'invalid input'
    else:
        if ipt == '1':
            Dirichlet(sparsity,dimension)





print s









