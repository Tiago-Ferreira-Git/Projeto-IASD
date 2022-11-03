import search
import time 

class RTBProblem(search.Problem):
    puzzle_dimension = None
    initial = None
    algorithm = None
    initial_index = None
    def __init__(self) -> None:
        pass
    
    def setAlgorithm(self):
        """Sets the uninformed search algorithm chosen"""    
        self.algorithm = search.iterative_deepening_search #breadth_first_graph_search

    def solve(self):
        """Calls the uninformed search algorithm chosen. """
        return self.algorithm(self)

    def load(self, fh):
        board = list()
        blank = []
        for line in fh:           
            line = line.rstrip("\n")           
            if line.startswith('#'):
                continue       
            else:        
                words = line.split(" ")
                if len(words) == 1:
                    try:
                        self.puzzle_dimension = int(words[0])
                        i = 0
                    except ValueError: 
                        print("Dimension not valid")
                        exit()
                else:
                    j = 0
                    for word in words:
                        if len(word) > 7:
                            if word[:7] == "initial":
                                self.initial_index = (i,j)
                        j += 1
                    board.append(words)
                    if(i == self.puzzle_dimension-1): break
                    i += 1
        self.initial = *(tuple(row) for row in board),


    def actions(self, state):
        n = self.puzzle_dimension
        for i in range(n):
            for j in range(n):
                if state[i][j][0] == 'e':
                    if i != n-1:
                        if not(state[i+1][j][0] == 'e' or state[i+1][j][-3] == 'n' or state[i+1][j][0] == 'g'  or state[i+1][j][0] == 'i'): 
                            yield (i, j, "d")
                    if i != 0:
                        if not(state[i-1][j][0] == 'e' or state[i-1][j][-3] == 'n' or state[i-1][j][0] == 'g'  or state[i-1][j][0] == 'i'): 
                            yield (i, j, "t")
                    if j != 0:
                        if not(state[i][j-1][0] == 'e' or state[i][j-1][-3] == 'n' or state[i][j-1][0] == 'g'  or state[i][j-1][0] == 'i'): 
                            yield (i, j, "l")
                    if j != n-1:
                        if not( state[i][j+1][0] == 'e' or state[i][j+1][-3] == 'n' or state[i][j+1][0] == 'g'  or state[i][j+1][0] == 'i'): 
                            yield (i, j, "r")



    def result(self, state, action):
        n = self.puzzle_dimension+2
        i, j, dir = action
        if dir == 't':
            return self.swap(state, i, j, i-1, j)
        elif dir == 'd':
            return self.swap(state, i, j, i+1, j)
        elif dir == 'l':
            return self.swap(state, i, j, i, j-1)
        elif dir == 'r':
            return self.swap(state, i, j, i, j+1)
    
    def swap(self, state, i1, j1, i2, j2):
        new_state = list(state)
        if i1 == i2:
            row = list(new_state[i1])
            row[j1], row[j2] = row[j2], row[j1]
            new_state[i1] = tuple(row)
        else:
            row1 = list(new_state[i1])
            row2 = list(new_state[i2])
            row1[j1], row2[j2] = row2[j2], row1[j1]
            new_state[i1] = tuple(row1)
            new_state[i2] = tuple(row2)
        return tuple(new_state)


    def goal_test(self, state):
        """Return  True if the state is a goal"""
        return self.isSolution(state)

    def isSolution(self,state):
    
        self.board = state
        # register in i,j the coordinates of the initial tile
        i,j = self.initial_index
        # find where the next tile in path must be
        next = self.board[i][j].split("-")
        next = next[1]
        # move search to the next tile
        while next != "no" and next != "goal":
            i, j, next = self.Check(i, j, next)
        if next == "no":
            return False
        elif next == "goal":
            return True
        else:
            print("Something went wrong.")
            exit()

    def Check(self, i, j, next):
        i, j = move(i, j, next)
        if (0 <= j < self.puzzle_dimension) and (0 <= i < self.puzzle_dimension):     
            current = self.board[i][j].split("-")
            prev = reverse(next)
            if current[0] == prev:
                next = current[1]
            elif current[1] == prev:
                next = current[0]
            else:
                return i, j, "no"
            return i, j, next
        else:
            return 0,0,"no"

def move(i, j, next):
    if next == "left":
        j-=1
    elif next == "right":
        j+=1
    elif next == "top":
        i-=1
    elif next == "down":
        i+=1
    else:
        print("error")
        return (-1,-1)
    return (i, j)

def reverse(str):
    if str == "left":
        return("right")
    elif str == "right":
        return("left")
    elif str == "top":
        return("down")
    elif str == "down":
        return("top")
    else:
        return "goal"
