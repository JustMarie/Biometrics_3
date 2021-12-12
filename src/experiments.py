import os
from utils import *
import matplotlib.pyplot as plt
from matplotlib import gridspec

PATH = os.getcwd()

WAIT_TIME = 0.001  # between image processing

methods = ["Histogram", "DFT", "DCT", "Scale", "Gradient"]

method_weight = {  # weights for LAB №4
    "Histogram": 0.3,
    "DFT": 0.15,
    "DCT": 0.15,
    "Scale": 0.3,
    "Gradient": 0.1
}


def search(method, visualize, params):
    fail = 0
    success = 0
    num_of_standards = 0
    num_of_test = []
    percentage = []

    #  images for test ( тестовая выборка )
    images = next(os.walk(f"{PATH}/ATT_run/test"))[2]

    if visualize:
        fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20, 5))
        graph, = ax[0].plot([], [])
        ax[0].set_xlim([0, len(images)])
        ax[0].set_ylim([0, 105])
        ax[0].set_xlabel('Number of tests')
        ax[0].set_ylabel('Percentage of success')
        ax[0].set_title(f'Method: {method.upper()}')
        plt.ion()
        plt.show()

    for image in images:
        result = []

        persons = next(os.walk("./ATT_run/"))[1]
        for person in persons:
            if person == "test":
                continue

            # эталоны
            standards = next(os.walk(f"./ATT_run/{person}"))[2]
            if num_of_standards == 0:
                num_of_standards = len(standards)
            for standard in standards:
                result.append(
                    {
                        "score": compare_images(f"{PATH}/ATT_run/test/{image}",
                                                f"{PATH}/ATT_run/{person}/{standard}", method, params),
                        "path": f"{PATH}/ATT_run/{person}/{standard}",
                        "answer": person,
                    }
                )

        result.sort(key=lambda a: a["score"], reverse=True)
        answer = result[0]["answer"]

        if image.split("_")[0] == answer:
            success += 1
        else:
            fail += 1

        num_of_test.append(success + fail)
        percentage.append(success / (fail + success) * 100)

        if visualize:
            graph.set_data(num_of_test, percentage)

            img_search = np.float32(cv.imread(f"{PATH}/ATT_run/test/{image}", 0))
            ax[1].imshow(img_search, cmap='gray')
            ax[1].set_title("Sample")

            img_res = np.float32(cv.imread(result[0]["path"], 0))
            ax[2].imshow(img_res, cmap='gray')
            ax[2].set_title("Result")
            plt.pause(WAIT_TIME)

    test_num = 10 - num_of_standards
    success_proc = round(success / (fail + success) * 100, 2)

    if method == "Histogram":
        print(
            f"ORL(40, {num_of_standards}, {test_num}, CV) " + f"[{method}: 112*92->{params['BIN']} /L1/ " + f"{success_proc}%] \n")
    if method == "Scale":
        print(
            f"ORL(40, {num_of_standards}, {test_num}, CV) " + f"[{method}: 112*92->{params['M']}*{params['N']} /L1/ " + f"{success_proc}%] \n")
    if method == "DCT":
        print(
            f"ORL(40, {num_of_standards}, {test_num}, CV) " + f"[{method}: 112*92->{params['p']}(zigzag) /L1/ " + f"{success_proc}%] \n")
    if method == "DFT":
        print(
            f"ORL(40, {num_of_standards}, {test_num}, CV) " + f"[{method}: 112*92->{params['p']}(zigzag) /L1/ " + f"{success_proc}%] \n")
    if method == "Gradient":
        print(
            f"ORL(40, {num_of_standards}, {test_num}, CV) " + f"[{method}: 112*92-> W={params['w']}, step={params['st']} /L1/ " + f"{success_proc}%] \n")


