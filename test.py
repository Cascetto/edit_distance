import matplotlib.pyplot as plt
import string
import random

from typing import List, Tuple
from edit_distance import *
from timeit import default_timer as tm


def list_to_string(l: list) -> str:
    result = ""
    for e in l:
        result += str(e)
    return result


def get_test_words(set_size: int = 1000) -> list:
    check_list = open("check_list.txt", "r")
    result = list()
    for line in check_list.readlines():
        result.append(line[:-1])
    set_size = set_size if set_size < len(result) else len(result)
    random.shuffle(result)
    return result[0: set_size]


def shuffle_letters(words: list):
    for i in range(len(words)):
        a = list(words[i])
        l = int(len(a)/2)
        nshuffle = random.randint(0, l)
        for _ in range(nshuffle):
            i = random.randint(0, len(a) - 2)
            a[i], a[i + 1] = a[i + 1] + a[i]
        words[i] = list_to_string(a)

# def manual_test(query: str):
#     n_gram_length = input("Insert the desired ngram length: ")
#     tolerance = input("Insert the match percentage of ngrams desired (> 0 and < 1): ")
#     start = tm()
#     get_closest_word(query, float(tolerance), int(n_gram_length))
#     stop = tm()
#     print(f"\nElapsed time {stop - start}")


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


def main_test():
    no_jaccard = list()
    jaccard = list()
    start = tm()
    for i in reversed(range(3, 11)):
        temp = sub_test(i, 1)
        no_jaccard.append(temp[0])
        jaccard.append(temp[1])
        print(tm() - start)
    return no_jaccard, jaccard


def save_chart(data: List[List[dict]], file_path: str, plot_type: str):
    filer = open(file_path, "w+")
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
    plt.xlabel("Length of words")
    plt.ylabel("Time to check")
    plt.plot(xaxis, yaxis)
    plt.title(plot_type)
    plt.show()
    filer.close()
