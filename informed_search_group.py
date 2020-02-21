import queue

class Node:
    def __init__(self, value, parent, g, h, t):
        self.parent = parent
        self.value = value
        self.f = g + h  # combo (f = g + h)
        self.g = g  # path
        self.h = h  # heuristic
        self.t = t  # type of search (G or A)

        # Less than function to compare nodes.
        # A Star compare using f(n), Greedy compare using h(n)
    def __lt__(self, other):
        # A Star comparison
        if self.t == "A":
            # was <
            if self.f < other.f:
                return True
            else:
                return False
        # If Greedy search comparison
        else:
            # was <
            if self.h < other.h:
                return True
            else:
                return False


# For the Manhattan distance. You are going to be comparing the start grid to the goal grid and return the absolute value to get the position.
# Manhattan distance is a ideal world where you could move freely. This is counting steps dispite if you can move there or not.

# Heuristic Function:Create a heuristic function to be use for h(n). (Manhattan distance can be used here).
# The brackets are the coordinates. X = 0 y = 1.
# "current" = Node Object, "goal" = coordinate
def heuristic(current, goal):
    h = abs(current.value[0] - goal[0]) + abs(current.value[1] - goal[1])
    return h

testlist = [[1, 2], [3, 4]]
# test = queue.PriorityQueue()
# OG_Node = Node([1, 1], None, 6, 2, "A")
# test.put(OG_Node)
# NEW_Node = Node([1, 1], None, 5, 1, "A")
# test.put(NEW_Node)
# print(test.get().value)
# print(OG_Node.value)
print(testlist[0])
# print(OG_Node.g)
# print("Break")
# print(OG_Node < NEW_Node)