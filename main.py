from typing import List

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


def sub_test(word_length: int, set_size: int):
    no_ngram_test = list()
    ngram_test = list()
    for i in range(set_size):

        # no ngram test
        test = "".join(random.choices(string.ascii_lowercase, k=word_length))
        start = tm()
        matches, distance = get_closest_word(test, 0, 1)
        stop = tm()
        no_ngram_test.append([test, matches, distance, stop - start])

        # ngram test
        start = tm()
        matches, distance = get_closest_word(test)
        stop = tm()
        ngram_test.append({"word": test, "matches": matches, "distance": distance, "time": stop - start})


def main_test():
    test_chart = list()
    for i in range(3, 10):
        test_chart.append(sub_test(i, 10))
    return test_chart


def save_chart(data: List[dict]):
    file = open(".output.csv", "w+")
    for i in data:
        prefix = f"len{len(i[0]['word'])}"
        for j in i:
            file.write(f"{prefix + j['word']};{j['matches']};{j['distance']};{j['time']}\n")


if __name__ == "__main__":
    while True:
        case = input("Select activity:\n1) Manual test\n2) Automatic test (fixed n-gram size):\n"
                     "3) Automatic test (fixed jaccard index requirement)\n4) Main test\nOther) Exit\n")
        if case == "1":
            manual_test(input("Insert word to match: "))
        elif case == "2":
            automated_test_2(input("Insert word to match: "))
        elif case == "3":
            automated_test_3(input("Insert word to match: "))
        elif case == "4":
            chart = main_test()
            save_chart()
        else:
            break
