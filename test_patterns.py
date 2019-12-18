import import_ipynb
import biometrics_features as bf
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import cv2 as cv
import pandas as pd


def check_templ_im(k=4, method):
  images = []
  for i in range(1, 41):
      for j in range(1, k+1):
          images.append(path_to_images + str(i) + "_" + str(j) + ".png")

        
  index = [i for i in range(1, 41)]
  #columns = ["image_"+str(i) in range(1, k+1)] 
  for i in range(1, k+1):
     pattern_scale["image_"+str(i)]= ''
    
  for i in range(0, 40):
      for j in range(0, k):
          pattern_scale.iloc[i, j] = get_dist(images[i*k], images[i*k+j], 'scale', (18, 15))
    
