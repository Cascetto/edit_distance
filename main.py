import matplotlib.pyplot as plt

from edit_distance import *
from timeit import default_timer as tm
import string
import random


def manual_test(query: str):
    n_gram_length = input("Insert the desired ngram length: ")
    tolerance = input("Insert the match percentage of ngrams desired (> 0 and < 1): ")
    start = tm()
    get_closest_word(query, float(tolerance), int(n_gram_length))
    stop = tm()
    print(f"\nElapsed time {stop - start}")


def automated_test_2(query: str):
    steps = [x / 100 for x in range(1, 99)]
    timechart = list()
    for index in steps:
        start = tm()
        match, checks = get_closest_word(query, index_required=index)
        stop = tm()
        timechart.append([index, stop - start, checks, match])
    for entry in timechart:
        print(entry)


def automated_test_3(query: str):
    wlen = len(query)
    timechart = list()
    for l in range(wlen):
        start = tm()
        match, checks = get_closest_word(query, 0.66, l)
        stop = tm()
        timechart.append([l, stop - start, checks, match])
    return timechart


def sub_test(word_length: int, set_size: int) -> list:
    result = [[] for _ in range(101)]
    for i in range(set_size):
        test = "".join(random.choices(string.ascii_lowercase, k=word_length))
        for threshold in range(101):
            start = tm()
            matches, checks = get_closest_word(test, threshold / 100, 2)
            stop = tm()
            result[threshold].append({"word": test, "matches": matches, "checks": checks, "time": stop - start})
        print(f"\nWord {i + 1} done\n")
    return result


def main_test():
    return sub_test(8, 100)


# xaxis = jaccard threshold
# yaxis = time, number of matchs, umber of check


def save_chart(data: list, file_path: str):
    file = open(file_path, "w+")
    for threshold_index in range(len(data)):
        time = 0
        ncheck = 0
        nmatch = 0
        for word_index in range(len(data[threshold_index])):
            time += data[threshold_index][word_index]['time']
            ncheck += data[threshold_index][word_index]['checks']
            nmatch += len(data[threshold_index][word_index]['matches'])
        time /= (len(data[threshold_index]) if len(data[threshold_index]) != 0 else 1)
        nmatch /= (len(data[threshold_index]) if len(data[threshold_index]) != 0 else 1)
        ncheck /= (len(data[threshold_index]) if len(data[threshold_index]) != 0 else 1)
        file.write(f"{threshold_index / 100};{time};{nmatch};{ncheck}\n")
    file.close()


if __name__ == "__main__":
    # while True:
    #     case = input("Select activity:\n1) Manual test\n2) Automatic test (fixed n-gram size):\n"
    #                  "3) Automatic test (fixed jaccard index requirement)\n4) Main test\nOther) Exit\n")
    #     if case == "1":
    #         manual_test(input("Insert word to match: "))
    #     elif case == "2":
    #         automated_test_2(input("Insert word to match: "))
    #     elif case == "3":
    #         automated_test_3(input("Insert word to match: "))
    #     elif case == "4":
    #         chart = main_test()
    #         save_chart(chart)
    #     else:
    #         break
    chart = main_test()
    save_chart(chart, "./data.csv")
