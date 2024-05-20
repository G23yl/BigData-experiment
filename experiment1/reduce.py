from mythread import MyThread


def reducer(shuffle_name):
    hash_dict = {}
    link_dict = {}
    file1 = open(shuffle_name)
    for line in file1:
        word = line.split("'")[3]
        temp = line.split("'")[1]
        cnt = int(line.strip().split(",")[2])
        if link_dict.get(temp) == None:
            link_dict[temp] = {word: 1}
        else:
            link_dict[temp][word] = 1

        if hash_dict.get(word) == None:
            hash_dict[word] = cnt
        else:
            hash_dict[word] += cnt
    return hash_dict, link_dict


if __name__ == "__main__":
    shuffle_path1 = "./result/shuffle"
    threads = []
    for i in range(1, 4):
        shuffle_path = shuffle_path1 + str(i) + ".txt"
        t = MyThread(reducer, (shuffle_path,))
        threads.append(t)
    for i in range(3):
        threads[i].start()
    for i in range(3):
        threads[i].join()
    dict_total = {}
    for i in range(3):
        (d, _) = threads[i].get_result()
        for key, value in d.items():
            if dict_total.get(key) == None:
                dict_total[key] = value
            else:
                dict_total[key] += value
    # 获取前1000个单词
    words_list = [
        tup[0]
        for tup in sorted(dict_total.items(), key=lambda d: d[1], reverse=True)[:1000]
    ]
    words_dict = {word: 1 for word in words_list}
    with open("./result/reduce_1000.txt", "w") as f:
        for i in range(1000):
            f.write("{}\n".format(words_list[i]))

    # 获取跳转关系
    link_relation = {}
    for i in range(3):
        (_, link) = threads[i].get_result()
        for word in words_list:
            if link.get(word) == None and link_relation.get(word) == None:
                link_relation[word] = {}
            elif link.get(word) != None and link_relation.get(word) == None:
                link_relation[word] = {}
                for key, value in link[word].items():
                    if words_dict.get(key) != None:
                        link_relation[word][key] = value
            elif link.get(word) != None and link_relation.get(word) != None:
                link_in_words = {}
                for key, value in link[word].items():
                    if words_dict.get(key) != None:
                        link_in_words[key] = value
                link_relation[word] = link_relation[word] | link_in_words

    with open("./result/link_relation.txt", "w") as f:
        for word in words_list:
            f.write("{}:".format(word))
            wdict = link_relation[word]
            for key, _ in wdict.items():
                f.write("{} ".format(key))
            f.write("\n")
