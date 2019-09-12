import os
import sys
import copy

moveNum = {1:"RIGHT", 2:"LEFT", 3:"UP", 4:"DOWN"}
moveStr = {"RIGHT":1, "LEFT":2, "UP":3, "DOWN":4}

class Node(object):
    def __init__(self, state, action_history, gn, hn):
        # You may add more attributes as necessary
        self.state = state
        self.action_history = action_history
        self.gn = gn
        self.hn = hn

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # You may add more attributes as necessary
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.solvable = True
        self.priorityQueue = list()

    def solve(self):
        # TODO: Write your code here
        # return: a list of actions like: ["UP", "DOWN"]
        startNode = Node(init_state, list(), 0, self.heuristicFunction(init_state))
        self.priorityQueue.push(startNode)
        while True:
            node = self.pop()
            if self.isGoalNode(node):
                break
            new_frontier_nodes = self.generateFrontierNode(node)
            self.priorityQueue.pushAll(new_frontier_nodes)
        return node.action_history
            
    # h1 heuristic: number of misplaced tiles
    def calcNumMisplacedTiles(self, curr_state):
        num = 1
        numMisplaced = 0
        for i in range(3):
            for j in range(3):
                if (curr_state[i][j] != num):
                    numMisplaced += 1
                num +=1
        if (curr_state[2][2] == 0):
            numMisplaced -= 1
        return numMisplaced

    # h2 heuristic: total Manhattan-Distance
    def calcDistanceSum(self, state):
        sum = 0
        for i in range(9):
            sum += self.getDistance(i, state)
        return sum

    def getDistance(self, number, state):
        indexGoal = self.getIndex(number, goal_state)
        indexCurrentState = self.getIndex(number, state)
        distance = abs(indexGoal[0] - indexCurrentState[0]) + abs(indexGoal[1] - indexCurrentState[1])
        return distance

    def getIndex(self, number, state):
        for idxOuter, row in enumerate(state):
            for idxInner, elem in enumerate(row):
                if elem == number:
                    return (idxOuter, idxInner)

    # h3 = (h1 + h2)/2
    def heuristicFunction(self, state):
        return (self.calcDistanceSum(state) + self.calcNumMisplacedTiles(state)) / 2

    # Calculate f(n) = g(n) + h3(n)
    def calc_fn(self, node):
        return len(node.action_history) + self.heuristicFunction(node.state)

    # State-related methods
    def findPossibleMoves(self, state):
        moves = list()
        zeroRow = 0
        zeroCol = 0
        for i in range(3):
            for j in range(3):
                if (state[i][j] == 0):
                    zeroRow = i
                    zeroCol = j

        if (zeroRow == 0):
            moves.append(moveStr["UP"])
        elif (zeroRow == 1):
            moves.append(moveStr["UP"])
            moves.append(moveStr["DOWN"])
        elif (zeroRow == 2):
            moves.append(moveStr["DOWN"])

        if (zeroCol == 0):
            moves.append(moveStr["LEFT"])
        elif (zeroCol == 1):
            moves.append(moveStr["LEFT"])
            moves.append(moveStr["RIGHT"])
        elif (zeroCol == 2):
            moves.append(moveStr["RIGHT"])

        return moves

    def isGoalNode(self, node):
        return self.calcNumMisplacedTiles(node.state) == 0

    def generateFrontierNode(self, node):
        possibleMoves = self.findPossibleMoves(node.state)
        for move in possibleMoves:
            newState = self.getNextState(node.state, move)

    def getNextState(self, state, move):
        indexOfZero = self.getIndex(0, state)
        nextState = copy.deepcopy(state)
        if(move == moveStr.RIGHT):
            nextState[indexOfZero[0]][indexOfZero[1]] = nextState[indexOfZero[0]][indexOfZero[1] - 1]
            nextState[indexOfZero[0]][indexOfZero[1] - 1] = 0
        elif(move == moveStr.LEFT):
            nextState[indexOfZero[0]][indexOfZero[1]] = nextState[indexOfZero[0]][indexOfZero[1] + 1]
            nextState[indexOfZero[0]][indexOfZero[1] + 1] = 0
        elif(move == moveStr.DOWN):
            nextState[indexOfZero[0]][indexOfZero[1]] = nextState[indexOfZero[0] - 1][indexOfZero[1]]
            nextState[indexOfZero[0] - 1][indexOfZero[1]] = 0
        else:
            nextState[indexOfZero[0]][indexOfZero[1]] = nextState[indexOfZero[0] + 1][indexOfZero[1]]
            nextState[indexOfZero[0] + 1][indexOfZero[1]] = 0
        return nextState

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
