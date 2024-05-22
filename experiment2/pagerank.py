import numpy as np
import pandas as pd


def readfile(file_name: str):
    relation_dict = {}
    key_words = []
    file = open(file_name)
    for line in file:
        temp = {}
        key_word = line.strip().split(":")[0]
        link_to = line.strip().split(":")[1]
        key_words.append(key_word)
        if link_to != "":
            for word in link_to.split(" "):
                temp[word] = 1
        relation_dict[key_word] = temp
    return sorted(key_words), relation_dict


def PageRank(M, beita=0.8):
    N = M.shape[0]
    r0 = np.full((N, 1), 1 / N, dtype=float)
    bias = (1 - beita) / N * np.ones((N, 1), dtype=float)
    while True:
        print(np.sum(r0))
        temp = r0
        r0 = beita * np.dot(M, r0) + bias
        error = np.sum(np.abs(temp - r0))
        if error < 1e-08:
            break
    return r0


if __name__ == "__main__":
    (key_words, relation_dict) = readfile("./link_relation.txt")
    matrix = pd.DataFrame(np.zeros((len(key_words), len(key_words))), index=key_words, columns=key_words, dtype=float)
    # matrix = np.zeros((1000, 1000), dtype=float)
    for i in range(len(key_words)):
        link_to = relation_dict[key_words[i]]
        for j in range(len(key_words)):
            if link_to.get(key_words[j]) != None:
                matrix[key_words[j]][key_words[i]] = 1
                # matrix.loc[key_words[j], key_words[i]] = 1.0
    matrix = matrix.div(matrix.sum(axis=0), axis=1)
    matrix = matrix.fillna(0)
    # for i in range(len(key_words)):
    #     sum = np.sum(matrix[i])
    #     if sum != 0:
    #         matrix[i] /= sum
    # matrix = matrix.T
    page_rank = PageRank(matrix)
    print(np.sum(page_rank))
    with open("./page_rank.txt", "w") as f:
        for i in range(len(key_words)):
            f.write(f"{key_words[i]}: {page_rank[i][0]}\n")
