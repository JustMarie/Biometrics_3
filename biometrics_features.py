import numpy as np
import cv2 as cv

from math import exp, pi, sqrt, cos, sin
import matplotlib.pyplot as plt
import seaborn as sns
import os

def Scale(src, m, n):
    M, N = src.shape
    small_img = cv.resize(src, (15, 18), interpolation=cv.INTER_AREA)
 #   pixel_vector = small_img.ravel()
 #   return pixel_vector
    return small_img
    
    
def DFT(img, p):
    M, N = img.shape
    F_pM_Cos = np.zeros((p, M))
    F_pM_Sin = np.zeros((p, M))
    F_Np_Cos = np.zeros((N, p))
    F_Np_Sin = np.zeros((N, p))
    for i in range(0, p):
        for j in range(0, M):
            F_pM_Cos[i, j] = cos(2 * pi / M * i * j)
            F_pM_Sin[i, j] = sin(2 * pi / M * i * j)

    for i in range(0, N):
        for j in range(0, p):
            F_Np_Cos[i, j] = cos(2 * pi / N * i * j)
            F_Np_Sin[i, j] = sin(2 * pi / N * i * j)
    
    FXcos = (F_pM_Cos.dot(img))
    FXsin = (F_pM_Sin.dot(img))
    
    Creal = FXcos.dot(F_Np_Cos) - FXsin.dot(F_Np_Sin)
    Cimage = FXcos.dot(F_Np_Sin) + FXsin.dot(F_Np_Cos)
   
    tmp = np.square(Creal) + np.square(Cimage)
  #  tmp = np.matmul(Creal, Creal) + np.matmul(Cimage, Cimage)
    C = np.sqrt(tmp)
    return C

def DCT(img, p):
    M, N = img.shape
    T_pM = np.zeros((p, M))
    T_Np = np.zeros((N, p))

    for j in range(0, M):
        T_pM[0, j] = 1 / sqrt(M)
    for i in range(1, p):
        for j in range(0, M):
            T_pM[i, j] = sqrt(2 / M) * cos((pi * (2 * j + 1) * i) / (2 * M))

    for i in range(0, N):
        T_Np[i, 0] = 1 / sqrt(N)
    for i in range(0, N):
        for j in range(0, p):
            T_Np[i, j] = sqrt(2 / N) * cos((pi * (2 * i + 1) * j) / (2 * N))

    C = (T_pM.dot(img)).dot(T_Np)
    return C
def histogram(img, BIN):
    Hi = [0 for _ in range(256)]
    M, N = img.shape
    for i in range(0, M):
        for j in range(0, N):
            Hi[int(img[i, j])] += 1

    Hb = [0 for _ in range(BIN)]
    for i in range(0, BIN):
        for j in range(int(i * 256 / BIN), int((i + 1) * 256 / BIN)):
            Hb[i] += Hi[j]
    HbNorm = [Hb[i] / (M * N) for i in range(BIN)]
    return [Hi, Hb, HbNorm]
# https://docs.opencv.org/3.4/d8/dbc/tutorial_histogram_calculation.html

def gradient(img, W, S):
    M, N = img.shape
    result = []

    lastRow = img[0:W]
    for i in range(S, M - W + 1, S):
        row = img[i:(i + W)]
        diff = abs(np.linalg.norm(lastRow - row))
        lastRow = row
        result.append(diff)
    return result


def distance(test, template):
    return abs(np.linalg.norm(np.array(test) - np.array(template)))
