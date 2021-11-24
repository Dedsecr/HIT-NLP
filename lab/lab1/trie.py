# -*- coding: utf-8 -*-
from utils import *

class Node:
    def __init__(self):
        self.value = False
        self.children = MyDict()

class Trie:
    def __init__(self, DICT_path):
        self.DICT_path = DICT_path
        self.root = Node()
        self.max_len = 0

    def insert(self, sequence):
        self.max_len = max(len(sequence), self.max_len)
        node_now = self.root
        for item in sequence:
            if item not in node_now.children:
                node_now.children[item] = Node()
            node_now = node_now.children[item]
        node_now.value = True

    def search(self, sequence):
        node_now, result = self.root, None
        for i in range(len(sequence)):
            if sequence[i] not in node_now.children:
                return result
            else:
                node_now = node_now.children[sequence[i]]
            if node_now.value:
                result = sequence[:i + 1]
        return result

    def build(self, reverse=False):
        with open(self.DICT_path, 'r', encoding='utf8') as f:
            for line in f.readlines():
                if reverse:
                    self.insert(line.strip()[::-1])
                else:
                    self.insert(line.strip())
