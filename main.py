import test


if __name__ == "__main__":
    words = test.get_test_words(20)
    test.shuffle_letters(words)
    t = test.main_test()
    test.save_chart(t[0], "./nj.csv", "no jaccard")
    test.save_chart(t[1], "./j.csv", "jaccard")