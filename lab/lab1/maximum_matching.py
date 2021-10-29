from utils import *

class trie_tree:
    def __init__(self):
        self.nex = []
        self.cnt = 0
        self.exist = []

    def insert(self, s, l): # 插入字符串
        p = 0
        for i in range(l):
            c = ord(s[i]) - ord('a')
            if self.nex[p][c] == 0:
                self.nex[p][c] = self.cnt # 如果没有，就添加结点
                self.cnt += 1
            p = self.nex[p][c]
        self.exist[p] = True

    def find(self, s, l): # 查找字符串
        p = 0
        for i in range(0, l):
            c = ord(s[i]) - ord('a')
            if self.nex[p][c] == 0:
                return False
            p = self.nex[p][c]
        return self.exist[p]


def maximum_matching(dic_path):
    maxlen = ''
    len_sum = 0
    with open(dic_path, 'r', encoding='utf-8') as f:
        lines = [l[:-1].split(' ') for l in f.readlines()]
    dict_ = remove_repeated_words([l[0] for l in lines])
    hash_base = get_hash_base(remove_repeated_words(get_single_words(dict_)))
    assert hash_base != -1
    se = set()
    for dic in dict_:
        len_sum += len(dic)
        if len(dic) > len(maxlen):
            maxlen = dic
        for x in dic:
            se.add(x)
    print(len_sum, maxlen, len(maxlen), len(se), len(dict_))
if __name__ == '__main__':
    maximum_matching('data_1/dic.txt')