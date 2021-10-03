import os
import shutil


def rename_base_folders():
    female_folder_path = "./../../Desktop/SPBU/biometrics/code/faces94/female"
    male_folder_path = "./../../Desktop/SPBU/biometrics/code/faces94/male"

    dst = "./face_base/"

    # reenumerate female folders
    for folder in os.listdir(female_folder_path):
        os.renames(os.path.join(female_folder_path, folder), os.path.join(female_folder_path, str(int(folder) + 113)))

    # rename x.jpg to y_x.jpg
    for folder in os.listdir(female_folder_path):

        for file in os.listdir(os.path.join(female_folder_path, folder)):
            new_file_name = folder + "_" + file
            old_name = female_folder_path + "/" + folder + "/" + file
            new_name = female_folder_path + "/" + folder + "/" + new_file_name
            os.rename(old_name, new_name)

    # copy to folder in repository
    for folder in os.listdir(female_folder_path):
        for file in os.listdir(os.path.join(female_folder_path, folder)):
            file_to_copy = female_folder_path + "/" + folder + "/" + file
            shutil.copy(file_to_copy, dst)

    #  handle female photos

    # rename 20 male folders x.jpg to y_x.jpg
    for folder in os.listdir(male_folder_path):
        if 19 < int(folder) < 41:
            for file in os.listdir(os.path.join(male_folder_path, folder)):
                new_file_name = folder + "_" + file
                old_name = male_folder_path + "/" + folder + "/" + file
                new_name = male_folder_path + "/" + folder + "/" + new_file_name
                os.rename(old_name, new_name)
                # print("old name: " + old_name)
                # print("new_name: " + new_name)
                # print()

    # copy to folder in repository
    for folder in os.listdir(male_folder_path):
        if 19 < int(folder) < 41:
            for file in os.listdir(os.path.join(male_folder_path, folder)):
                file_to_copy = male_folder_path + "/" + folder + "/" + file
                shutil.copy(file_to_copy, dst)
