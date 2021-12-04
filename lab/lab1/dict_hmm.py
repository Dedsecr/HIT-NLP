#-*- coding:utf-8 -*-
import sys
import pickle
import math

from utils import *

B_TOKEN = 'B'
M_TOKEN = 'M'
E_TOKEN = 'E'
S_TOKEN = 'S'

class Dict_hmm:
    def __init__(self, SEG_POS_path, DICT_path, WORDDICT_path, epsilon=sys.float_info.epsilon):
        self.SEG_POS_path = SEG_POS_path
        self.DICT_path = DICT_path
        self.WORDDICT_path = WORDDICT_path
        self.epsilon = epsilon
        self.state_lst = [B_TOKEN, M_TOKEN, E_TOKEN, S_TOKEN]
        self.start_p = {}
        self.trans_p = {}
        self.emit_p = {}
        self.state_dict = {}
        self.words = set()
        for state in self.state_lst:
            self.start_p[state] = 1 / len(self.state_lst)
            self.trans_p[state] = {s:1 / len(self.state_lst) for s in self.state_lst}
            self.emit_p[state] = {}
            self.state_dict[state] = 0

    def _label(self, word):
        out = []
        if len(word) == 1:
            out = [S_TOKEN]
        else:
            out += [B_TOKEN] + [M_TOKEN] * (len(word) - 2) + [E_TOKEN]
        return out

    def get_dict(self):
        with open(self.SEG_POS_path, 'r') as f:
            lines = [l.strip().split() for l in f.readlines()]
        
        line_nb = 0
        for line in lines:
            if not line: continue
            char_lst, state_lst = [], []
            line_nb += 1
            for word in line:
                if ('/m' in word and word.isascii()) or len(word) == 0: continue
                true_word = word[1 if word[0] == '[' else 0 : word.index('/')]
                self.words.add(true_word)
                state_lst.extend(self._label(true_word))
                char_lst.extend(true_word)
            
            assert len(state_lst) == len(char_lst)
            for index, state in enumerate(state_lst):
                self.state_dict[state] += 1
                if index == 0:
                    self.start_p[state] += 1
                else:
                    self.trans_p[state_lst[index-1]][state] += 1
                self.emit_p[state][char_lst[index]] = self.emit_p[state].get(char_lst[index], 0) + 1

        for state, num in self.start_p.items():
            self.start_p[state] = math.log((num + self.epsilon) / line_nb)

        for pre_state, value in self.trans_p.items():
            for cur_state, cur_num in value.items():
                self.trans_p[pre_state][cur_state] = math.log((cur_num + self.epsilon) / self.state_dict[pre_state])
        
        for state, value in self.emit_p.items():
            for char, char_num in value.items():
                self.emit_p[state][char] = math.log((char_num + self.epsilon) / self.state_dict[state])
        
        self._save_dict()
    
    def _save_dict(self):
        with open(self.DICT_path, 'wb') as f:
            pickle.dump(self.start_p, f)
            pickle.dump(self.trans_p, f)
            pickle.dump(self.emit_p, f)
            for state in self.state_lst:
                pickle.dump(math.log(self.epsilon / self.state_dict[state]), f)
        with open(self.WORDDICT_path, 'w', encoding='utf-8') as f:
            for word in self.words:
                f.write(word + '\n')
        
if __name__ == '__main__':
    dict = Dict_hmm(DATA_TRAIN_POS, DICT_HMM, WORDDICT_HMM)
    dict.get_dict()
    