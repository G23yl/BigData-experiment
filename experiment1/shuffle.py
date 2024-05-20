from mythread import MyThread

def shuffle(combine_name1: str, combine_name2: str, combine_name3: str, write_file_name):
    file1 = open(combine_name1)
    file2 = open(combine_name2)
    file3 = open(combine_name3)
    dict = {}
    for line in file1:
        temp = (line.split("'")[1], line.split("'")[3])
        cnt = int(line.strip().split(",")[2])
        if dict.get(temp) == None:
            dict[temp] = cnt
        else:
            dict[temp] += cnt
    for line in file2:
        temp = (line.split("'")[1], line.split("'")[3])
        cnt = int(line.strip().split(",")[2])
        if dict.get(temp) == None:
            dict[temp] = cnt
        else:
            dict[temp] += cnt
    for line in file3:
        temp = (line.split("'")[1], line.split("'")[3])
        cnt = int(line.strip().split(",")[2])
        if dict.get(temp) == None:
            dict[temp] = cnt
        else:
            dict[temp] += cnt
    with open(write_file_name, "w") as f:
        for key, value in dict.items():
            f.write("('{}', '{}'),{}\n".format(key[0], key[1], value))


if __name__ == "__main__":
    threads = []
    combine_path = "./result/combine"
    write_path_1 = "./result/shuffle"
    for i in range(1, 4):
        combine_path_1 = combine_path + str(i * 3 - 2) + ".txt"
        combine_path_2 = combine_path + str(i * 3 - 1) + ".txt"
        combine_path_3 = combine_path + str(i * 3) + ".txt"
        write_path = write_path_1 + str(i) + ".txt"
        t = MyThread(shuffle, (combine_path_1, combine_path_2, combine_path_3, write_path))
        threads.append(t)
    for i in range(3):
        threads[i].start()
    for i in range(3):
        threads[i].join()
