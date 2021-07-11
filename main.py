import test


if __name__ == "__main__":
    # t = test.main_test()
    # test.save_chart(t[0], "./nj.csv", "no jaccard")
    # test.save_chart(t[1], ".j.csv", "jaccard")
    test.bootstrap_3d_test(20)