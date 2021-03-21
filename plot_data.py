from typing import IO

from matplotlib import pyplot as plt


LENGTH = 0
QUERY = 1
# remove first and last 2 characters from each entry
MATCHES = 2
CONTROLS = 3
TIME = 4


def plot_graph(file_path: str):
    xaxis = []
    yaxis_time = []
    yaxis_check = []
    yaxis_matchs = []

    file = open(file_path, "r")
    for line in file:
        line = line[0: len(line) - 2].split(";")
        xaxis.append(float(line[0]))
        yaxis_time.append(float(line[1]))
        yaxis_matchs.append(float(line[2]))
        yaxis_check.append(float(line[3]))
    file.close()

    plt.xlabel("Jaccard index threshold")

    plt.title("Ji/Time")
    plt.plot(xaxis, yaxis_time)
    plt.ylabel("Avarage computation time")
    plt.show()

    plt.title("Ji/Checks")
    plt.plot(xaxis, yaxis_check)
    plt.ylabel("Avarage number of word confronted")
    plt.show()

    plt.title("Ji/Matches")
    plt.plot(xaxis, yaxis_matchs)
    plt.ylabel("Avarage number of word found with minimum distance")
    plt.show()


if __name__ == "__main__":
    plot_graph("./data.csv")
