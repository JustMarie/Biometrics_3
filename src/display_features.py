import biometrics_features as bf
import matplotlib.pyplot as plt
import os
import numpy as np
import cv2 as cv
import time

path_to_images = "C:\\Users\\mmingazo\\PycharmProjects\\Biometrics\\src\\ATT_masked"


def show_features_of_one_image(m, n, p, BIN, w, s):
    """display all feature spaces for all images and certain parameters"""
    """ params = (m, n, p, BIN, W, s)"""
    #    scale_feat = bf.scale(img, params[0], params[1])   #return matrix of resized image
    #    dtf_feat = DFT(img, params[2])                     # return matrix p*p? mot centred
    #    dct_feat = DCT(img, params[2])                     # also
    #    hist_feat = histogram(img, params[3])              # list of distributon, hist and normallised hist
    #    grad_feat = gradient(img, params[4])               # list of numers

    plt.ion()
    fig, ax = plt.subplots(nrows=2, ncols=3)

    images = next(os.walk(path_to_images))[2]

    for path in images:
        path_to_image = path_to_images + "\\" + path
        img = np.float32(cv.imread(path_to_image, 0))

        scale_feat = bf.Scale(img, m, n)  # return matrix of resized image
        dtf_feat = bf.DFT(img, p)  # return matrix p*p? not centred
        dct_feat = bf.DCT(img, p)  # also
        hist_feat = bf.histogram(img, BIN)  # list of distributon, hist and normallised hist
        grad_feat = bf.gradient(img, w, s)

        ax[0, 0].imshow(img, cmap='gray')
        ax[0, 0].set_title("Origin")

        ax[0, 1].imshow(scale_feat, cmap='gray')
        ax[0, 1].set_title("Scale to {}x{}".format(m, n))

        ax[0, 2].cla()
        dft_centred = np.fft.fftshift(dtf_feat)
        dft_centred = np.log(np.abs(dft_centred))
        ax[0, 2].set_title("DFT, p={}".format(p))

        ax[0, 2].imshow(abs(dft_centred), cmap='gray')

        ax[1, 0].imshow(dct_feat, cmap='gray')
        ax[1, 0].set_title("DCT, p={}".format(p))

        ax[1, 1].cla()
        b = hist_feat[1]
        edges = [i * BIN for i in range(1, len(b) + 1)]
        ax[1, 1].bar(edges, b, width=int(BIN / 2))
        ax[1, 1].set_title("Hist, BIN={}".format(BIN))

        ax[1, 2].cla()
        x_grad = range(len(grad_feat))
        ax[1, 2].plot(x_grad, grad_feat)
        ax[1, 2].grid(True)
        ax[1, 2].set_title("Grad, w={} s={}".format(w, s))

        fig.canvas.draw()

        plt.subplots_adjust(hspace=0.55, wspace=0.45)

        plt.show()

        fig.canvas.flush_events()

        time.sleep(0.1)

    # plt.ioff()
