from signs import *
from sorting import set_num_of_standards

methods = ["Histogram", "DFT", "DCT", "Scale", "Gradient"]  # methods for LAB №3

visualize = True  # show graphs
show_images = True  # show images in optimal search

num_of_standards = 2  # set num of standards(training dataset) before executable cycle

set_num_of_standards(num_of_standards)

#  ======== LAB №3 ==========
# for method in methods:
#     search(method, visualize=visualize)

for i in range(1, 10):
    num_of_standards = i
    set_num_of_standards(num_of_standards)
    search('DCT', 20, visualize = False)


#  ======== LAB №4 ==========
#search_optimal(visualize, show_images)


