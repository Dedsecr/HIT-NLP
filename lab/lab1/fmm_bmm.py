# -*- coding: utf-8 -*-

import time

from utils import *
from trie import *
from evaluation import *

class MM:
    def __init__(self, DICT_path, CONTENT_path):
        del_old_file(DATA1_FMM)
        del_old_file(DATA1_BMM)

        self.CONTENT_path = CONTENT_path
        self.DICT_path = DICT_path
        
    def MM(self, MM_type='F', dict_type='AVL', timer=False):
        self.trie = Trie(self.DICT_path, type=dict_type)
        self.trie.build(reverse=True if MM_type != 'F' else False)
        f_mm = open(DATA1_FMM if MM_type == 'F' else DATA1_BMM, 'a', encoding='utf8')

        if timer:
            time_start = time.time()
        with open(self.CONTENT_path, 'r', encoding='utf8') as f:
            lines = [l.strip() for l in f.readlines()]
        for line in lines:
            now_line, segs = line if MM_type == 'F' else line[::-1], []
            while len(now_line) > 0:
                result = self.trie.search(now_line[:self.trie.max_len])
                if result is not None:
                    segs.append(result)
                    now_line = now_line[len(result):]
                else:
                    segs.append(now_line[0])
                    now_line = now_line[1:]
            if MM_type != 'F':
                for i in range(len(segs)):
                    segs[i] = segs[i][::-1]
                segs = segs[::-1]
            segs = post_process(segs)
            for seg in segs:
                f_mm.write(seg + '/ ')
            f_mm.write('\n')
        f_mm.close()
        if timer:
            time_end = time.time()
            return time_end - time_start

def post_process(segs):
    now, result_segs = '', []
    for i in range(len(segs)):
        if segs[i].isascii():
            now += segs[i]
        elif len(now) > 0:
            result_segs.append(now)
            now = segs[i]
        else:
            result_segs.append(segs[i])
    if len(now) > 0:
        result_segs.append(now)
    return result_segs

if __name__ == '__main__':    
    '''
    type: 'AVL', 'HASH' or 'HASH1'
    '''
    mm = MM(DATA1_DICT, DATA1_TEST_CONTENT)
    time_FMM = mm.MM(MM_type='F', dict_type='AVL', timer=True)
    time_BMM = mm.MM(MM_type='B', dict_type='AVL', timer=True)
    with open(DATA1_TIMECOST, 'w', encoding='utf8') as f:
        f.write('Before Optimization:\n')
        f.write('\tFMM: time: {:.2f}, Acc: {}\n'.format(time_FMM, Evaluation(DATA1_TEST_POS, DATA1_FMM).get_accuracy()))
        f.write('\tBMM: time: {:.2f}, Acc: {}\n'.format(time_BMM, Evaluation(DATA1_TEST_POS, DATA1_BMM).get_accuracy()))
    
    mm = MM(DATA1_DICT, DATA1_TEST_CONTENT)
    time_FMM = mm.MM(MM_type='F', dict_type='HASH1', timer=True)
    time_FMM = mm.MM(MM_type='B', dict_type='HASH1', timer=True)
    with open(DATA1_TIMECOST, 'a', encoding='utf8') as f:
        f.write('After Optimization:\n')
        f.write('\tFMM: time: {:.2f}, Acc: {}\n'.format(time_FMM, Evaluation(DATA1_TEST_POS, DATA1_FMM).get_accuracy()))
        f.write('\tBMM: time: {:.2f}, Acc: {}\n'.format(time_BMM, Evaluation(DATA1_TEST_POS, DATA1_BMM).get_accuracy()))

    