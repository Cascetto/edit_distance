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


def get_test_words(word_length: int, set_size: int = 1000) -> list:
    check_list = open("lexicon.txt", "r")
    result = list()
    for line in check_list.readlines():
        len(line[:-1]) == word_length and result.append(line[:-1])
    set_size = set_size if set_size < len(result) else len(result)
    random.shuffle(result)
    return result[0: set_size]


def shuffle_letters(words: list):
    for i in range(len(words)):
        a = list(words[i])
        l = int(len(a)/3)
        nshuffle = random.randint(0, l)
        for _ in range(nshuffle):
            j = random.randint(0, len(a) - 2)
            a[j], a[j + 1] = a[j + 1] + a[j]
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


def sub_test(word_length: int, set_size: int):
    no_ngram_test = list()
    ngram_test = list()

    word_list = get_test_words(word_length, set_size)
    shuffle_letters(word_list)

    for word in word_list:

        test = word
        # no ngram test
        # start = tm()
        # matches, check = get_closest_word(test, 0, 1)
        # stop = tm()
        # no_ngram_test.append({"word": test, "matches": matches, "check": check, "time": stop - start})
        #
        # # ngram test
        # start = tm()
        # matches, check = get_closest_word(test, 0.33, 2)
        # stop = tm()
        # ngram_test.append({"word": test, "matches": matches, "check": check, "time": stop - start})

        start = tm()
        matches, check = get_closest_word(test, 0.66, 2)
        stop = tm()
        ngram_test.append({"word": test, "matches": matches, "check": check, "time": stop - start})

    return no_ngram_test, ngram_test


def main_test():
    no_jaccard = list()
    jaccard = list()
    start = tm()
    for i in reversed(range(3, 11)):
        temp = sub_test(i, 10)
        no_jaccard.append(temp[0])
        jaccard.append(temp[1])
        print(tm() - start)
    return no_jaccard, jaccard


def save_chart(data: List[List[dict]], file_path: str, plot_type: str):
    filer = open(file_path, "w+")
    xaxis = []
    ytime = []
    ynum_of_matches = []
    for i in data:
        prefix = f"{len(i[0]['word'])}"
        avg_time = 0
        num_of_match = 0
        for j in i:
            filer.write(f"{prefix};{j['word']};{j['check']};{j['time']}\n")
            avg_time += j['time']
            num_of_match += j['check']
        avg_time /= (l := len(i))
        num_of_match /= l
        xaxis.append(len(i[0]['word']))
        ytime.append(avg_time)
        ynum_of_matches.append(num_of_match)
    filer.close()
    plt.xlabel("Length of words")
    plt.ylabel("Time to check")
    plt.plot(xaxis, ytime)
    plt.title(plot_type)
    plt.show()

    plt.xlabel("Length of words")
    plt.ylabel("Number of matches")
    plt.plot(xaxis, ynum_of_matches)
    plt.title(plot_type)
    plt.show()
