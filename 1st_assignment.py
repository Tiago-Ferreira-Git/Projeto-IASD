import search
from copy import deepcopy

class State():
    def __init__(self) -> None:
        self.board = None
        self.blanks = None


class RTBProblem(search.Problem):

    def __init__(self) -> None:
        # To save the initial state 
        self.initial = None
        # cordinates of the "start" tile
        self.start = None
        # the algoritm to be used
        self.algorithm = None

    def result(self, state, action):
        temp = action.split("-")
        print(action)
        i, j, dir = int(temp[0]), int(temp[1]), temp[2]
        new_blanks = list(state.blanks)
        new_board = list(state.board)

        if dir == "up":
            swap(new_board, new_blanks, (i, j), (i-1, j))
        elif dir == "down":
            swap(new_board, new_blanks, (i, j), (i+1, j))
        elif dir == "left":
            swap(new_board, new_blanks, (i, j), (i, j-1))
        elif dir == "right":
            swap(new_board, new_blanks, (i, j), (i, j+1))
            
        new_state = State() 
        new_state.board = tuple(new_board)
        new_state.blanks = tuple(new_blanks)
        #print(new_blanks)
        return new_state
    
    def actions(self, state):
        """
        The possible actions are moving a blank tile to all the adjacent tiles, this will be:
        <i>-<j>-<dir>
        where i, j are the coordinates of a blank tile and dir, the direction where it will be moved
        """
        #TODO: dir could be a number for the increment in coordinates -> more efficient (worth it?)

        action_list = []
        for tile in state.blanks:
            i, j = tile[0], tile[1]
            if self.is_moveable(state.board, i-1, j):
                action_list.append(f"{i}-{j}-up")
            if self.is_moveable(state.board, i+1, j):
                action_list.append(f"{i}-{j}-down")
            if self.is_moveable(state.board, i, j-1):
                action_list.append(f"{i}-{j}-left")
            if self.is_moveable(state.board, i, j+1):
                action_list.append(f"{i}-{j}-right")
        return action_list
    
    def goal_test(self, state):
        # the first tile
        i, j = self.start[0], self.start[1]
        # find where the next tile in path must be
        next = state.board[i][j].split("-")
        next = next[1]
        # move search to the next tile
        while next != "no" and next != "goal":
            i, j, next = check(state, i, j, next)
        if next == "no":
            return False
        elif next == "goal":
            return True
        else:
            print("tenso, algo deu merda")
            exit()
    

    def load(self, fh):
        board = list()
        blanks = []
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
                                self.start = (i,j)
                        if word == "empty-cell":
                            blanks.append((i,j))               
                        j += 1
                    
                    board.append(tuple(words))
                    if(i == self.puzzle_dimension-1): break
                    i += 1
        self.initial = State()            
        self.initial.board = tuple(board)
        self.initial.blanks = tuple(blanks)

    def setAlgorithm(self):
        self.algorithm = search.breadth_first_tree_search
    
    def solve(self):
        return self.algorithm(self)

    # ----------------------------- Extra functions ----------------------------------- #

    def is_moveable(self, board, i,j):
        if i < 0 or j < 0 or i > self.puzzle_dimension-1 or j > self.puzzle_dimension-1:
            return False
        tile = board[i][j].split("-")
        if tile[0] == "initial" or tile[0] == "goal" or tile[-1] == "not" or tile[0] == "empty":
            return False
        else:
            return True

    # def find_initial_and_blanks(self):
    #     """
    #     find initial -> find where the initial piece is. 
    #     """
    #     blanks = []
    #     for row in self.board:
    #         for column in row:
    #             if  "empty" in (column.split("-")):
    #                 blanks.append([self.board.index(row), row.index(column)])
    #             elif "initial" in (column.split("-")):
    #                 self.start = (self.board.index(row), row.index(column))
    #     return blanks

    def printb(self):
        print(self.board)
    

def check(state, i, j, next):
    i, j = move(i, j, next)
    current = state.board[i][j].split("-")
    prev = reverse(next)
    if current[0] == prev:
        next = current[1]
    elif current[1] == prev:
        next = current[0]
    else:
        return i, j, "no"
    return i, j, next

# board is a list of tuples
def swap(board, blanks,  first, second):
        # both on the same row
        if first[0] == second[0]:
            row = list(board[first[0]])
            row[first[1]], row[second[1]] = row[second[1]], row[first[1]]
            board[first[0]] = tuple(row)
            blanks.remove((first[0], first[1]))
            blanks.append((second[0], second[1]))
        else:
            row1 = list(board[first[0]])
            row2 = list(board[second[0]])
            row1[first[1]], row2[second[1]] = row2[second[1]], row1[first[1]]
            board[first[0]] = tuple(row1)
            board[second[0]] = tuple(row2)
            blanks.remove((first[0], first[1]))
            blanks.append((second[0], second[1]))

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
        exit()
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


if __name__ == "__main__":
    rtbp = RTBProblem()
    with open("testes/pub04.dat") as file:
        rtbp.load(file)
        rtbp.setAlgorithm()
        solution = rtbp.solve()
        print(solution.path())

   
   
#comentário
#tamanho do puzzle
#configuração do puzzle linha por linha
#N caracteres separados por um espaço
#files termina com um espaço em branco