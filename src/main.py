from signs import *
from sorting import set_num_of_standards
import display_features as df
from test_patterns import example

methods = ["Histogram", "DFT", "DCT", "Scale", "Gradient"]  # methods for LAB №3

visualize = True  # show graphs
show_images = True  # show images in optimal search

num_of_standards = 1  # set num of standards(training dataset) before executable cycle

# set_num_of_standards(num_of_standards)

# ======== LAB №3 ==========
# for method in methods:
# search("DFT", 20, visualize=visualize)

for i in range(1, 10):
    num_of_standards = i
    set_num_of_standards(num_of_standards)
    search('DCT', 20, visualize=True)

#  ======== LAB №4 ==========
# search_optimal(visualize, show_images)

# df.show_features_of_one_image(18, 15, 20, 32, 20, 4)

example()
