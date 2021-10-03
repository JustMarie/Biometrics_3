import math

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from skimage.io import imread
from skimage.color import rgb2gray
from barcode import EAN8
from barcode.writer import ImageWriter

HIST_SIZE = 8


def calc_hist_from_image(path):
    cv_image = cv.imread(path, cv.IMREAD_GRAYSCALE)
    image = np.float32(cv_image)
    hist = cv.calcHist([image], [0], None, [HIST_SIZE], [0, 255], accumulate=False).flatten("F")
    normalized_hist = [i / (cv_image.shape[0] * cv_image.shape[1]) for i in hist]
    max_hist_value = np.max(normalized_hist)
    scaled_hist = [math.floor(i * 9.5 / max_hist_value) for i in normalized_hist]

    # print("hist: ", hist)
    # print("normalized_hist: ", normalized_hist)
    # print("scaled_hist: ", scaled_hist[0:7])

    return scaled_hist


def plot_hist(hist):
    plt.figure()
    plt.bar(np.arange(1, HIST_SIZE + 1), hist)
    plt.xlim([0, HIST_SIZE + 1])
    plt.show()


def calc_ssim(path_1, path_2):
    image_1 = cv.imread(path_1, cv.IMREAD_GRAYSCALE)
    image_2 = cv.imread(path_2, cv.IMREAD_GRAYSCALE)

    score = ssim(image_1, image_2, multichannel=False)
    # print("SSIM: {}".format(score))


def calc_ssim2(path_1, path_2):
    image_1 = rgb2gray(imread(path_1))
    image_2 = rgb2gray(imread(path_2))

    # score2 = ssim(image_1, image_2, multichannel=False, gaussian_weights=True, sigma=1.5, use_sample_covariance=False,
    #               data_range=1.0)
    score2 = ssim(image_1, image_2, multichannel=False)
    # print("SSIM2: {}".format(score2))


def create_ean_barcode(path):
    hist_int_list = calc_hist_from_image(path)
    hist_str_list = map(str, hist_int_list[0:7])
    hist_numbers = ''.join(hist_str_list)

    bar = EAN8(hist_numbers, writer=ImageWriter())
    bar_name = path.split("/")[-1]
    bar_path = bar.save(bar_name)

    bar_png = plt.imread(bar_path)
    fig, ax = plt.subplots()
    ax.imshow(bar_png)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()
