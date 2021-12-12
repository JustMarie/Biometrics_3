import cv2 as cv
import numpy as np
from src import biometrics_features as bf

HIST_METHOD = "HISTCMP_CORREL"
# BIN = 8

DCT_NORMALIZATION = 256
DFT_NORMALIZATION = 256
# p = 20

NUMBERS_OF_SCALING = 2


# M = 20
# N = 16

# GRADIENT_WIDTH = 10
# GRADIENT_STEP = 10


def compare_images(path_to_image_1, path_to_image_2, method, params):
    image_1 = np.float32(cv.imread(path_to_image_1, 0))
    image_2 = np.float32(cv.imread(path_to_image_2, 0))

    if method == "Histogram":

        hist_1 = cv.calcHist([image_1], [0], None, [params['BIN']], (0, 256), accumulate=False)
        hist_2 = cv.calcHist([image_2], [0], None, [params['BIN']], (0, 256), accumulate=False)

        # _, hist_1, _ = bf.histogram(image_1, BIN)
        # _, hist_2, _ = bf.histogram(image_2, BIN)

        diff = cv.compareHist(hist_1, hist_2, method=eval("cv." + HIST_METHOD))
        # diff = np.linalg.norm(np.array(hist_1) - np.array(hist_2))

        return diff

    elif method == "DCT":

        dct_1 = bf.DCT(image_1 / DCT_NORMALIZATION, params['p'])
        dct_2 = bf.DCT(image_2 / DCT_NORMALIZATION, params['p'])

        dct_1_vect = zigzag(dct_1, params['p'], bright_pixel=params['br_px'])
        dct_2_vect = zigzag(dct_2, params['p'], bright_pixel=params['br_px'])

        # dct_1 = cv.dct(image_1 / DCT_NORMALIZATION)
        # dct_2 = cv.dct(image_2 / DCT_NORMALIZATION)
        #
        # dct_1_vect = zigzag(dct_1, params['p'], bright_pixel=params['br_px'])
        # dct_2_vect = zigzag(dct_2, params['p'], bright_pixel=params['br_px'])

        diff = np.linalg.norm(dct_1_vect - dct_2_vect)

        return 1 / diff

    elif method == "DFT":

        dft_1 = bf.DFT(image_1 / DCT_NORMALIZATION, params['p'])
        dft_2 = bf.DFT(image_2 / DCT_NORMALIZATION, params['p'])

        dft_1_vect = zigzag(dft_1, params['p'], bright_pixel=params['br_px'])
        dft_2_vect = zigzag(dft_2, params['p'], bright_pixel=params['br_px'])

        diff = np.linalg.norm(dft_1_vect - dft_2_vect)

        return 1 / diff

    elif method == "Scale":

        scale_1 = cv.resize(image_1, (params['N'], params['M']), interpolation=cv.INTER_AREA)
        scale_2 = cv.resize(image_2, (params['N'], params['M']), interpolation=cv.INTER_AREA)
        scale_1_flat = scale_1.ravel()
        scale_2_flat = scale_2.ravel()

        diff = np.linalg.norm(scale_1_flat - scale_2_flat)

        return 1 / diff

    elif method == "Gradient":

        # barcode_1 = get_barcode_from_image(path_to_image_1)
        # barcode_2 = get_barcode_from_image(path_to_image_2)

        gr1 = np.array(bf.gradient(image_1, params['w'], params['st']))
        gr2 = np.array(bf.gradient(image_2, params['w'], params['st']))

        diff = np.linalg.norm(gr1 - gr2)

        return 1 / diff


def get_barcode_from_image(path, st, width):
    image = np.float32(cv.imread(path, 0))

    rows, _ = map(int, image.shape)
    result = []

    for i in range(0, rows, st):
        if i + 2 * width > rows:
            break

        result.append(
            np.linalg.norm(
                image[i: i + width] - image[i + width: i + (2 * width)]
            )
        )

    # average = sum(result) / len(result)
    # result = map(lambda a: 0 if a < average else 1, result)

    return np.fromiter(result, dtype=np.int)


def zigzag(c, p_param, bright_pixel=True):
    # DCT and DFT return matrix p*p
    t = 0
    vect_size = int(p_param * (p_param + 1) / 2)
    vector = np.zeros(vect_size, dtype=int)

    for y in range(p_param):
        for k in reversed(range(y + 1)):
            vector[t] = c[y - k, k]
            t += 1
    first_pixel = int(not bright_pixel)
    return vector[first_pixel:, ]
