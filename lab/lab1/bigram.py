# -*- coding: utf-8 -*-
'''
二元语法模型
词典存储结构
w 表示当前词、wi表示该词前面的词及次数
{
    w:{
        w1: c1
        w2: c2
        w3: c3
    }
}
'''
import re
import math
import json
import codecs
from utils import *


# coding=utf-8
class Trie:
    root = {}
    # 终结点
    END = '/'

    # 将词加入字典树
    def add(self, word):
        # 从根节点遍历单词,char by char,如果不存在则新增,最后加上一个单词结束标志
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node[self.END] = None

    # 一个词是否在字典树中
    def contain(self, word):
        node = self.root
        for c in word:
            if c not in node:
                return False
            node = node[c]
        # 　判断是否为终结点
        return self.END in node

    # 扫描一个句子中, 所有以该字开始的单词
    def scan(self, sentence, index):
        cnt = index - 1
        result = [index]
        node = self.root
        for i, c in enumerate(sentence):
            if c not in node:
                return result
            node = node[c]
            cnt += 1
            if self.END in node and i:
                result.append(cnt)

        return result


class Bigram:

    def __init__(self):
        # TODO 测试集上检查平滑处理的抉择问题
        self.minfreq = -3.14e+100
        # 构建字典树、用于扫描全切分有向图
        self.trie = Trie()
        self.construct_trie()
        # 构建 二元词典
        self.construct_bigram_dic()
        # 读取二元词典
        # with open('files/bigram_dic.json', 'r') as f:
        #     self.bigram_dic = json.load(f)



    # 构建字典树
    def construct_trie(self, dic_file=DICT_UNIGRAM):
        with codecs.open(dic_file, 'r', encoding='utf8') as f:
            d = f.read()
            text = d.split('\r\n')
        # unigram
        # self.unigram = {}
        # unigram_time = 0
        self.words_num = len(text)
        for line in text:
            if (line != ""):
                words = line.split(" ")
                # self.unigram[words[0]] = int(words[1])
                # unigram_time += int(words[1])
                self.trie.add(words[0])
        # 词频词典
        # for key in self.unigram.keys():
        #    self.unigram[key] = math.log(self.unigram.get(key) / unigram_time)

    # 构建二元词典
    def construct_bigram_dic(self, seg_file=DATA_TRAIN_POS):
        with codecs.open(seg_file, 'r', 'gbk') as f:
            text = f.read()
        lines = text.split('\r\n')
        seg_lists = []
        # 按行提取分词结果
        for line in lines:
            # 遇到空白行直接进行下一行
            pattern = re.compile(r'^199801')
            # 未匹配下一行
            if not re.match(pattern, line):
                continue
            # 将每行正则匹配  Word/sign 包括 [Word/sign
            regex = r'\s[^\s^/]+/\w+'
            segs = re.findall(regex, line)
            # 处理匹配得到的字符
            seg_list = []
            for seg in segs:
                # 去除可能的[、同时去除匹配首位的空格
                s = seg.replace('[', '')[1:]
                word = s.split('/')[0]
                # 该行所有分词
                seg_list.append(word)
            # 首位插入BOS
            seg_list.insert(0, "^")
            # 尾部插入EOS
            seg_list.append("$")
            # 保存每行分词结果
            seg_lists.append(seg_list)
        # 构造bigram词典
        self.bigram_dic = {}
        # 遍历每行
        for seg_list in seg_lists:
            # 从第二个分词（第一个是BOS）遍历每行的分词语料
            for i in range(1, len(seg_list)):
                # 第一次遇到
                if seg_list[i] not in self.bigram_dic:
                    self.bigram_dic[seg_list[i]] = {}
                    # 保存该词前面的词
                    self.bigram_dic[seg_list[i]][seg_list[i - 1]] = 1
                else:
                    self.bigram_dic[seg_list[i]][seg_list[i - 1]] = self.bigram_dic[seg_list[i]].get(seg_list[i - 1], 0) + 1
        # 频数转换为概率, 取对数
        for key1 in self.bigram_dic.keys():
            sigma = 1e-7
            sum_freq = 0
            for key2 in self.bigram_dic.get(key1).keys():
                sum_freq += self.bigram_dic[key1].get(key2)
            # 求c(wi-1wi)/ c(wi)概率
            for key2 in self.bigram_dic.get(key1).keys():
                self.bigram_dic[key1][key2] = math.log(
                    (self.bigram_dic[key1].get(key2) + sigma) / (sum_freq + sigma * self.words_num))
                # add(sigma)
                temp = math.log(sigma / (sum_freq + self.words_num))
                if self.minfreq > temp:
                    self.minfreq = temp
        # with open('bigram_dic.json', 'w') as f:
        #     json.dump(self.bigram_dic, f)
        # print(self.minfreq)

    # 构建全切分有向图
    def construct_DAG(self, sentence):
        # {key:list}
        self.DAG = {}
        # ^ - $
        for i in range(1, len(sentence) - 1):
            # 保存以wi开始的词
            self.DAG[i] = self.trie.scan(sentence[i:-1], i)
        # 加EOS和BOS
        self.DAG[len(sentence) - 1] = [len(sentence) - 1]
        self.DAG[0] = [0]

    def dp_search(self, sentence):
        # prob max
        viterbi = {}
        for i in range(len(sentence)):
            viterbi[i] = {}
        # { i :{ end1: (prob, next), end2 : (prob, next) }}
        viterbi[len(sentence) - 1][len(sentence) - 1] = (0., len(sentence))
        # 反向DP
        for i in range(len(sentence) - 2, -1, -1):
            # 对每个wi起始的词求最大概率
            for x in self.DAG[i]:
                # P(wx+1...wy | wi..wx)*viterbi[x+1][index][0]
                prob_index = max(
                    (self.bigram_dic.get(sentence[x + 1:y + 1], {}).get(sentence[i:x + 1], self.minfreq) +
                     viterbi.get(x + 1)[y][0], y) for y in self.DAG[x + 1])
                viterbi[i][x] = prob_index

        # BOS
        end = max((self.bigram_dic.get(sentence[1:y + 1], {}).get(sentence[0], self.minfreq) +
                   viterbi.get(1)[y][0], y) for y in self.DAG[1])[1]
        # 回溯*
        start = 1
        segs = []
        while start < len(sentence) - 1:
            segs.append(sentence[start:end + 1])
            temp = start
            start = end + 1
            # print(viterbi[temp][end][0])
            end = viterbi[temp][end][1]
        return segs

    # 调用bigram分词并做后续处理
    def cut(self, sentence):
        sentence = '^' + sentence + '$'
        # 构建句子 全切分有向图
        self.construct_DAG(sentence)
        # 得到bigram分词结果
        bigram_segs = self.dp_search(sentence)
        return bigram_segs


