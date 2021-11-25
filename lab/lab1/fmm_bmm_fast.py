# -*- coding: utf-8 -*-

import os

from utils import *
from trie import *

class MM:
    def __init__(self, DICT_path, CONTENT_path):
        if os.path.exists(DATA1_FMM):
            os.remove(DATA1_FMM)
        if os.path.exists(DATA1_BMM):
            os.remove(DATA1_BMM)

        self.CONTENT_path = CONTENT_path
        self.DICT_path = DICT_path
        
    def MM(self, MM_type='F'):
        self.trie = Trie(self.DICT_path)
        self.trie.build(reverse=True if MM_type != 'F' else False, fast=True)
        f_mm = open(DATA1_FMM if MM_type == 'F' else DATA1_BMM, 'a', encoding='utf8')

        with open(self.CONTENT_path, 'r', encoding='utf8') as f:
            lines = [l.strip() for l in f.readlines()]
        for line in lines:
            now_line, segs = line if MM_type == 'F' else line[::-1], []
            while len(now_line) > 0:
                result = self.trie.search(fast_trick_2_byte(now_line[:self.trie.max_len]))
                if result is not None:
                    result = fast_trick_2_str(result)
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
    mm = MM(DATA1_DICT, DATA1_TEST_CONTENT)
    mm.MM(MM_type='F')
    mm.MM(MM_type='B')