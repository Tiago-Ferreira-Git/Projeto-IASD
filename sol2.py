import search
import time
from os import listdir

ACTIONS = 0

class RTBProblem(search.Problem):
    puzzle_dimension = None
    initial = None
    algorithm = None
    initial_index = None
    def __init__(self) -> None:
        pass

    def setAlgorithm(self):
        """Sets the uninformed search algorithm chosen"""
        self.algorithm = search.iterative_deepening_search #depth_first_tree_search

    def solve(self):
        """Calls the uninformed search algorithm chosen. """
        return self.algorithm(self)

    def load(self, fh):
        board = list()
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith('#'):
                continue
            row = line.split(' ')
            if len(row) == 1:
                try:
                    self.puzzle_dimension = int(row[0])
                    i = 0
                except ValueError:
                    print("Dimension not valid")
                    exit()
            else:
                j = 0
                words = []
                for word in row:   
                    if word[0] == 'i':
                        self.initial_index = (i,j)
                    w = word.split('-')
                    if len(w) == 2:
                        words.append(w[0][0] + w[1][0])
                    elif len(w) == 3:
                        words.append(w[0][0] + w[1][0] + w[2][0])
                    j+=1
                board.append(words)
                if(i == self.puzzle_dimension-1): break
                i += 1
        self.initial = *(tuple(row) for row in board),


    def actions(self, state):
        global ACTIONS
        ACTIONS +=1
        n = self.puzzle_dimension
        for i in range(n):
            for j in range(n):
                if state[i][j][0] == 'e':
                    if j != n-1:
                        if not( state[i][j+1][0] == 'e' or state[i][j+1][-1] == 'n' or state[i][j+1][0] == 'g'  or state[i][j+1][0] == 'i'):
                            yield (i, j, 4)
                    if j != 0:
                        if not(state[i][j-1][0] == 'e' or state[i][j-1][-1] == 'n' or state[i][j-1][0] == 'g'  or state[i][j-1][0] == 'i'):
                            yield (i, j, 3)
                    if i != n-1:
                        if not(state[i+1][j][0] == 'e' or state[i+1][j][-1] == 'n' or state[i+1][j][0] == 'g'  or state[i+1][j][0] == 'i'):
                            yield (i, j, 2)
                    if i != 0:
                        if not(state[i-1][j][0] == 'e' or state[i-1][j][-1] == 'n' or state[i-1][j][0] == 'g'  or state[i-1][j][0] == 'i'):
                            yield (i, j, 1)


    def result(self, state, action):
        n = self.puzzle_dimension+2
        i, j, dir = action
        if dir == 1:
            return self.swap(state, i, j, i-1, j)
        elif dir == 2:
            return self.swap(state, i, j, i+1, j)
        elif dir == 3:
            return self.swap(state, i, j, i, j-1)
        elif dir == 4:
            return self.swap(state, i, j, i, j+1)

    def swap(self, state, i1, j1, i2, j2):
        new_state = list(state)
        if i1 == i2:
            row = list(new_state[i1])
            row[j1], row[j2] = row[j2], row[j1]
            new_state[i1] = tuple(row)
            if len(state) > self.puzzle_dimension:
                blanks = list(new_state[self.puzzle_dimension])
                i = blanks.index((i1,j1))
                blanks[i] = (i2,j2)
                new_state[self.puzzle_dimension] = tuple(blanks)
        else:
            row1 = list(new_state[i1])
            row2 = list(new_state[i2])
            row1[j1], row2[j2] = row2[j2], row1[j1]
            new_state[i1] = tuple(row1)
            new_state[i2] = tuple(row2)
            if len(state) > self.puzzle_dimension:
                blanks = list(new_state[self.puzzle_dimension])
                i = blanks.index((i1,j1))
                blanks[i] = (i2,j2)
                new_state[self.puzzle_dimension] = tuple(blanks)
        return tuple(new_state)

    #@profile
    def goal_test(self, state):
        i,j = self.initial_index
        # find where the next tile in path must be
        next = state[i][j][1]
        # move search to the next tile
        while next != 'x' and next != 'g':
            i, j, next = self.Check(i, j, next, state)
        if next == 'x':
            return False
        elif next == 'g':
            return True
        else:
            print("Something went wrong.")
            exit()
    
    #@profile
    def Check(self, i, j, next, state):
        if next == 'l':
            j-=1
            prev = 'r'
        elif next == 'r':
            j+=1
            prev = 'l'
        elif next == 't':
            i-=1
            prev = 'd'
        else:
            i+=1
            prev = 't'
        if (0 <= j < self.puzzle_dimension) and (0 <= i < self.puzzle_dimension):
            if state[i][j][0] == prev:
                return (i, j, state[i][j][1])
            elif state[i][j][1] == prev:
                return (i, j, state[i][j][0])
            else:
                return i, j,'x'
        else:
            return 0,0,'x'


if __name__ == "__main__":

    for files in listdir("testes"):
        if files[-3:] == "dat":
            with open("testes/"+files,"r") as fh:
                #print(files)
                start_time = time.time()
                teste = RTBProblem()
                teste.setAlgorithm()
                teste.load(fh)
                print(teste.solve())
                print(f"No ficheiro {files} demorou {time.time()-start_time}")
    #print(ACTIONS)

    # rtbp = RTBProblem()
    # with open("testes/pub01.dat") as file:
    #     rtbp.load(file)
    #     print(rtbp.initial)
    #     print(rtbp.initial_index)
    #     print(rtbp.goal_test(rtbp.initial))

        # actions = rtbp.actions(rtbp.initial)
        # print(actions)
        #for action in actions:
        #    print(rtbp.printb(rtbp.result(rtbp.initial, action)))
        # rtbp.setAlgorithm()
        # solution = rtbp.solve()
        # print(solution)
