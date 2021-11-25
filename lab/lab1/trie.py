# -*- coding: utf-8 -*-
from utils import *

END_OF_WORD = 1
END_OF_SEQUENCE = 2

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
            node_next = node_now.children.get(item)
            if node_next == None:
                node_now.children.insert(item, Node())
            node_now = node_now.children.get(item)
        node_now.value = True

    def search(self, sequence):
        node_now, result = self.root, None
        for i in range(len(sequence)):
            node_next = node_now.children.get(sequence[i])
            if node_next == None:
                return result
            else:
                node_now = node_next
            if node_now.value:
                result = sequence[:i + 1]
        return result

    def build(self, reverse=False, fast=False):
        with open(self.DICT_path, 'r', encoding='utf8') as f:
            for token in f.readlines():
                if reverse: token = token.strip()[::-1]
                else: token = token.strip()
                if fast:
                    token = fast_trick_2_byte(token)
                self.insert(token)
