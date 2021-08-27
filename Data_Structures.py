# Will need a priority que which allows for a push and pop function
# I think

import heapq
import math


class PriorityQueue:

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


class PriorityQueueFunction(PriorityQueue):

    def __init__(self, function):
        self.function = function
        PriorityQueue.__init__(self)

    def push(self, item):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.function(item))


class ABTree:

    def __init__(self, max_size, array, child):
        self.array = array
        self.child = child
        self.max_size = max_size
        self.isleaf = True
        self.hasParent = False

    def set_is_leaf(self):
        self.isleaf = False

    def set_has_parent(self):
        self.hasParent = True

    def check_is_leaf(self):
        return self.isleaf

    def lookup(self, item):
        if len(self.array) == 0:
            return False
        if self.array.__contains__(item):
            return True
        else:
            if self.check_is_leaf():
                return False
            i = 0
            while i < len(self.array):
                if item < self.array[i]:
                    return self.child[i].lookup(item)
                i += 1
            return self.child[-1].lookup(item)

    def insert(self, item):
        added = False
        if len(self.array) == 0:
            self.array.append(item)
        if self.array.__contains__(item):
            return False
        elif self.isleaf:
            if len(self.array) < self.max_size:
                #the item is inserted at this level of the array.
                i = 0
                array = []
                while i < len(self.array):
                    if item < self.array[i] and not added:
                        array.append(item)
                        added = True
                    array.append(self.array[i])
                    i += 1
                if not added:
                    array.append(item)
                self.array = array
                return False
            elif len(self.array) == self.max_size:
                #Then we must split the node and push the center item up
                left_side = []
                right_side = []
                i = 0
                middle = math.floor((self.max_size+ 1)/2)
                middlest = None
                while i < len(self.array):
                    if i < middle:
                        if item < self.array[i] and not added:
                            added = True
                            left_side.append(item)
                        left_side.append(self.array[i])
                    elif i == middle:
                        if item < self.array[i] and not added:
                            added = True
                            middlest = item
                            right_side.append(self.array[i])
                        else:
                            middlest = self.array[i]
                    else:
                        if item < self.array[i] and not added:
                            added = True
                            right_side.append(item)
                        right_side.append(self.array[i])
                    i += 1
                if not added:
                    right_side.append(item)
                newchild = ABTree(self.max_size, right_side, [])
                newchild.set_has_parent()
                if not self.hasParent:
                    #Then the tree has no parent and must deal
                    newleftchild = ABTree(self.max_size, left_side, [])
                    newleftchild.set_has_parent()
                    self.array = [middlest]
                    self.child = [newleftchild, newchild]
                    self.set_is_leaf()
                    return False
                else:
                    self.set_has_parent()
                    self.array = left_side
                    return [middlest, newchild]
        else:
            i = 0
            while i < len(self.array):
                if item < self.array[i] and not added:
                    retval = self.child[i].insert(item)
                    added = True
                i += 1
            if not added:
                retval = self.child[i].insert(item)
            add2 = False
            if retval and len(self.array) < self.max_size:
                #So we have a new part and open spaces so
                newchild = []
                array = []
                i = 0
                while i < len(self.array):
                    newchild.append(self.child[i])
                    if retval[0] < self.array[i] and not add2:
                        add2 = True
                        array.append(retval[0])
                        newchild.append(retval[1])
                    array.append(self.array[i])
                    i += 1
                newchild.append(self.child[i])
                if not add2:
                    array.append(retval[0])
                    newchild.append(retval[1])
                self.array = array
                self.child = newchild
            elif retval and len(self.array) == self.max_size:
                #This means that on inserting into the child we split the child node and returned the midleest
                #Value of the child node, so we would need to insert that into this node, but since this node is already
                #Full, we must split this array and do stuff
                left_side = []
                left_child = []
                right_side = []
                right_child = []
                i = 0
                middle = math.floor((self.max_size + 1) / 2)
                middlest = None
                while i < len(self.array):
                    if i < middle:
                        left_child.append(self.child[i])
                        if retval[0] < self.array[i] and not add2:
                            left_side.append(retval[0])
                            left_child.append(retval[1])
                            add2 = True
                        left_side.append(self.array[i])
                    elif i == middle:
                        left_child.append(self.child[i])
                        if retval[0] < self.array[i] and not add2:
                            add2 = True
                            middlest = retval[0]
                            right_child.append(retval[1])
                            right_side.append(self.array[i])
                        else:
                            middlest = self.array[i]
                    else:
                        right_child.append(self.child[i])
                        if retval[0] < self.array[i] and not add2:
                            add2 = True
                            right_side.append(retval[0])
                            right_child.append(retval[1])
                        right_side.append(self.array[i])
                    i += 1
                right_child.append(self.child[i])
                if not add2:
                    right_side.append(retval[0])
                    right_child.append(retval[1])
                newchild = ABTree(self.max_size, right_side, right_child)
                newchild.set_is_leaf()
                newchild.set_has_parent()
                if not self.hasParent:
                    # We must make a parent
                    newleftchild = ABTree(self.max_size, left_side, left_child)
                    newleftchild.set_is_leaf()
                    newleftchild.set_has_parent()
                    self.array = [middlest]
                    self.child = [newleftchild, newchild]
                    return False
                else:
                    self.array = left_side
                    self.child = left_child
                    return [middlest, newchild]

    def print_tree(self):
        #This will print the tree lol
        if self.isleaf:
            print "This is a leaf"
            for i in self.array:
                print i
        else:
            print "This node contains the following"
            for i in self.array:
                print i
            print "And it has " + str(len(self.child)) + " children"
            for i in self.child:
                i.print_tree()
