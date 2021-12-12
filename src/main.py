from experiments import *
from preparation import set_num_of_standards
import display_features as df
from test_patterns import example

methods = ["Histogram", "DFT", "DCT", "Scale", "Gradient"]  # methods for LAB №3

visualize = True  # show graphs
show_images = True  # show images in optimal search

num_of_standards = 2  # set num of standards(training dataset) before executable cycle

set_num_of_standards(num_of_standards)

# # ======== LAB №3 ==========
# for method in methods:
#     search_optimal_one_method(method)

# search_optimal_one_method("Histogram")

# for i in range(1, 10):
#     num_of_standards = i
#     set_num_of_standards(num_of_standards)
#     search('DCT', 20, visualize=True)

#  ======== LAB №4 ==========
params = dict(p=20, br_px=False, BIN=32, M=14, N=12, w=10, st=11)
search_optimal_all_methods(visualize, show_images, params)

# df.show_features_of_one_image(18, 15, 20, 32, 20, 4)

# example()

# search_optimal_one_method("Scale")
