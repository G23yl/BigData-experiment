import os
import re
from mythread import MyThread


def get_all_files_name(folder_name):
    files_name_list = []
    files = os.listdir(folder_name)
    for file in files:
        if file.endswith(".txt"):
            path = os.path.join(folder_name, file)
            files_name_list.append(path)
    return files_name_list


def read_file(file_handle):
    words_list = []
    for line in file_handle:
        line_list = re.findall(r"\b[a-zA-Z]+\b", line)
        for word in line_list:
            words_list.append(word.lower())
    return words_list


def mapper(folder_name, write_file_name):
    files_name_list = get_all_files_name(folder_name=folder_name)
    key_words_handle = open("./source_data/words.txt")
    key_words_hash = {}
    for key_word in key_words_handle:
        key_words_hash[key_word.strip().lower()] = 1
    with open(write_file_name, "w") as f:
        for file_name in files_name_list:
            file_handle = open(file_name)
            words_list = read_file(file_handle)
            for word in words_list:
                if key_words_hash.get(word) != None:
                    f.write(
                        "{},{}\n".format(
                            (file_name.split("/")[3].split(".")[0], word), 1
                        )
                    )


if __name__ == "__main__":
    threads = []
    folder_path_1 = "./source_data/folder_"
    result_path_1 = "./result/result"
    for i in range(1, 10):
        folder_path = folder_path_1 + str(i)
        result_path = result_path_1 + str(i) + ".txt"
        t = MyThread(mapper, (folder_path, result_path))
        threads.append(t)
    for i in range(9):
        threads[i].start()
    for i in range(9):
        threads[i].join()
    