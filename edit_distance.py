from math import inf


def edit_distance(x: str, y: str, cost: dict = None) -> int:
    if cost is None or cost.keys():
        cost = {'copy': 0, 'replace': 1, 'twiddle': 1, 'insert': 1, 'delete': 1}
    m = len(x) + 1
    n = len(y) + 1

    distance = [inf] * (m * n)
    distance[0] = 0
    operation = ["None"] * (m * n)

    for i in range(1, m):
        distance[i * n] = cost['delete'] * i
        operation[i * n] = f"Delete {x[i - 1]}"

    for j in range(1, n):
        distance[j] = cost['insert'] * j
        operation[j] = f"Insert {y[j - 1]}"

    for i in range(1, m):
        for j in range(1, n):
            if x[i - 1] == y[j - 1]:
                distance[i * n + j] = distance[(i - 1) * n + (j - 1)] + cost['copy']
                operation[i * n + j] = f"Copy {x[i - 1]}"
            if x[i - 1] != y[j - 1] and distance[(i - 1) * n + (j - 1)] + cost['replace'] < distance[i * n + j]:
                distance[i * n + j] = distance[(i - 1) * n + (j - 1)] + cost['replace']
                operation[i * n + j] = f"Replace {x[i - 1]} with {y[j - 1]}"
            if x[i - 1] == y[j - 2] and x[i - 2] == y[j - 1] and j > 2 and i > 2 \
                    and distance[(i - 2) * n + (j - 2)] + cost['twiddle'] < distance[i * n + j]:
                distance[i * n + j] = distance[(i - 2) * n + (j - 2)] + cost['twiddle']
                operation[i * n + j] = f"Twiddle {x[i - 1]} and {y[j - 1]}"
            if distance[(i - 1) * n + j] + cost['delete'] < distance[i * n + j]:
                distance[i * n + j] = distance[(i - 1) * n + j] + cost['delete']
                operation[i * n + j] = f"Delete {x[i - 1]}"
            if distance[i * n + (j - 1)] + cost['insert'] < distance[i * n + j]:
                distance[i * n + j] = distance[i * n + (j - 1)] + cost['insert']
                operation[i * n + j] = f"Insert {y[j - 1]}"

    # print_matrix(distance, m, n)
    # print_matrix(operation, m, n)

    return distance[m * n - 1]


def print_matrix(matrix, m, n):
    for i in range(m):
        print(matrix[i * n: (i + 1) * n])


def get_ngrams(x, length: int = 2) -> set:
    l = len(x)
    if l <= length:
        return [x]

    ngrams = []
    for i in range(l - length + 1):
        ngrams.append(x[i: i + length])
    return set(ngrams)


def get_closest_word(query: str, lexicon_path: str = "./lexicon.txt") -> list:
    min_distance = inf
    closest = list
    lexicon = open(lexicon_path, 'r')
    n1 = get_ngrams(query)
    for word in lexicon:
        word = word.replace("\n", "")
        n2 = get_ngrams(word)
        if len(n1.intersection(n2)) / len(n1.union(n2)) >= 0.6:
            distance = edit_distance(query, word)
            if distance < min_distance:
                closest = [word]
                min_distance = distance
            elif min_distance == distance:
                closest.append(word)
    return closest
