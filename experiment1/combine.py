from mythread import MyThread

def combine(result_file_name, write_file_name):
    dict = {}
    file = open(result_file_name)
    for line in file:
        temp = (line.split("'")[1], line.split("'")[3])
        if dict.get(temp) == None:
            dict[temp] = 1
        else:
            dict[temp] += 1
    with open(write_file_name, "w") as f:
        for key, value in dict.items():
            f.write("('{}', '{}'),{}\n".format(key[0], key[1], value))
        

if __name__ == "__main__":
    threads = []
    result_path_1 = "./result/result"
    write_path_1 = "./result/combine"
    for i in range(1, 10):
        result_path = result_path_1 + str(i) + ".txt"
        write_path = write_path_1 + str(i) + ".txt"
        t = MyThread(combine, (result_path, write_path))
        threads.append(t)
    for i in range(9):
        threads[i].start()
    for i in range(9):
        threads[i].join()