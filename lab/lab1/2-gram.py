import numpy as np
import re
from oov import *
from utils import *
from evaluation import *


class Bigram:
    def __init__(self, src_path, freq_path, dst_path, dic_path, punct='[。；！？]'):
        self.src_path = src_path
        self.freq_path = freq_path
        self.dic_path = dic_path
        self.word_cnt = 0
        self.punct = punct
        self.dst_file = open(dst_path, 'w', encoding='utf-8')

        self.two_gram_dic = self._load_dic()
        self.freq_dic = self._load_freq()

    def _load_dic(self):
        dic_file = open(self.dic_path, 'r')
        dic_lines = dic_file.readlines()
        two_gram_dic = {}
        for line in dic_lines:
            temp = line.strip().split()
            two_gram_dic[temp[0]] = {}
            for i in range(int((len(temp) - 1) / 2)):
                two_gram_dic[temp[0]][temp[i * 2 + 1]] = int(temp[i * 2 + 2])

        return two_gram_dic

    def _load_freq(self):
        self.word_cnt = 0
        freq_file = open(self.freq_path, 'r', encoding='utf-8')
        freq_lines = freq_file.readlines()
        freq_dic = {}
        for line in freq_lines:
            if line == '\n':
                continue
            freq_dic[line.split()[0]] = int(line.split()[1])
            self.word_cnt += int(line.split()[1])

        return freq_dic

    def get_dag(self, sentence):
        dag = {}
        for k in range(len(sentence)):
            cur_list = []
            i = k
            frag = sentence[k]
            while i < len(sentence) and frag in self.freq_dic:
                if self.freq_dic[frag] > 0:
                    cur_list.append(i)
                i += 1
                frag = sentence[k:i + 1]
            if len(cur_list) == 0:
                cur_list.append(k)
            dag[k] = cur_list
        return dag

    # def calc_log_pos(self, pre_word, post_word, pre_post_dic, freq_dic):
    #     pre_freq = freq_dic.get(pre_word, 0)
    #     combine_freq = pre_post_dic.get(pre_word, {}).get(post_word, 0)
    #     return np.log(combine_freq + 1) - np.log(pre_freq + len(freq_dic))

    def calc_log_pos(self, pre_word, post_word):
        # print(self.word_cnt)
        sigma = 1e-7
        pre_freq = self.freq_dic.get(pre_word, 0)
        combine_freq = self.two_gram_dic.get(pre_word, {}).get(post_word, 0)
        return np.log(combine_freq + sigma) - np.log(pre_freq + sigma * self.word_cnt)

    def dp_on_dag(self, sentence, dag):
        pos_p_by_pre = {}
        pos_p_by_pre['BOS'] = {}
        for i in dag[3]:
            pos_p_by_pre['BOS'][(3, i + 1)] = self.calc_log_pos('BOS', sentence[3:i + 1])
        cur_start = 3
        while cur_start < len(sentence) - 3:
            for pre_end in dag[cur_start]:
                pre_word = sentence[cur_start:pre_end + 1]
                all_post_p = {}
                if sentence[pre_end + 1: pre_end + 4] == 'EOS':
                    all_post_p['EOS'] = self.calc_log_pos(pre_word, 'EOS')
                else:
                    for post_end in dag[pre_end + 1]:
                        post_word = sentence[pre_end + 1:post_end + 1]
                        all_post_p[(pre_end + 1, post_end + 1)] = self.calc_log_pos(pre_word, post_word)
                pos_p_by_pre[(cur_start, pre_end + 1)] = all_post_p
            cur_start += 1

        pre_by_post = {}  # 某个词的所有前词
        # print(pos_p_by_pre)
        for pre_word in pos_p_by_pre:
            for post_word in pos_p_by_pre[pre_word]:
                if post_word not in pre_by_post.keys():
                    pre_by_post[post_word] = []
                pre_by_post[post_word].append(pre_word)

        all_words = list(pos_p_by_pre.keys())
        all_words.append('EOS')
        route = {}
        for word in all_words:  # 遍历全切分词中的所有词
            if word == 'BOS':
                route[word] = (0.0, 'BOS')
                continue
            pre_words = pre_by_post[word]
            route[word] = max((pos_p_by_pre[pre][word] + route[pre][0], pre) for pre in pre_words)
        return route

    def frag(self, sentence):
        sentence = 'BOS' + sentence + 'EOS'
        fully_dag = self.get_dag(sentence)
        route = self.dp_on_dag(sentence, fully_dag)
        cur_word = 'EOS'
        frag_list = []
        while cur_word != 'BOS':
            word = route[cur_word][1]
            if word != 'BOS':
                frag_list.insert(0, sentence[word[0]:word[1]])
            cur_word = word
        return frag_list

    def bigram(self):
        with open(self.src_path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]

        # line_cnt = 0
        for line in lines:
            # print(line_cnt)
            # line_cnt += 1
            if not line:
                self.dst_file.write('\n')
                continue
            
            seg_line, last_pos = line[:19] + '/ ', 0
            line = line[19:]
            for i in re.finditer(self.punct, line):
                sentence = line[last_pos:i.start()]
                if sentence == '':
                    continue
                seg_list = self.frag(sentence)

                # 数字、英文字母处理
                seg_list = post_process(seg_list)

                # 未登录词处理
                oov = OOV()
                seg_list = oov.oov(seg_list)

                frag_sentence = ''
                for s in seg_list:
                    frag_sentence += s + '/ '

                seg_line += frag_sentence + i.group() + '/ '
                last_pos = i.end()

            if line[last_pos:] != '':
                # frag_line += frag(line[last_pos:], freq_dic, two_gram_dic)
                seg_list = self.frag(line[last_pos:])

                # 数字、英文字母处理
                seg_list = post_process(seg_list)

                # 未登录词处理
                oov = OOV()
                seg_list = oov.oov(seg_list)

                for s in seg_list:
                    seg_line += s + '/ '

            self.dst_file.write(seg_line + '\n')
        self.dst_file.close()


if __name__ == '__main__':
    b = Bigram(DATA_TEST_CONTENT, DICT_UNIGRAM, BI_SEG, DICT_BIGRAM)
    b.bigram()
    print(str(Evaluation(DATA_TEST_POS, BI_SEG)))