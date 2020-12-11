from typing import List, Tuple
import matplotlib.pyplot as plt

from edit_distance import *
from timeit import default_timer as tm
from os import path
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


def sub_test(word_length: int, set_size: int) -> Tuple[List[dict]]:
    no_ngram_test = list()
    ngram_test = list()
    for i in range(set_size):

        # no ngram test
        test = "".join(random.choices(string.ascii_lowercase, k=word_length))
        start = tm()
        matches, distance = get_closest_word(test, 0, 1)
        stop = tm()
        no_ngram_test.append({"word": test, "matches": matches, "distance": distance, "time": stop - start})

        # ngram test
        start = tm()
        matches, distance = get_closest_word(test, 0.33, 3)
        stop = tm()
        ngram_test.append({"word": test, "matches": matches, "distance": distance, "time": stop - start})

    return no_ngram_test, ngram_test


def main_test(start_point: int):
    no_jaccard = list()
    jaccard = list()
    next_iter = start_point
    for i in range(3, 10):
        next_iter = i + 1 if i != 9 else 0
        temp = sub_test(i, 100)
        no_jaccard.append(temp[0])
        jaccard.append(temp[1])
        if i != 10:
            resume = input(f"{i}-length word set completed, want to continue? (Y/n)")
            if resume == 'n':
                break
    filec = open("checkpoint.txt", 'w+')
    filec.write(str(next_iter))
    filec.close()
    return no_jaccard, jaccard


def save_chart(data: List[List[dict]], file_path: str, plot_type: str, new_chart: bool = True):
    filer = open(file_path, "w+" if new_chart else "a")
    xaxis = []
    yaxis = []
    for i in data:
        prefix = f"{len(i[0]['word'])}"
        avg_time = 0
        for j in i:
            filer.write(f"{prefix};{j['word']};{j['matches']};{j['distance']};{j['time']}\n")
            avg_time += j['time']
        avg_time /= len(i)
        xaxis.append(len(i[0]['word']))
        yaxis.append(avg_time)
    plt.plot(xaxis, yaxis)
    plt.title(plot_type)
    plt.show()
    filer.close()


if __name__ == "__main__":
    if path.exists("checkpoint.txt"):
        file = open("checkpoint.txt")
        index = file.readline()
        file.close()
        chart1, chart2 = main_test(int(index))
        save_chart(chart1, "./no_intersect.csv", "NO JACCARD INTERSECTION", int(index) <= 0)
        save_chart(chart2, "./intersect.csv", "JACCARD INTERSECTION ", int(index) <= 0)
    else:
        chart1, chart2 = main_test(0)
        save_chart(chart1, "./no_intersect.csv", "NO JACCARD INTERSECTION")
        save_chart(chart2, "./intersect.csv", "JACCARD INTERSECTION ")

