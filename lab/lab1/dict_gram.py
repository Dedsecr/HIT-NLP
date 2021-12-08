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
            if ('/m' in seg and seg.isascii()) or len(seg) == 0: continue
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


class Dict_bigram:
    def __init__(self, SEG_POS_path, DICT_path):
        self.SEG_POS_path = SEG_POS_path
        self.DICT_path = DICT_path
        self.words = {}
        self.max_len = 0
    
    def preprocess(self):
        with open(self.SEG_POS_path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
        dst_lines = []
        for l in lines:
            if not l: continue
            dst_line = []
            for word in l.split():
                if '/m' in word and word.isascii(): continue
                dst_line.append(word[1 if word[0] == '[' else 0:word.index('/')])
            dst_lines.append(dst_line)
        return dst_lines

    def get_dict(self):
        two_gram_dic = {}
        data_lines = self.preprocess()
        for line in data_lines:
            line.insert(0, 'BOS')
            line.append('EOS')
            for i in range(len(line) - 1):
                cur_word = line[i]
                post_word = line[i + 1]
                if cur_word not in two_gram_dic.keys():
                    two_gram_dic[cur_word] = {}
                if post_word not in two_gram_dic[cur_word]:
                    two_gram_dic[cur_word][post_word] = 1
                else:
                    two_gram_dic[cur_word][post_word] += 1

        two_gram_dic = {i: two_gram_dic[i] for i in sorted(two_gram_dic)}
        for word in two_gram_dic:
            two_gram_dic[word] = {i: two_gram_dic[word][i] for i in sorted(two_gram_dic[word])}
        dic_file = open(self.DICT_path, 'w')
        for word in two_gram_dic:
            write_line = word + ' '
            for p_word in two_gram_dic[word]:
                write_line += p_word + ' ' + str(two_gram_dic[word][p_word]) + ' '
            dic_file.write(write_line + '\n')


if __name__ == '__main__':
    # dict = Dict_unigram(DATA_TRAIN_POS, DICT_UNIGRAM)
    # dict.get_dict()
    dict = Dict_bigram(DATA_TRAIN_POS, DICT_BIGRAM)
    dict.get_dict()