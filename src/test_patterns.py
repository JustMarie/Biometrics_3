import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv


def example():
    fig, ax = plt.subplots(nrows=2, ncols=3)

    path_to_images = "C:\\Users\\mmingazo\\PycharmProjects\\Biometrics\\src\\ATT"
    path_to_images_masked = "C:\\Users\\mmingazo\\PycharmProjects\\Biometrics\\src\\ATT_masked"

    img1 = "10_9.png"
    img2 = "20_6.png"
    img3 = "29_9.png"

    im1_p = path_to_images + "\\" + img1
    im1_p_masked = path_to_images_masked + "\\" + img1
    im_0_0 = np.float32(cv.imread(im1_p, 0))
    im_1_0 = np.float32(cv.imread(im1_p_masked, 0))

    im2_p = path_to_images + "\\" + img2
    im2_p_masked = path_to_images_masked + "\\" + img2
    im_0_1 = np.float32(cv.imread(im2_p, 0))
    im_1_1 = np.float32(cv.imread(im2_p_masked, 0))

    im3_p = path_to_images + "\\" + img3
    im3_p_masked = path_to_images_masked + "\\" + img3
    im_0_2 = np.float32(cv.imread(im3_p, 0))
    im_1_2 = np.float32(cv.imread(im3_p_masked, 0))

    ax[0, 0].imshow(im_0_0, cmap='gray')
    ax[0, 0].set_xticks([])
    ax[0, 0].set_yticks([])

    ax[1, 0].imshow(im_1_0, cmap='gray')
    ax[1, 0].set_xticks([])
    ax[1, 0].set_yticks([])

    ax[0, 1].imshow(im_0_1, cmap='gray')
    ax[0, 1].set_xticks([])
    ax[0, 1].set_yticks([])

    ax[1, 1].imshow(im_1_1, cmap='gray')
    ax[1, 1].set_xticks([])
    ax[1, 1].set_yticks([])

    ax[0, 2].imshow(im_0_2, cmap='gray')
    ax[0, 2].set_xticks([])
    ax[0, 2].set_yticks([])

    ax[1, 2].imshow(im_1_2, cmap='gray')
    ax[1, 2].set_xticks([])
    ax[1, 2].set_yticks([])

    plt.subplots_adjust(hspace=0.55, wspace=0.45)

    plt.show()
