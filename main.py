import test


if __name__ == "__main__":
    words = test.get_test_words(10)
    test.shuffle_letters(words)
    test.main_test(3)
    print(words)
