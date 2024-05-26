import itertools
import numpy as np


def readfile(file_name: str):
    relation_list = []
    words = []
    file = open(file_name)
    for line in file:
        temp = {}
        key_word = line.strip().split(":")[0]
        link_to = line.strip().split(":")[1]
        words.append(key_word)
        if link_to != "":
            for word in link_to.split(" "):
                temp[word] = 1
        if temp.get(key_word) == None:
            temp[key_word] = 1
        relation_list.append(temp)
    return sorted(words), relation_list


class AssoRules:
    def __init__(self, file_name, threshold=0.15, conf=0.3):
        self.threshold = threshold
        self.conf = conf
        self.L0, self.relation = readfile(file_name)
        self.L1_dict = {} 
        self.L2_dict = {}
        self.L3_dict = {}
        self.L4_dict = {}
        self.L1 = []
        self.L2 = []
        self.L3 = []
        self.L4 = []
        self.num2 = 0
        self.num3 = 0
        self.num4 = 0

    def get_L1(self):
        return self.L1

    def get_L2(self):
        return self.L2

    def get_L3(self):
        return self.L3

    def get_L4(self):
        return self.L4

    def cal_support(self, x: set):
        support = 0
        for value in self.relation:
            if x.issubset(set(value)):
                support += 1
        return support

    # 生成k阶候选项集
    def Ck(self, k, L):
        ck_list = []
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                s = set(L[i]) | set(L[j])
                s = sorted(list(s))
                if len(s) == k and tuple(s) not in ck_list:
                    ck_list.append(tuple(s))
        return ck_list

    def first_order_freq_itemset(self):
        for it in self.L0:
            cnt = self.cal_support(set([it]))
            if cnt >= self.threshold * len(self.relation):
                self.L1_dict[it] = cnt
                self.L1.append(it)
        sorted(self.L1)

    def PCY(self):
        num_of_bucket = 990000
        bucket = np.zeros(num_of_bucket)    #统计每个桶次数
        bucket_dict = {}
        pass2_pair = set()
        vec = np.zeros(num_of_bucket)   #频繁桶为1
        for basket in self.relation:
            basket = sorted(list(basket.keys()))
            for pair in list(itertools.combinations(basket, 2)):
                idx = hash((hash(pair[0]) % num_of_bucket * hash(pair[1]) % num_of_bucket)) % num_of_bucket
                bucket[idx] += 1
                if bucket_dict.get(idx) == None:
                    bucket_dict[idx] = [pair]
                else:
                    bucket_dict[idx].append(pair)
        for i in range(num_of_bucket):
            if bucket[i] >= self.threshold * len(self.relation):
                vec[i] = 1
                pass2_pair = pass2_pair | set(bucket_dict[i])
        for pair in pass2_pair:
            s = self.cal_support(set(pair))
            if s >= self.threshold * len(self.relation):
                self.L2.append(pair)
                self.L2_dict[pair] = s
        # sorted(self.L2, key=lambda d: d[0])

    def high_order_freq_itemset(self, L_last, k):
        if k == 2:
            C = list(itertools.combinations(L_last, 2))
        else:
            C = self.Ck(k, L_last)  # k项生成
        # 获取每个k阶集的个数
        for tup in C:
            support = self.cal_support(set(tup))
            if support >= self.threshold * len(self.relation):
                if k == 2:
                    self.L2_dict[tup] = support
                    self.L2.append(tup)
                if k == 3:
                    self.L3_dict[tup] = support
                    self.L3.append(tup)
                if k == 4:
                    self.L4_dict[tup] = support
                    self.L4.append(tup)

    def generate_items(self):
        self.first_order_freq_itemset()
        # self.high_order_freq_itemset(self.L1, 2)
        self.PCY()
        self.high_order_freq_itemset(self.L2, 3)
        self.high_order_freq_itemset(self.L3, 4)

    def assorules(self):
        with open("./rules.txt", "w") as f:
            # L2关系
            for tup in self.L2:
                items = set(tup)
                s_items = self.L2_dict[tup]
                for i in tup:
                    j = items - set([i])
                    s_j = self.L1_dict[tuple(j)[0]]
                    if s_items / s_j >= self.conf:
                        f.write(f"{j} -> {set([i])}\n")
                        self.num2 += 1
            # L3关系
            for tup in self.L3:
                items = set(tup)
                s_items = self.L3_dict[tup]
                for i in tup:
                    # 2 -> 1
                    j = items - set([i])
                    s_j = self.L2_dict[tuple(sorted(list(j)))]
                    if s_items / s_j >= self.conf:
                        f.write(f"{j} -> {set([i])}\n")
                        self.num3 += 1
                    # 1 -> 2
                    s_i = self.L1_dict[tuple([i])[0]]
                    if s_items / s_i >= self.conf:
                        f.write(f"{set([i])} -> {j}\n")
                        self.num3 += 1
            # L4关系
            for tup in self.L4:
                items = set(tup)
                s_items = self.L4_dict[tup]
                for i in tup:
                    # 3 -> 1
                    j = items - set([i])
                    s_j = self.L3_dict[tuple(sorted(list(j)))]
                    if s_items / s_j >= self.conf:
                        f.write(f"{j} -> {set([i])}\n")
                        self.num4 += 1
                    # 1 -> 3
                    s_i = self.L1_dict[tuple([i])[0]]
                    if s_items / s_i >= self.conf:
                        f.write(f"{set([i])} -> {j}\n")
                        self.num4 += 1
                # 2 -> 2
                for i in range(4):
                    for j in range(i + 1, 4):
                        x = set([tup[i], tup[j]])
                        y = items - x
                        s_y = self.L2_dict[tuple(sorted(list(y)))]
                        if s_items / s_y >= self.conf:
                            f.write(f"{y} -> {x}\n")
                            self.num4 += 1


if __name__ == "__main__":
    # 获取L0和1000个篮子
    ass = AssoRules("./link_relation.txt")
    ass.generate_items()
    ass.assorules()