def search_optimal_one_method(method):
    params = dict(p=0, br_px=False, BIN=0, M=0, N=0, w=0, st=0)
    hist_params = [8, 16, 32, 64, 128]
    scale_params = [[12, 10], [14, 12], [16, 13], [18, 15], [20, 16], [20, 18], [22, 18]]

    if method == "Histogram":

        for i in hist_params:
            params.update(BIN=i)
            search("Histogram", True, params)

    elif method == "DCT":

        print("Without bright pixel")
        for i in range(4, 29, 4):
            params.update(p=i)
            search("DCT", True, params)

        print("With bright pixel")
        for i in range(4, 29, 4):
            params.update(p=i, br_px=True)
            search("DCT", True, params)

    elif method == "DFT":

        print("Without bright pixel")
        for i in range(28, 30, 4):
            params.update(p=i)
            search("DFT", True, params)

        print("With bright pixel")
        for i in range(28, 30, 4):
            params.update(p=i, br_px=True)
            search("DFT", False, params)

    elif method == "Scale":

        for i in scale_params:
            params.update(M=i[0], N=i[1])
            search("Scale", False, params)

    elif method == "Gradient":

        for st in range(3, 16, 4):
            for w in range(5, 31, 5):
                params.update(w=w, st=st)
                search("Gradient", False, params)


def search_optimal_all_methods(visualize, show_images, params):
    fail = 0
    success = 0
    num_of_test = []
    percentage = []

    images = next(os.walk(f"{PATH}/ATT_run/test"))[2]

    if visualize:
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # graph, = ax.plot([], [])
        # ax.set_xlim([0, len(images)])
        # ax.set_ylim([0, 105])
        # plt.xlabel('Number of tests')
        # plt.ylabel('Percentage of success')
        # plt.title('Parallel FARES')
        # plt.ion()
        # # plt.get_current_fig_manager().window.setGeometry(0, 0, 650, 400)
        # # fig.canvas.manager.window.move
        # # fig.canvas.manager.window.move(650, 400)
        # plt.show()

        fig = plt.figure()

        ax = fig.add_subplot(111)
        graph, = ax.plot([], [])
        ax.set_xlim([0, len(images)])
        ax.set_ylim([0, 105])
        plt.xlabel('Number of tests')
        plt.ylabel('Percentage of success')
        plt.title('Parallel FARES')
        plt.ion()
        # plt.get_current_fig_manager().window.setGeometry(0, 0, 650, 400)
        # fig.canvas.manager.window.move
        # fig.canvas.manager.window.move(650, 400)
        plt.show()

    if show_images:
        cv.namedWindow("TEST IMAGE", cv.WINDOW_NORMAL)
        cv.moveWindow("TEST IMAGE", 0, 0)
        cv.resizeWindow("TEST IMAGE", 300, 300)

        for idx, method in enumerate(methods):
            cv.namedWindow(f"{method.upper()} ANSWER", cv.WINDOW_NORMAL)
            cv.resizeWindow(f"{method.upper()} ANSWER", 300, 300)
            cv.moveWindow(f"{method.upper()} ANSWER", (idx + 1) * 300 + 150, 0)

    for image in images:
        if show_images:
            test_img = cv.imread(f"{PATH}/ATT_run/test/{image}", 0)
            cv.imshow("TEST IMAGE", test_img)
        result = {}

        for method in methods:
            internal_result = []
            persons = next(os.walk("./ATT_run/"))[1]
            for person in persons:
                if person == "test":
                    continue

                standards = next(os.walk(f"./ATT_run/{person}"))[2]
                for standard in standards:
                    internal_result.append(
                        {
                            "score": compare_images(f"{PATH}/ATT_run/test/{image}",
                                                    f"{PATH}/ATT_run/{person}/{standard}", method, params),
                            "path": f"{PATH}/ATT_run/{person}/{standard}",
                            "answer": person,
                        }
                    )

            internal_result.sort(key=lambda a: a["score"], reverse=True)
            internal_answer = internal_result[0]["answer"]

            if internal_answer not in result:
                result[internal_answer] = method_weight[method]
            else:
                result[internal_answer] += method_weight[method]

            if show_images:
                img = cv.imread(f"{PATH}/ATT/{internal_answer}_1.png", 0)
                cv.imshow(f"{method.upper()} ANSWER", img)

        answer = max(result, key=result.get)

        if image.split("_")[0] == answer:
            success += 1
        else:
            fail += 1

        num_of_test.append(success + fail)
        percentage.append(success / (fail + success) * 100)

        if visualize:
            graph.set_data(num_of_test, percentage)
            plt.draw()
            plt.pause(WAIT_TIME)

    print("Optimal method")
    print(f"fail: {fail}")
    print(f"success: {success}")
    print(f"percentage of success: {success / (fail + success) * 100}\n")
