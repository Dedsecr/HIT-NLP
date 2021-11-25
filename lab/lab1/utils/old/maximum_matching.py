import numpy as np
from utils import *

class trie_tree:
    def __init__(self, dict_):
        # self.hash_base, self.max_code = get_hash_base(remove_repeated_ele(get_single_words(dict_)))
        self.hash_base, self.max_code = 5590, 8640
        self.nex = np.zeros((1, mod), dtype=np.int)
        self.exist = [False]

    def insert_words(self, words):
        i, s = 0, len(words)
        for word in words:
            self.insert(word)
            i+=1
            print(self.nex.shape, "{} / {}".format(i, s))

    def insert(self, word):
        p = 0 
        for w in word:
            c = hash(w, self.hash_base)
            if self.nex[p][c] == 0:
                self.nex = np.append(self.nex, np.zeros((1, mod), dtype=np.int), axis=0)
                self.nex[p][c] = self.nex.shape[0] - 1
                self.exist.append(False)
            p = self.nex[p][c]
        self.exist[p] = True

    def find(self, word):
        p = 0 
        for w in word:
            c = hash(w, self.hash_base)
            if self.nex[p][c] == 0:
                return False
            p = self.nex[p][c]
        return self.exist[p]


def maximum_matching(dic_path):
    with open(dic_path, 'r', encoding='utf-8') as f:
        lines = [l[:-1].split(' ') for l in f.readlines()]
        dict_ = remove_repeated_ele([l[0] for l in lines])
    trie_t = trie_tree(dict_)
    trie_t.insert_words(dict_)
    
if __name__ == '__main__':
    maximum_matching('data_1/dic.txt')