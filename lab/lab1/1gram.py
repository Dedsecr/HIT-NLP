from utils import *

class Word_1_gram:
    def __init__(self, word, cnt):
        self.word = word
        self.cnt = cnt

class Gram_1:
    def __init__(self, SEG_POS_path, DICT_path):
        self.SEG_POS_path = SEG_POS_path
        self.DICT_path = DICT_path
        self._read_dict()
    
    def _read_dict(self):
        with open(self.DICT_path, 'r', encoding='utf8') as f:
            lines = [l.strip().split() for l in f.readlines()]
        self.dict = [Word_1_gram(l[0], int(l[1])) for l in lines]
        self.max_len = max([len(w.word) for w in self.dict])
    
    def get_DAG(self, word):
        DAG = {}
        for r in range(len(word)):
            for l in range(max(r - self.max_len, 0), r + 1):
                print(l, r)
        #     for j in range(r + 1, len(word) + 1):
        #         if word[r:j] in self.dict:
        #             DAG[r] = j
        # return DAG

if __name__ == '__main__':
    dict = Gram_1(DATA_SEG_POS, DICT_1GRAM)
    dict.get_DAG('计算机')