# -*- coding: utf-8 -*-
from utils import *

class Evaluation:
    def __init__(self, DATA_path, PRED_path):
        self.DATA = []
        with open(DATA_path, 'r', encoding='utf8') as f:
            lines = [l.strip() for l in f.readlines()]
        for l in lines:
            segs, now_segs = l.split(), []
            for seg in segs:
                if len(seg) == 0: continue
                word = seg[1 if seg[0] == '[' else 0 : seg.index('/')]
                now_segs.append(word)
            self.DATA.append(now_segs)
        
        self.PRED = []
        with open(PRED_path, 'r', encoding='utf8') as f:
            lines = [l.strip() for l in f.readlines()]
        for l in lines:
            segs, now_segs = l.split(), []
            for seg in segs:
                if len(seg) == 0: continue
                word = seg[0 : seg.index('/')]
                now_segs.append(word)
            self.PRED.append(now_segs)
    
    def to_region(self, segs):
        region, start = [], 0
        for seg in segs:
            end = start + len(seg)
            region.append((start, end))
            start = end
        return region

    def get_accuracy(self):
        assert len(self.DATA) == len(self.PRED)
        A_size, B_size, A_cap_B_size = 0, 0, 0
        for i in range(len(self.DATA)):
            if len(self.DATA[i]) == 0: continue
            A, B = set(self.to_region(self.DATA[i])), set(self.to_region(self.PRED[i]))
            A_size += len(A)
            B_size += len(B)
            A_cap_B_size += len(A & B)
        p, r = A_cap_B_size / B_size * 100, A_cap_B_size / A_size * 100
        return p, r, 2 * p * r / (p + r)
        

if __name__ == '__main__':
    print(Evaluation(DATA1_TEST_POS, DATA1_FMM).get_accuracy())
    print(Evaluation(DATA1_TEST_POS, DATA1_BMM).get_accuracy())
