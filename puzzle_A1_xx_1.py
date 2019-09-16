import os
import sys
from collections import deque
import copy

#Attributes of each tile (node)
class NodeAttributes:
    def __init__(self, state, parent, move):
        self.state = state #Initially initalState
        self.parent = parent #Initially None
        self.move = move #Initially None

    def _eq_(self, other):
        return self.state == other.state

    def _lt_(self, other):
        return self.state < other.state

#Global variables to be used
goalNode = NodeAttributes
nodesGenerated = 0 #For report
maxFrontierSize = 0 #For report
initialState = list()
goalState = list()
boardSide = 3 #Number of elements in each row
boardLen = 9 #Total number of elements

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
       
    def breadthFirstSearch(self, init_state):
        global maxFrontierSize, goalNode

        #Transfer the data from 2D array to list
        #because easier to deal with list than 2D array
        for i in range(boardSide):
            for j in range(boardSide):
                initialState.append(init_state[i][j])
                goalState.append(goal_state[i][j])

        # explored = set()
        explored = deque()
        # explored = list()
        queue = deque([NodeAttributes(initialState, None, None)])

        while queue:
            node = queue.popleft() #Remove and return an element (node) from the left side of the deque
            if node not in explored:
                # explored.insert(0, node)
                explored.appendleft(node)
            # explored.add(node)

            if node.state == goalState:
                goalNode = node
                return queue

            #Visit neighbours around the node
            neighbours = self.expand(node) 

            for neighbour in neighbours:
                if neighbour not in explored:
                    queue.append(neighbour)
                    # explored.insert(0, neighbour)
                    explored.appendleft(neighbour)
                    # explored.add(neighbour)
                    

            if len(queue) > maxFrontierSize:
                maxFrontierSize = len(queue)

    #Expand the node to visit its neighbours, and call move function
    def expand(self, node):
        global nodesGenerated
        nodesGenerated += 1
        neighbours = list()

        neighbours.append(NodeAttributes(self.move(node.state, 1), node, 1)) #Move up
        neighbours.append(NodeAttributes(self.move(node.state, 2), node, 2)) #Move down
        neighbours.append(NodeAttributes(self.move(node.state, 3), node, 3)) #Move left
        neighbours.append(NodeAttributes(self.move(node.state, 4), node, 4)) #Move right

        #Recursively find all the neighbours of the neighbours of the current neighbour
        #and store these in nodes
        nodes = [neighbour for neighbour in neighbours if neighbour.state] 

        return nodes

    #Move to check whether to move up, down, left or right
    #depending on the position passed from expanding the node.
    #Move accordingly and update the newNodeState list
    def move(self, nodeState, position):
        newNodeState = copy.copy(nodeState) #Copy nodeState list into newNodeState list, nodeState is node.state
        i = newNodeState.index(0) #Find the position of 0 in the list

        if position == 1:  #Up
            #if i is not found from 0 to 2 i.e. the top row, then can move up
            if i not in range(boardSide):
                temp = newNodeState[i - boardSide]
                newNodeState[i - boardSide] = newNodeState[i]
                newNodeState[i] = temp
                return newNodeState
            else:
                return None

        elif position == 2:  #Down
            #if i is not found from 6 to 8, i.e. bottom row, then can move down
            if i not in range(boardLen - boardSide, boardLen):
                temp = newNodeState[i + boardSide]
                newNodeState[i + boardSide] = newNodeState[i]
                newNodeState[i] = temp
                return newNodeState
            else:
                return None

        elif position == 3:  #Left 
            #i not equal to 0, 3, 6, i.e. the leftmost row, then can move left
            if i not in range(0, boardLen, boardSide):
                temp = newNodeState[i - 1]
                newNodeState[i - 1] = newNodeState[i]
                newNodeState[i] = temp
                return newNodeState
            else:
                return None

        elif position == 4:  #Right
            #i not equal to 2, 5, 8, i.e. the rightmost row, then can move right
            if i in range(boardSide - 1, boardLen, boardSide):
                temp = newNodeState[i + 1]
                newNodeState[i + 1] = newNodeState[i]
                newNodeState[i] = temp
                return newNodeState
            else:
                return None

    #Backtrack to find the moves taken to reach goal_state 
    #after it is known that goal_state can be reached
    def backtrack(self):
        currentNode = goalNode
        actions = list()

        while initialState != currentNode.state:
            if currentNode.move == 1:
                movement = 'Up'
            elif currentNode.move == 2:
                movement = 'Down'
            elif currentNode.move == 3:
                movement = 'Left'
            else:
                movement = 'Right'

            actions.insert(0, movement) #insert the movement at the front of the actions list

            if(len(actions) > 300): #if the number of actions goes more than 300, unsolvable
                actions.clear()
                movement = "Unsolvable"
                actions.insert(0, movement)
                return actions

            currentNode = currentNode.parent

        return actions

    def solve(self):
        self.breadthFirstSearch(init_state)
        actions = self.backtrack()
        return actions
        # TODO: Write your code here
        # return: a list of actions like: ["UP", "DOWN"]
        #pass

    # You may add more (helper) methods if necessary.
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.


if __name__ == "__main__":
    # do NOT modify below
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    init_state = [[0 for i in range(3)] for j in range(3)]
    goal_state = [[0 for i in range(3)] for j in range(3)]
    lines = f.readlines()

    i,j = 0, 0
    for line in lines:
        for number in line:
            if '0'<= number <= '8':
                init_state[i][j] = int(number)
                j += 1
                if j == 3:
                    i += 1
                    j = 0

    for i in range(1, 9):
        goal_state[(i-1)//3][(i-1)%3] = i
    goal_state[2][2] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')
