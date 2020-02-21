#!/usr/bin/env python3.7

import queue

# Node class to hold the location and parent node (needed for getting final path)
class Node:
    def __init__(self, value, parent, h, g, t):
        self.parent = parent
        self.value = value
        self.g = g  # path cost
        self.h = h  # heuristic cost
        self.f = g + h  # path and heuristic
        self.t = t  # type of search (G or A)

    # Less than function to compare nodes.
    # A Star compare using f(n), Greedy compare using h(n)
    def __lt__(self, other):
        # A Star comparison
        if self.t == "A":
            if self.f < other.f:
                return True
            else:
                return False
        if self.t == "G":
            if self.h < other.h:
                return True
            else:
                return False


def readGrid(filename):
    # print('In readGrid')
    grid = []
    with open(filename) as f:
        for l in f.readlines():
            grid.append([int(x) for x in l.split()])

    f.close()
    # print 'Exiting readGrid'
    return grid


def outputGrid(grid, start, goal, path):
    # print('In outputGrid')
    filenameStr = 'path.txt'

    # Open filename
    f = open(filenameStr, 'w')

    # Mark the start and goal points
    grid[start[0]][start[1]] = 'S'
    grid[goal[0]][goal[1]] = 'G'

    # Mark intermediate points with *
    for i, p in enumerate(path):
        if i > 0 and i < len(path) - 1:
            grid[p[0]][p[1]] = '*'

    # Write the grid to a file
    for r, row in enumerate(grid):
        for c, col in enumerate(row):

            # Don't add a ' ' at the end of a line
            if c < len(row) - 1:
                f.write(str(col) + ' ')
            else:
                f.write(str(col))

        # Don't add a '\n' after the last line
        if r < len(grid) - 1:
            f.write("\n")

    # Close file
    f.close()


def InList(node, theList):
    for n in theList:
        if n.value == node.value:
            return True
    return False


def printNodeList(l):
    for node in l:
        print(node.value)


# This creates our heuristic that calculates the distance of our current
# location to our goal. Manhattan distance.
def heuristic(currentloc, goal):
    return abs(currentloc[0] - goal[0]) + abs(currentloc[1] - goal[1])


# Returns all adjacent locations for node that are free space
def getChildren(location, grid):

    result = []

    up = location[:]
    up[0] -= 1
    if up[0] > -1 and grid[up[0]][up[1]] != 0:
        result.append(up)

    right = location[:]
    right[1] += 1
    if right[1] < len(grid[right[0]]) and grid[right[0]][right[1]] != 0:
        result.append(right)

    down = location[:]
    down[0] += 1
    if down[0] < len(grid) and grid[down[0]][down[1]] != 0:
        result.append(down)

    left = location[:]
    left[1] -= 1
    if left[1] > -1 and grid[left[0]][left[1]] != 0:
        result.append(left)

    return result


# Gets all children for node and adds them to the openList if possible
def expandNode(node, openList, openListCopy, closedList, grid, goal):

    children = getChildren(node.value, grid)
    for c in children:
        if node.t == "G":
            nd = Node(c, node, heuristic(node.value, goal), 0, "G")
            if not InList(nd, closedList) and not InList(nd, openListCopy):
                # calculate the heuristic cost, set c.h field
                openList.put(nd)
                openListCopy.append(nd)
        if node.t == "A":
            pathCost = grid[c[0]][c[1]] + node.g
            nd = Node(c, node, heuristic(node.value, goal), pathCost, "A")
            if not InList(nd, closedList) and not InList(nd, openListCopy):
                # calculate the heuristic cost, set c.h field
                openList.put(nd)
                openListCopy.append(nd)


# Sets the path variable by inserting each node on the current node's path
def setPath(current, path):
    # print('In setPath')

    # While not at the root, append each node's parent
    while current.parent != '':
        path.insert(0, current.parent.value)
        current = current.parent


def uninformedSearch(type, grid, start, goal):
    print('\nStarting search, type: %s start: %s goal: %s' % (type, start, goal))

    # Set initial variables
    # newNode = Node(c, node, heuristic(node.value, goal), 0, "G")
    current = Node(start, '', heuristic(start, goal), 0, type)
    path = []

    # The open list is a priority queue
    openList = queue.PriorityQueue()

    # List of nodes in the open list
    # This is needed because you cannot iterate over a Queue object
    openListCopy = []

    # Initially, push the root node onto the open list
    openList.put(current)
    openListCopy.append(current)

    # List of expanded nodes
    closedList = []

    # Track the number of expanded nodes
    numExpanded = 0

    # While we are not at the goal and we haven't expanded all nodes
    while not openList.empty():

        # Pop off closed list
        current = openList.get()

        # Add to closed list
        closedList.append(current)

        # Check for goal
        if current.value == goal:
            break

        else:

            # Expand this node
            expandNode(current, openList, openListCopy, closedList, grid, goal)

            # Data
            numExpanded += 1

    # If we found the goal, then build the final path
    if not openList.empty() or current == goal:
        # Set the path variable
        setPath(current, path)

        # Append the goal because setPath doesn't add that
        path.append(goal)
    #     print("Path found - Success!")
    # if openList.empty() and current != goal:
    #     print("Path NOT found - Failed!")

    return [path, numExpanded]


def main():
    print('Starting main function for uninformedSearch program')
    grid = readGrid('gridfile.txt')
    print('Grid read from file: %s' % grid)

    algo = input('Input \'G\' or \'A\'\n')

    if algo != 'G' and algo != 'A':
        print('Invalid input')

    else:
        if algo == 'greedy':
            print('testing Greedy search')
        else:
            print('testing A* search')
        start = [1, 1]
        goal = [4, 3]
        [p, numExpanded] = uninformedSearch(algo, grid, start, goal)
        if len(p) > 0:
            print('\nFinal path: %s' % p)
            print('Number of states expanded: %d' % numExpanded)
            outputGrid(grid, start, goal, p)
            print('\nPath found - Success!')
        else:
            print('Path not found - Failed!')


if __name__ == '__main__':
    main()
    print('\nExiting normally, thank you for using our search! :)')
