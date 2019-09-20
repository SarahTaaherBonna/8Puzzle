"""
Group 48
Benn Tay Guobin (A0167647N)
Chong Chee Yuan (A0182546Y)
Sarah Taaher Bonna (A0171268B)
"""

import os
import sys
from collections import deque
import copy

#Attributes of each tile (node)
class NodeAttributes:
    def __init__(self, state, parent, move):
        self.state = tuple(state) #Initially initalState
        self.parent = parent #Initially None
        self.move = move #Initially None

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.state < other.state

    def __hash__(self):
        return hash(self.state)

#Global variables to be used
goalNode = None
nodesGenerated = 0 #For report
maxFrontierSize = 0 #For report
initialState = list()
boardSide = 3 #Number of elements in each row
boardLen = 9 #Total number of elements
actions = list()

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.transformedGoalState = list()
        self.actions = list()
       
    def breadthFirstSearch(self, init_state):
        global maxFrontierSize, goalNode, nodesGenerated

        #Transfer the data from 2D array to list
        #because easier to deal with list than 2D array
        for i in range(boardSide):
            for j in range(boardSide):
                initialState.append(init_state[i][j])
                self.transformedGoalState.append(goal_state[i][j])

        self.transformedGoalState = tuple(self.transformedGoalState)
                
        explored = set()
        initialNode = NodeAttributes(initialState, None, None)
        queue = deque([initialNode])
        explored.add(initialNode)

        while queue:
            node = queue.popleft() #Remove and return an element (node) from the left side of the deque  

            if node.state == self.transformedGoalState:
                goalNode = node
                return queue

            #Visit neighbours around the node
            neighbours = self.expand(node) 

            for neighbour in neighbours:
                nodesGenerated += 1
                if neighbour not in explored:
                    queue.append(neighbour)
                    explored.add(neighbour)
                    
            if len(queue) > maxFrontierSize:
                maxFrontierSize = len(queue)

    #Expand the node to visit its neighbours, and call move function
    def expand(self, node):
        neighbours = list()

        for i in range(1, 5):
            newState = self.move(node.state, i)
            if newState:
                neighbours.append(NodeAttributes(newState, node, i))

        return neighbours

    #Move to check whether to move up, down, left or right
    #depending on the position passed from expanding the node.
    #Move accordingly and update the newNodeState list
    def move(self, nodeState, position):
        newNodeState = list(copy.deepcopy(nodeState)) #Copy nodeState list into newNodeState list, nodeState is node.state
        i = newNodeState.index(0) #Find the position of 0 in the list

        if position == 1:  #Up 
            #if i is not found from 0 to 2 i.e. the top row, then can move up
            if i not in [0, 1 , 2]:
                temp = newNodeState[i - boardSide]
                newNodeState[i - boardSide] = newNodeState[i]
                newNodeState[i] = temp
                return newNodeState
            else:
                return None

        if position == 2:  #Down 
            #if i is not found from 6 to 8, i.e. bottom row, then can move down
            if i not in [6, 7, 8]:
                temp = newNodeState[i + boardSide]
                newNodeState[i + boardSide] = newNodeState[i]
                newNodeState[i] = temp
                return newNodeState
            else:
                return None

        if position == 3:  #Left
            #i not found in 0, 3, 6, i.e. the leftmost row, then can move left
            if i not in [0, 3, 6]:
                temp = newNodeState[i - 1]
                newNodeState[i - 1] = newNodeState[i]
                newNodeState[i] = temp
                return newNodeState
            else:
                return None

        if position == 4:  #Right
            #i not found in 2, 5, 8, i.e. the rightmost row, then can move right
            if i not in [2, 5, 8]:
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
        while currentNode and (initialState != currentNode.state):
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
                movement = "UNSOLVABLE"
                actions.insert(0, movement)
                return actions

            currentNode = currentNode.parent

        return actions

    def solve(self):
        self.breadthFirstSearch(init_state)
        if not goalNode:
            return ["UNSOLVABLE"]
        actions = self.backtrack()
        actions.pop(0)
        return actions
        # TODO: Write your code here
        # return: a list of actions like: ["UP", "DOWN"]
        #pass

    # You may add more (helper) methods if necessary.
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.


if __name__ == "__main__":
    # do NOT modify below
    if len(sys.argv) != 3: # change to 5 to print nodesGenerated and maxFrontierSize
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
        
    #with open(sys.argv[3], 'a') as f:
        #f.write(str(nodesGenerated)+'\n')

    #with open(sys.argv[4], 'a') as f:
        #f.write(str(maxFrontierSize)+'\n')
