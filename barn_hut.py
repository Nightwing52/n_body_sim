import numpy as np
import math

class Tree:
    def __init__(self, COM_x, COM_y, m, empty): #set empty to True if initializing an empty node
        if not empty:
            self.x, self.y, self.s=0.0, 0.0, 0.0
            self.m, self.COM_x, self.COM_y=m, COM_x, COM_y
        else:
            self.x, self.y, self.s, self.m=COM_x, COM_y, m, 0
            self.COM_x, self.COM_y=0.0, 0.0
        self.children=[None, None, None, None]
        
    def __get_square__(self): #returns location and size of square, not COM
        return (self.x, self.y, self.s)
    
    def __get_mass__(self):
        return self.m

    def __get_COM__(self):
        return (self.COM_x, self.COM_y)

    def __set_COM__(self, pos, m):
        self.COM_x, self.COM_y, self.m=pos[0], pos[1], m
        
    def __set_square__(self, x, y, s): #for empty nodes
        self.x, self.y, self.s=x, y, s
    
    def add(self, body):
        if self.__in_node__(body.__get_COM__()):
            if self.m == 0: #node empty; base case
                self.__set_COM__(body.__get_COM__(), body.__get_mass__())
                return True
            elif self.children[0] != None: #internal node
                self.__update_COM__(body.__get_COM__(), body.__get_mass__())
                return self.children[0].add(body) or self.children[1].add(body) or self.children[2].add(body) or self.children[3].add(body)
            else: #external node; have to divide
                old=Tree(self.COM_x, self.COM_y, self.m, False)
                loc=self.__get_square__()
                s=self.s
                ul, ur=Tree(loc[0], loc[1], s/2, True), Tree(loc[0]+s/2, loc[1], s/2, True)
                ll, lr=Tree(loc[0], loc[1]+s/2, s/2, True), Tree(loc[0]+s/2, loc[1]+s/2, s/2, True)
                self.__set_neighbors__(ul, ur, ll, lr)
                self.add(old) and self.add(body)
                self.__update_COM_in__()
                return True
        return False

    def __update_COM__(self, pos, m): #for empty nodes
        self.COM_x=(self.COM_x*self.m+pos[0]*m)/(self.m+m)
        self.COM_y=(self.COM_y*self.m+pos[1]*m)/(self.m+m)
        self.m+=m

    def __update_COM_in__(self): #for internal nodes
        M, x, y=0.0, 0.0, 0.0
        for child in self.children:
            if child != None:
                m=child.__get_mass__()
                COM=child.__get_COM__()
                x+=m*COM[0]
                y+=m*COM[1]
                M+=m
        self.COM_x, self.COM_y, self.m=x/M, y/M, M
        
    def __set_neighbors__(self, ul, ur, ll, lr):
        self.children=[ul, ur, ll, lr]
    
    def __in_node__(self, pos):
        return pos[0] > self.x and pos[0] < self.x+self.s and pos[1] > self.y and pos[1] < self.y+self.s

    #outputs a pre traversal or whatever it's called
    def print_tree(self):
        if self.m == 0: #none empty
            print("Empty node! Square information: "+str(self.x)+" "+str(self.y)+" "+str(self.s))
            return True
        elif self.children[0] != None: #internal node
            print("Internal node! Center of mass information: "+str(self.COM_x)+" "+str(self.COM_y)+" "+str(self.m))
            return self.children[0].print_tree() and self.children[1].print_tree() and self.children[2].print_tree() and self.children[3].print_tree()
        else: #external node
            print("External node! Particle information: "+str(self.COM_x)+" "+str(self.COM_y)+" "+str(self.m))
            return True

    #builds tree from positions
    def build_tree(n, x, y, m):
        head=Tree(0.0, 0.0, 1.0, True)
        for i in range(n):
            head.add(Tree(x[i], y[i], m[i], False))
        return head
    
    #recursively computes force on a single body
    def find_force(self, x, y, tol=0.5):
        delta_x, delta_y=x-self.COM_x, y-self.COM_y
        r=math.sqrt(delta_x**2+delta_y**2)
        if self.COM_x == x and self.COM_y == y: #force on itself
            return np.zeros(2)
        elif self.children[0] == None: #external node! have to compute force directly
            return np.array([-1*self.m*delta_x/r**3, -1*self.m*delta_y/r**3])
        elif self.s/r < tol: #internal node, but far enough to approximate by COM
            return np.array([-1*self.m*delta_x/r**3, -1*self.m*delta_y/r**3])
        else: #subdividing
            force=np.zeros(2)
            for i in range(4):
                if self.children[i] != None:
                    force+=self.children[i].find_force(x, y)
            return force
