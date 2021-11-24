from utils.self_balanced_tree import *

class MyDict:
    def __init__(self):
        self.tree = AVLTree()
    
    def insert(self, key, value):
        self.tree.insert(key, value)
    
    def get(self, key):
        return self.tree.get_extra_data(key)

class MySet:
    def __init__(self):
        self.tree = AVLTree()
    
    def add(self, key):
        self.tree.insert(key, key)
    
    def toList(self):
        return self.tree.toList()