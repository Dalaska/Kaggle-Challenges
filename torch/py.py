# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:28:30 2019

@author: dalaska
"""
import matplotlib as plt
import numpy as np

#fig = plt.figure(figsize = (10,5))
#plt.plot()
#plt.show()
#plt.xlabel
data = np.linspace(0,1,10)
class Node:
    def __init__(self,value):
        self.value = value

    def addLeft(self,LeftNode):
        self.left = LeftNode

    def addRight(self,RightNode):
        self.right = RightNode

class Tree:
    def __init__(self,root):
        self.root = root
    
    def addNode(self,node):
        self.node = node

class Graph:
    def __init__(self,node):
        self.node = node
        
   
# dict
# hash 
# tuple
# sack
d = {'Woodman': 95, 'Alan': 85, 'Bobo': 59}  
if 'woodman' in d:  # d字典中有woodman
    print(d['woodman'])
print(d.keys())  # 获取字典所有的键的可迭代对象
print(d.values()) 
l = ['知乎', 'woodman', 1987, 2017]
t1 = ('知乎', 'woodman', 1987, 2017, 'woodman')
t2 = (1, 2, 3, 4)

# object heading


if __name__ == '__main__':  
    dir(n1)
    type(n1)
    n1 = Node(3)
    n2 = Node(1)
    n3 = Node(2)
    n1.addLeft(n2)
    n1.addRight(n3)
    n1.left.value