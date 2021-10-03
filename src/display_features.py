import import_ipynb
import biometrics_features as bf
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import cv2 as cv
import time


path_to_images = "C:\\Users\\tima7\\Jupyter Projects\\my progs\\Templ_matching\\ORL_DB\\ATT\\ATT\\"

def show_features_of_one_image(m, n, p, BIN, w, s):
# params = (m, n, p, BIN, W, s)
#    scale_feat = bf.scale(img, params[0], params[1])   #return matrix of resized image
#    dtf_feat = DFT(img, params[2])                     # return matrix p*p? mot centred
#    dct_feat = DCT(img, params[2])                     # also
#    hist_feat = histogram(img, params[3])              # list of distributon, hist and normallised hist
#    grad_feat = gradient(img, params[4])               # list of numers
    
    plt.ion()
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)
    
   # images = next(os.walk(path_to_images))[2]
    images = [path_to_images + str(i) + "_1.png" for i in range(1, 41)]
    for path in images:
        img = np.float32(cv.imread(path, 0))
        scale_feat = bf.Scale(img, m, n)   #return matrix of resized image
        dtf_feat = bf.DFT(img, p)                     # return matrix p*p? mot centred
        dct_feat = bf.DCT(img, p)                     # also
        hist_feat = bf.histogram(img, BIN)              # list of distributon, hist and normallised hist
        grad_feat = bf.gradient(img, w, s)    
        
        plt.clf()
        
        #plt.subplot(231)
        ax1.imshow(img, cmap='gray')
        
        #plt.subplot(232)
        ax2.imshow(scale_feat, cmap='gray')
        
        #plt.subplot(233)
        dft_centred = np.fft.fftshift(dtf_feat)
        dft_centred = np.log(np.abs(dft_centred))
        ax3 = sns.heatmap(abs(dft_centred), cmap='gray')
        
        #plt.subplot(234)
        ax4 = sns.heatmap(dct_feat, cmap='gray')
        
        #plt.subplot(235)
        b = hist_feat[1]
        edges = [i*BIN for i in range(1, len(b)+1)]
        ax5.bar(edges, b, width=int(BIN/2))
        
        #plt.subplot(236)
        x_grad = range(len(grad_feat))
        ax5.plot(x_grad, grad_feat)
        ax6.grid(True)
        
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Задержка перед следующим обновлением
        time.sleep(0.02)
        
    plt.ioff()

    #plt.show()   
