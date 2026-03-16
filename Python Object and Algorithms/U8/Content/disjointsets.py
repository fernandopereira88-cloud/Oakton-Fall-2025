'''
Created on Sep 22, 2024

@author: Ivan Temesvari
'''
class DisjointSet:
    def __init__(self, n):
        self.parent = [-1]*n #all cells are roots/no parent
        self.rank = [0] * n #the rank/height of each cell is initially 0
        
    def find(self, u):    
        if(self.parent[u] < 0):  #no parent
            return u
        else:
            #recurse to find root parent; path compression
            self.parent[u] = self.find(self.parent[u]) 
            return self.parent[u]
        
    def union(self, u, v): #union by height
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            elif self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1  #one level higher               
                
    def print_disjoint_set_tree(self):
        print("Disjoint Set Tree:")
        for i in range(len(self.parent)):
            print(f"Node {i}: Parent -> {self.parent[i]}")
