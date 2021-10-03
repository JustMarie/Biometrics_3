import biom_features as bf
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import cv2 as cv
import time

PATH = os.getcwd()
#methods = ["Histogram", "DFT", "DCT", "Scale", "Gradient"]


def feat_demonst(m, n, p, BIN, w, s):

    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(ncols=3, nrows=2, figsize=(10, 8))
    images = [PATH + "/ATT/" + str(i) + "_1.png" for i in range(1, 41)]

    for image in images:
        img = np.float32(cv.imread(image, 0))
        scale_feat = bf.Scale(img, m, n)  # return matrix of resized image
        dtf_feat = bf.DFT(img, p)  # return matrix p*p? mot centred
        dct_feat = bf.DCT(img, p)  # also
        hist_feat = bf.histogram(img, BIN)  # list of distributon, hist and normallised hist
        grad_feat = bf.gradient(img, w, s)


        ax1.imshow(img, cmap='gray')
        ax1.set_title("Origin image (112*92)")

        # resized imge
        ax2.imshow(scale_feat, cmap='gray')
        ax2.set_title("Scale, m=18, n=15")

        dft_centred = np.fft.fftshift(dtf_feat)
        dft_centred = np.log(np.abs(dft_centred))
        ax3.cla()
        ax3.imshow(abs(dft_centred), cmap='gray')
        ax3.set_title("DFT, p=20")

        # plt.subplot(234)
        ax4.imshow(dct_feat, cmap='gray')
        ax4.set_title("DCT, p=20")

        # plt.subplot(235)
        b = hist_feat[1]
        edges = [i * BIN for i in range(1, len(b) + 1)]
        ax5.cla()
        ax5.bar(edges, b, width=int(BIN / 2))

        # plt.subplot(236)
        x_grad = range(len(grad_feat))
        ax6.cla()
        ax6.plot(x_grad, grad_feat)

        ax6.grid(True)

        # fig.canvas.draw()
        # fig.canvas.flush_events()

        plt.ion()
        plt.show()
        plt.pause(0.05)

    plt.close()
