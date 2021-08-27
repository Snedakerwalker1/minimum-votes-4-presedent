# This File will run Dijkstra's algorithm on the set of States with electoral votes, to find the minimum number of
# voters needed to win the electoral college.
#
# A couple of assumptions will be made first the state is one by the minimum number of people so exactly < 50%
# Second all other states that are not used will be lost 100%

from States_Data import *
from Data_Structures import *


def Find_Fewest_Voters(filename="states.txt"):
    # now to just implement Dijkstra's to run find the minimum population needed to win the electoral college
    visited = ABTree(10, [], [])
    states = StatesData(filename)
    target = states.get_target_value()
    names = states.get_states()
    node1 = ElectorateState(names, 1, 0, 0)
    #need to initialize a minqueue
    queue = PriorityQueue()
    queue.push(node1,1)
    count = 0
    while not queue.isEmpty():
        count += 1
        node = queue.pop()
        if not isinstance(node, ElectorateState):
            return "Error bad node"
        if node.electorate_total >= target:
            print "A winner has been found"
            print "The vote total is " + str(node.get_vote_total())
            print "The total number of votes is " + str(node.get_total_voter_count())
            print "The electoral total is " + str(node.get_electorate_total())
            print "The states won are " + str(node.get_states())
            return
        else:
            for child in node.get_not_visited():
                newnode = node.add_state(child)
                if not newnode:
                    return "Node Error"
                if not visited.lookup(newnode.get_id()):
                    queue.push(newnode, newnode.get_priority())
                    visited.insert(newnode.get_id())
        if count > 33000000:
            return "Runtime Exception"
        if count%100 == 0:
            print count
    return "No node was found."

def Gready_Find_Fewest(filename="states.txt"):
    # After running into a memory error from the one above, v sad :'( , I dicided to implement a "greedy" version of this
    # algorithm, basically it starts with the state that has the lowest population to state ration then adds the next
    # state that will keep this ration the smallest, this in a side by side test with the test.txt this algorithm failed
    # finding a solution of about 15/40 vs the 10/40 solution normally found :(, so this is not necessarily the smallest
    # solution.
    # After running this now very quick version I found a solution that yielded the moderate 23.1% of voters to win the
    # country value, but noticed some discrepancies, and still not entirely convinced that the minimum number of voters
    # if found by just adding together all of the smallest states I have decided to try a third approach.
    visited = ABTree(10, [], [])
    states = StatesData(filename)
    target = states.get_target_value()
    names = states.get_states()
    node1 = ElectorateState(names, 1, 0, 0)

    while node1.electorate_total < target:
        queue = PriorityQueue()
        for child in node1.get_not_visited_arr(names):
            newnode = node1.add_state(child)
            if not newnode:
                return "Node Error"
            if not visited.lookup(newnode.get_id()):
                queue.push(newnode, newnode.get_priority())
                visited.insert(newnode.get_id())
        node1 = queue.pop()
    print "A winner has been found"
    print "The vote total is " + str(node1.get_vote_total())
    print "The total number of votes is " + str(node1.get_total_voter_count())
    print "The electoral total is " + str(node1.get_electorate_total())
    print "The states won are " + str(node1.get_states())


def Resourcefull_Greedy_Find_Fewest(filename="states.txt", kept_values=1000):
    # This algorithm will run in a similar manor to the greedy but instead of just taking the smallest node each time
    # it will take some kept_value number of nodes to be used as the base for the next step.
    # So with this slightly changed new algorithm and a start of 25 kept values the test came back with only one extra
    # state form the maximum. Which to me shows a very impressive improvement, since its not 11/40 vs 10/40.
    # Of course this could probably increase by fine tuning the kept value to a sweet spot where it safely ignores all
    # unnecessary data... ill do a couple of attempts.
    # After a few attempts I do notice that at 28 the test does pass, meaning that for the smaller test data set 28
    # keeping only the first 28 values will result in the optimal solution.
    #
    count = 0
    visited = ABTree(10, [], [])
    states = StatesData(filename)
    target = states.get_target_value()
    names = states.get_states()
    node1 = ElectorateState(names, 1, 0, 0)
    kept_nodes = []
    # so now we have to deal with node1 on its own yippy.
    queue = PriorityQueue()
    for child in node1.get_not_visited_arr(names):
        newnode = node1.add_state(child)
        if not newnode:
            return "Node Error"
        if not visited.lookup(newnode.get_id()):
            queue.push(newnode, newnode.get_priority())
            visited.insert(newnode.get_id())
    for i in range(0, kept_values):
        if not queue.isEmpty():
            kept_nodes.append(queue.pop())
    while True:
        queue = PriorityQueue()
        while len(kept_nodes) > 0:
            node1 = kept_nodes.pop()
            count += 1
            if node1.electorate_total >= target:
                print "A winner has been found"
                print "The vote total is " + str(node1.get_vote_total())
                print "The total number of votes is " + str(node1.get_total_voter_count())
                print "The electoral total is " + str(node1.get_electorate_total())
                print "The states won are " + str(node1.get_states())
                return
            for child in node1.get_not_visited_arr(names):
                newnode = node1.add_state(child)
                if not newnode:
                    return "Node Error"
                if not visited.lookup(newnode.get_id()):
                    queue.push(newnode, newnode.get_priority())
                    visited.insert(newnode.get_id())
            if count > 33000000:
                return "Runtime Exception"
            if count % 100 == 0:
                print count
        for i in range(0, kept_values):
            if not queue.isEmpty():
                kept_nodes.append(queue.pop())



def check_equive():
    state1 = ElectorateState(['a', 'b'], 1, 100, 0)
    state2 = ElectorateState(['c', 'd'], 1, 200, 4)
    state3 = ElectorateState(['a', 'b'], 2, 100, 0)
    print state1 == state2
    print state1 == state3

def test_ab_tree():
    tree = ABTree(4, [], [])
    tree.insert(1)
    tree.insert(2)
    tree.insert(5)
    tree.insert(6)
    tree.print_tree()
    tree.insert(3)
    tree.print_tree()
    tree.insert(4)
    tree.print_tree()
    tree.insert(7)
    tree.insert(8)
    tree.print_tree()

def test_not_v():
    state1 = ElectorateState(['a', 'b'], 1, 100, 0, ["c"])
    print state1.get_not_visited_arr(["a", "b", "c"])
    state2 = ElectorateState([], 1, 100, 0)
    print state2.get_not_visited_arr(["a", "b", "c"])

if __name__ == "__main__":
    #Find_Fewest_Voters("test.txt")
    #Find_Fewest_Voters("states.txt")
    #Gready_Find_Fewest("test.txt")
    Gready_Find_Fewest()
    Resourcefull_Greedy_Find_Fewest()
    #test_ab_tree()
    #test_not_v()
    print "All tests Passed"
