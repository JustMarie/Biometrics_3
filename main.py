from barcode_lab.barcode_utils import *

if __name__ == '__main__':
    path_to_image = "./face_base/1_1.jpg"
    path_to_image_same = "./face_base/1_2.jpg"
    path_to_image_another = "./face_base/11_1.jpg"
    calc_hist_from_image(path_to_image)

    create_ean_barcode(path_to_image)
