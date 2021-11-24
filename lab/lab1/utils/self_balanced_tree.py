class AVLNode:
    def __init__(self, data=None, extra_data=None):
        self.data = data
        self.extra_data = extra_data
        self.left = None
        self.right = None
        self.height = 0

class AVLTree:
    def __init__(self):
        self.root = None

    def __LL(self, node):
        temp = node.left
        node.left = temp.right
        temp.right = node
        node.height = max(self.__getHeight(node.right), self.__getHeight(node.left)) + 1
        temp.height = max(self.__getHeight(temp.right), self.__getHeight(temp.left)) + 1
        return temp

    def __RR(self, node):
        temp = node.right
        node.right = temp.left
        temp.left = node
        node.height = max(self.__getHeight(node.right), self.__getHeight(node.left)) + 1
        temp.height = max(self.__getHeight(temp.right), self.__getHeight(temp.left)) + 1
        return temp

    def __LR(self, node):
        node.left = self.__RR(node.left)
        return self.__LL(node)

    def __RL(self, node):
        node.right = self.__LL(node.right)
        return self.__RR(node)

    def __getHeight(self, node):
        if node == None:
            return -1
        return node.height

    def __insert(self, data, extra_data, node):
        if node == None:
            temp = AVLNode(data=data, extra_data=extra_data)
            return temp
        if data == node.data:
            return node
        if data < node.data:
            node.left = self.__insert(data, extra_data, node.left)
            if self.__getHeight(node.left) - self.__getHeight(node.right) >= 2:
                if data < node.left.data: node = self.__LL(node)
                else: node = self.__LR(node)
        else:
            node.right = self.__insert(data, extra_data, node.right)
            if self.__getHeight(node.right) - self.__getHeight(node.left) >= 2:
                if data > node.right.data: node = self.__RR(node)
                else: node = self.__RL(node)

        node.height = max(self.__getHeight(node.left), self.__getHeight(node.right)) + 1
        return node

    def insert(self, data, extra_data):
        self.root = self.__insert(data, extra_data, self.root)
        return self.root

    def __get_extra_data(self, data, node):
        if node == None:
            return None
        if data == node.data:
            return node.extra_data
        if data < node.data:
            return self.__get_extra_data(data, node.left)
        else:
            return self.__get_extra_data(data, node.right)

    def get_extra_data(self, data):
        return self.__get_extra_data(data, self.root)
    
    def __toList(self, node):
        result = []
        if node != None:
            result.append(node.extra_data)
            result += self.__toList(node.left)
            result += self.__toList(node.right)
        return result
    
    def toList(self):
        return self.__toList(self.root)