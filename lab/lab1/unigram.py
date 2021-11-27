# coding:utf-8
import re
import math

from utils import *
from evaluation import *

class Unigram:
    def __init__(self, SEG_POS_path, DICT_path):
        del_old_file(UNI_SEG)
        self.SEG_POS_path = SEG_POS_path
        self.DICT_path = DICT_path
        self._read_dict()
    
    def _read_dict(self):
        with open(self.DICT_path, 'r', encoding='utf8') as f:
            lines = [l.strip().split() for l in f.readlines()]
        self.dict = {l[0]: int(l[1]) for l in lines}
        self.max_len = max([len(w) for w in self.dict])
        self.dict_total = len(self.dict)
    
    def _get_DAG(self, word):
        DAG = {}
        for r in range(len(word)):
            DAG[r] = [r]
            for l in range(max(r - self.max_len, 0), r):
                if word[l:r + 1] in self.dict:
                    DAG[r].append(l)
        return DAG
    
    def Unigram(self):
        f_res = open(UNI_SEG, 'w', encoding='utf8')
        with open(self.SEG_POS_path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
        for line in lines:
            now_line, last_pos = [], 0
            for i in re.finditer(r'[，。；！？]', line):
                now_line.append((line[last_pos: i.start()], i.group()))
                last_pos = i.start() + 1
            now_line.append((line[last_pos:], ''))
            for sequence in now_line:
                word, flag = sequence
                if len(word) == 0: 
                    if flag != '': f_res.write(flag + '/ ')
                    continue
                DAG = self._get_DAG(word)
                route = self._calc_unigram(word, DAG)
                segs = self._get_segs(word, route)
                segs = post_process(segs)
                f_res.write('/ '.join(segs) + '/ ')
                if flag != '': f_res.write(flag + '/ ')
            f_res.write('\n')
        f_res.close()
    
    def _calc_unigram(self, sequence, DAG):
        len_seq = len(sequence)
        log_total = math.log(self.dict_total)
        route = [(0, 0)] * len_seq
        for i in range(len_seq):
            route[i] = max([(math.log(1 if sequence[x: i + 1] not in self.dict else self.dict[sequence[x: i + 1]]) - log_total + route[x - 1][0], x) for x in DAG[i]])
        return route
    
    def _get_segs(self, sequence, route):
        segs = []
        r = len(sequence) - 1
        while r >= 0:
            segs.append(sequence[route[r][1]:r + 1])
            r = route[r][1] - 1
        return segs[::-1]

if __name__ == '__main__':
    # dict = Unigram(DATA1_CONTENT, DICT_UNIGRAM)
    # dict.Unigram()
    print(str(Evaluation(DATA1_SEG_POS, UNI_SEG)))
