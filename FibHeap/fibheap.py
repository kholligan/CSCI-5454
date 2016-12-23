#Fibonacci Heap implementation
#Author: Kevin Holligan
#Based on the pseudocode from the CLRS text, ch 20.

class FibHeap:
    
    # internal node class 
    class node:
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.child = None
            self.left = None
            self.right = None
            self.degree = 0
            self.mark = False

    # Global access point to start of list and mininum node
    rootList, minNode = None, None
    totalNodes = 0
    
    def returnMin(self):
        return self.min_node

    def insert(self, key):
        node = self.node(key)
        node.left = node
        node.right = node
        #If rootList is empty, set it to the node
        if self.rootList is None:
                self.rootList = node
        #Otherwise, insert the node on to left of the root of rootList
        else:
            #Node points to root list and rootList's left
            node.left = self.rootList.left
            node.right = self.rootList
            #Old left node points to new node on its right
            self.rootList.left.right = node
            #RootList left points to node
            self.rootList.left = node
        #Update minNode pointer if necessary
        if self.minNode is None or node.key < self.minNode.key:
            self.minNode = node
        self.totalNodes += 1

    def merge(self, H2):
        H = FibHeap()
        H.minNode = self.minNode
        H.rootList = self.rootList

        #rootList points to tail of H2. tail of rootList points to head of H2
        h2tail = H2.rootList.right
        h1tail = self.rootList.right
        self.rootList.right = h2tail
        h2tail.left = self.rootList
        h1tail.left = H2.rootList
        H2.rootList.right = h1Tail

        #update minNode if necessary
        if H.minNode is None or (H2.minNode is not None and H2.minNode.key < H.minNode.key):
            H.minNode = H2.minNode
        H.totalNodes = self.totalNodes + H2.totalNodes
        del self
        del H2
        return H

    def deleteMin(self):
        z = self.minNode
        if z is not None:
            if z.child is not None:
                childNodes = [x for x in self.iterate(z.child)]
                for i in range(len(childNodes)):
                    #If rootList is empty, set it to the node
                    if self.rootList is None:
                            self.rootList = childNodes[i]
                    #Otherwise, insert the node on to left of the root of rootList
                    else:
                        #Node points to root list and rootList's left
                        childNodes[i].left = self.rootList.left
                        childNodes[i].right = self.rootList
                        #Old left node points to new node on its right
                        self.rootList.left.right = childNodes[i]
                        #RootList left points to node
                        self.rootList.left = childNodes[i]
                    childNodes[i].parent = None
            #Remove z from the root list of the heap
            #If z is first item in rootList, update rootList to next item
            if z is self.rootList:
                self.rootList = z.right
            #Update z's neighbors to point to each other
            z.left.right = z.right
            z.right.left = z.left
            #Set new min node in heap
            if z is z.right:
                self.minNode = self.rootList = None
            else:
                self.minNode = z.right
                self.consolidate()
            self.totalNodes -= 1
        return z


    def consolidate(self):
        #Create empty array based on number of nodes
        A = [None] * self.totalNodes
        #For each node w in the root list of H
        nodes = [w for w in self.iterate(self.rootList)]
        for w in range(len(nodes)):
            x = nodes[w]
            d = x.degree
            while A[d] is not None:
                y = A[d]
                #Swap which node is going to be the new parent when linking 
                if x.key > y.key:
                    temp = x
                    x = y
                    y = temp
                #Link the nodes together
                self.heapLink(y, x)
                #Set array element to none and increase degree
                A[d] = None
                d += 1
            A[d] = x
        #Update the minNode if there is a lower key in A
        for i in range(len(A)):
            if A[i] is not None:
                if A[i].key < self.minNode.key:
                    self.minNode = A[i]

    def heapLink(self, y, x):
        #Remove y from the root list of the heap
        #If y is first item in rootList, update rootList to next item
        if y is self.rootList:
            self.rootList = y.right
        #Update y's neighbors to point to each other
        y.left.right = y.right
        y.right.left = y.left
        #Point y to itself (reset it in a sense)
        y.left = y
        y.right = y
        #Because y is new child of x, when need it include it on child linked list
        #If root has no children
        if x.child is None:
            x.child = y
        #Insert the node between two nodes and update pointers
        else:
            y.left = x.child.left
            y.right = x.child
            x.child.left.right = y
            x.child.left = y
        #Update node properties
        x.degree += 1
        y.parent = x
        y.mark = False

    def decreaseKey(self, x, k):
        if k > x.key:
            return None
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self.cut(x, y)
            self.recursiveCut(y)
        #update the new minimum
        if x.key < self.minNode.key:
            self.minNode = x

    #Remove a child node and put it on root list
    def cut(self, x, y):
        # self.remove_from_child_list(y, x)
        #Remove x from child list of y
        if y.child is y.child.left:
            y.child = None
        #Make new entry into child list
        elif y.child is x:
            y.child = x.right
            x.right.y = y
        #Update child list pointers
        x.left.right = x.right
        x.right.left = x.left

        y.degree -= 1
        #Put node x in the rootList
        if self.rootList is None:
                self.rootList = x
        #Insert the node on the left of the root of rootList
        else:
            #Node points to root list and rootList's left
            x.left = self.rootList.left
            x.right = self.rootList
            #Old left node points to new node on its right
            self.rootList.left.right = x
            #RootList left points to node
            self.rootList.left = x
        #Update properties
        x.parent = None
        x.mark = False
    
    #Cut parents if two child nodes have been cut
    def recursiveCut(self, y):
        z = y.parent
        if z is not None:
            if y.mark is False:
                y.mark = True
            else:
                self.cut(y, z)
                self.recursiveCut(z)

    #Helper function to iterate over list
    def iterate(self, head):
        node = end = head
        while True:
            #only child
            if node.right is None and node.left is None:
                yield node
                break
            #If we've looped back to the beginning
            elif node.right is end:
                yield node
                break
            else:
                node = node.right