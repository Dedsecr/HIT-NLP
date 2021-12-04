# -*- coding: utf-8 -*-

from utils import *

class Dict_unigram:
    def __init__(self, SEG_POS_path, DICT_path):
        self.SEG_POS_path = SEG_POS_path
        self.DICT_path = DICT_path
        self.words = {}
        self.max_len = 0

    def get_dict(self):
        with open(self.SEG_POS_path, 'r') as f:
            lines = [l.strip().split() for l in f.readlines()]
        segs = [l[i] for l in lines for i in range(1, len(l))]
        for seg in segs:
            if '/m' in seg or len(seg) == 0: continue
            word = seg[1 if seg[0] == '[' else 0 : seg.index('/')]
            if word not in self.words:
                self.words[word] = 1
            else:
                self.words[word] += 1
            self.max_len = max(len(word), self.max_len)
        self._save_dict()
    
    def _save_dict(self):
        with open(self.DICT_path, 'w', encoding='utf8') as f:
            for word in self.words:
                f.write('{} {}\n'.format(word, self.words[word]))


if __name__ == '__main__':
    dict = Dict_unigram(DATA_TRAIN_POS, DICT_UNIGRAM)
    dict.get_dict()