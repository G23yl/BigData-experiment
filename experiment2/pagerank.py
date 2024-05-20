import numpy as np

def readfile(file_name: str):
    relation_dict = {}
    key_words = []
    file = open(file_name)
    for line in file:
        temp = {}
        key_word = line.strip().split(":")[0]
        link_to = line.strip().split(":")[1]
        key_words.append(key_word)
        for word in link_to.split(" "):
            temp[word] = 1
        relation_dict[key_word] = temp
    return key_words, relation_dict

def PageRank(M, beita = 0.8):
    page_rank_init = np.array(np.ones(M.shape[0]).T / M.shape[0])
    page_rank = page_rank_init
    beita_M = M * beita
    bias = page_rank_init * (1 - beita)
    while True:
        page_rank = np.dot(beita_M, page_rank_init) + bias
        error = np.sum(np.abs(page_rank - page_rank_init))
        if error < 1e-8:
            break
        page_rank_init = page_rank
    return page_rank


if __name__ == "__main__":
    (key_words, relation_dict) = readfile("./link_relation.txt")
    matrix = []
    for key in key_words:
        arr = []
        link_to = relation_dict[key]
        rank = len(link_to.keys())
        for i in range(len(key_words)):
            if link_to.get(key_words[i]) != None:
                arr.append(1 / rank)
            else:
                arr.append(0)
        matrix.append(arr)
    link_matrix = np.array(matrix).T
    page_rank = PageRank(link_matrix)   
    with open("./page_rank.txt", "w") as f:
        for i in range(len(key_words)):
            f.write("{}: {}\n".format(key_words[i], page_rank[i]))
