import os
from utils import *
import matplotlib.pyplot as plt

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


def search(method,p, **kwargs):
    fail = 0
    success = 0
    num_of_test = []
    percentage = []

    images = next(os.walk(f"{PATH}/ATT_run/test"))[2]

    if kwargs.get("visualize"):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        graph, = ax.plot([], [])
        ax.set_xlim([0, len(images)])
        ax.set_ylim([0, 105])
        plt.xlabel('Number of tests')
        plt.ylabel('Percentage of success')
        plt.title(f'Method: {method.upper()}')
        plt.ion()
        plt.show()

    for image in images:
        result = []

        persons = next(os.walk("./ATT_run/"))[1]
        for person in persons:
            if person == "test":
                continue

            standards = next(os.walk(f"./ATT_run/{person}"))[2]
            for standard in standards:
                result.append(
                    {
                        "score": compare_images(f"{PATH}/ATT_run/test/{image}",
                                                f"{PATH}/ATT_run/{person}/{standard}", p,
                                                method=method),
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

        if kwargs.get("visualize"):
            graph.set_data(num_of_test, percentage)
            plt.pause(WAIT_TIME)

    t_num = int((fail + success) / 40)
    p_num = int(10 - t_num)
    success_proc = round(success / (fail + success) * 100, 2)

    if method == "Histogram":
        print(f"ORL(40, {p_num}, {t_num}, CV) "+f"[{method}: 112*92->{BIN} /L1/ "+f"{success_proc}%] \n")
    if method == "Scale":
        print(f"ORL(40, {p_num}, {t_num}, CV) " + f"[{method}: 112*92->{M}*{N} /L1/ " + f"{success_proc}%] \n")
    if method == "DCT":
        print(f"ORL(40, {p_num}, {t_num}, CV) " + f"[{method}: 112*92->{p}(zigzag) /L1/ " + f"{success_proc}%] \n")
    if method == "DFT":
        print(f"ORL(40, {p_num}, {t_num}, CV) " + f"[{method}: 112*92->{p}(zigzag) /L1/ " + f"{success_proc}%] \n")
    if method == "Gradient":
        print(f"ORL(40, {p_num}, {t_num}, CV) " + f"[{method}: 112*92-> W={w}, step={st} /L1/ " + f"{success_proc}%] \n")
        #print(f"ORL(40, {p_num}, {t_num}, CV) " + f"[{method}:" + f"{success_proc}%] \n")
    #print(f"method: {method}")
    #print(f"fail: {fail}")
    #print(f"success: {success}")
    #print(f"percentage of success: {success / (fail + success) * 100}\n")


def search_optimal(visualize, show_images):
    fail = 0
    success = 0
    num_of_test = []
    percentage = []

    images = next(os.walk(f"{PATH}/ATT_run/test"))[2]

    if visualize:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        graph, = ax.plot([], [])
        ax.set_xlim([0, len(images)])
        ax.set_ylim([0, 105])
        plt.xlabel('Number of tests')
        plt.ylabel('Percentage of success')
        plt.title('Parallel FARES')
        plt.ion()
        fig.canvas.manager.window.move(650, 400)
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
            test_img = cv.imread(f"{PATH}/ATT_run/test/{image}")
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
                                                    f"{PATH}/ATT_run/{person}/{standard}",
                                                    method=method),
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
                img = cv.imread(f"{PATH}/ATT/{internal_answer}_1.png")
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
            plt.pause(WAIT_TIME)

    print("Optimal method")
    print(f"fail: {fail}")
    print(f"success: {success}")
    print(f"percentage of success: {success / (fail + success) * 100}\n")
