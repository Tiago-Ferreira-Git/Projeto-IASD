from os import listdir
import search
import time

"""
Name of the class: RTBProblem
     
Methods:
    __init__: Initializes an object of this class.
    Load: Loads a RTB puzzle.
    goal_test: Verifies if the loaded RTB puzzle is the solution.
    Check: Checks if there is any path to go to in the RTB puzzle
    result: Return  the state that results from executing the given action
    actions: Return the state that can be executed in the given state
    
Variables:
    initial: tuple that holds the loaded RTB puzzle board.
    initial_index: Holds the coordinates of the initial piece of the RTB puzzle.      
    puzzle_dimension: Int variable to save the dimension of the puzzle. 
    algorithm = variable that holds the algorithm chosen.
"""
class RTBProblem(search.Problem):
    puzzle_dimension = None
    initial = None
    algorithm = None
    initial_index = None
    
    def __init__(self) -> None:
        self.initial = ()
    
    def load(self, fh):
        """
        Name of the method: Load.
            
        Description: Loads a RTB puzzle board from the file object "fh" and stores 
        it as a matrix in the variable "board" of this class. As it loads the puzzle
        board it also finds where the initial piece of the puzzle is and stores it's 
        coordinates in the variable "initial_index" of this class.
        While loading we find the number of empty spaces and we keep the first empty
        space coordinates and then save this number in the board position (concactnated).
        For simplicity, we also get keep only the first letters of each word separated by
        "-" so we don't have to compare long strings (and save memory).
        It also ignores all coments present in the file object. 
            
        Parameters:
            self: Object of this class.
            fh: Object that holds in text format the moves of each tile of a RTB puzzle.
            
        Return: Does not return anything.    
        """
        board = (())
        initial_empty = None
        empty_counter = 0
        initial = False
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
                        if word[0] == "i":
                            self.initial_index = (i,j)
                        if word[0] == "g":
                            self.goal_index = (i,j)
                        if word[0] == "e":
                            empty_counter += 1
                            if not initial:
                                initial = True
                                initial_empty = (i,j)  
                        w = word.split('-')
                        if len(w) == 2:
                            words[j] = (w[0][0] + w[1][0]) + " "
                        elif len(w) == 3:
                            words[j] = (w[0][0] + w[1][0] + w[2][0])
                        j += 1
                    
                    board += (tuple(words))
                    if(i == self.puzzle_dimension-1): break
                    i += 1
        board = list(board)            
        board[(initial_empty[0] * self.puzzle_dimension)+initial_empty[1]] = board[(initial_empty[0] * self.puzzle_dimension)+initial_empty[1]][:2] + str(empty_counter)
        board = tuple(board)
        self.initial += board

    def result(self, state,action):
        """Return  the state that results from executing the given action""" 
        i,move = action   
        board = ()
        new_state = ()
        
        board = list(state)
        if move == "u":
            board[i], board[i-self.puzzle_dimension] =  board[i-self.puzzle_dimension], board[i] 
        elif move == "d":
            board[i], board[i+self.puzzle_dimension]=  board[i+self.puzzle_dimension], board[i]
        elif move == "l": 
            board[i], board[i-1] =  board[i-1], board[i] 
        elif move == "r":      
            board[i], board[i+1] =  board[i+1], board[i]
            
        new_state += tuple(board)
        return new_state

    def actions(self, state):
        """Return the state that can be executed in the given state"""
        n_empty = None
        empty_counter = 0
        
        for i,row in enumerate(state):
            if (state[i])[0] == "e":
                if (state[i])[2] != " ":
                    n_empty = int((state[i])[2])
                if(i+self.puzzle_dimension < self.puzzle_dimension**2):
                    if((state[i+self.puzzle_dimension])[2] != "n" and (state[i+self.puzzle_dimension])[0] != "i"  and (state[i+self.puzzle_dimension])[0] != "g" and (state[i+self.puzzle_dimension])[0] != "e"):
                        yield (i,"d")
                if(0 <= i-self.puzzle_dimension):
                    if((state[i-self.puzzle_dimension])[2] != "n" and (state[i-self.puzzle_dimension])[0] != "i"  and (state[i-self.puzzle_dimension])[0] != "g" and (state[i-self.puzzle_dimension])[0] != "e"):
                        yield (i,"u")
                if( i%self.puzzle_dimension != 0 ):
                    if((state[i-1])[2] != "n" and (state[i-1])[0] != "i"  and (state[i-1])[0] != "g" and (state[i-1])[0] != "e"):
                        yield (i,"l")
                if(i % self.puzzle_dimension != self.puzzle_dimension-1 ):
                    if((state[i+1])[2] != "n" and (state[i+1])[0] != "i"  and (state[i+1])[0] != "g" and (state[i+1])[0] != "e"):
                        yield (i,"r")
                empty_counter += 1                    
            if n_empty == empty_counter: break

    
    def h(self, node):
        """
        This is a heuristic function for the A* algorithm. The path from the initial
        to the goal tiles will be meantioned ahead as "path". There is a "gap" in the 
        path if the state is not a solution. To measure the gap in the path this 
        function starts in the initial tile and goes trough the path until it fails, 
        then does the same starting in the goal tile. Meanwhile it counts the number 
        of tiles already in the path wich will be used later. When the 2 tiles where
        the path fails are found, the L1 norm between them is computed, that is the 
        distance (in number of tiles) between those 2 points wich is the minimum number
        of moves that would be required to solve the puzzle if all the right tiles were
        adjacent (and could move) to their final position. This value will be refered
        to as "norm". 
        For cases where multiple states have the same norm there is the need for another
        value to chose the best node to explore. For that, it's used the counter set up early
        and the result returned by this function is "norm + 1/counter" which benefits states 
        that have already more tiles in the path.
        
        Its trivial that this heuristic never overestimates the true cost to goal given
        that it assumes the tiles that need to move are just one move away from their final 
        position wich only happens in the best case and is highly unlikely.

        This heuristic is also consistent because when generating a new node n' from a 
        parent node n, there can only happen one of three things: the gap decreases by
        one or the gap stays the same or the gap increases. Because c(n,a,n') = 1 for 
        any n, n' and a:
            
            - If the gap increases, h(n') will be bigger than h(n) so 
                        h(n) < c(n,a,n') + h(n'),
                which proves consistency
            - If the gap stays the same, h(n') will be the same as h(n) so
                        h(n) < c(n,a,n') + h(n'),
                which proves consistency
            - If the gap decreses, h(n') will be equal to h(n)-1 so
                        h(n) = c(n,a,n') + h(n'),
                which proves consistency
            
        Because the term "1/counter" is always smaller than 1, it does not affect the
        results above.
        """
        state = node.state
        less = 999
        i1,j1 = self.initial_index
        next = state[(i1*self.puzzle_dimension)+j1][1] 
        while next != 'x' and next != 'g':
            i1, j1, next, prev = self.Check(i1, j1, next, state)

        if prev == 'l':
            next = 'r'
        elif prev == 'r':
            next = 'l'
        elif prev == 't':
            next = 'd'
        else:
            next = 't'    
        for i, cell in enumerate(state):
            if(cell[2] != "n" and cell[0] != "i"  and cell[0] != "g" and cell[0] != "e"):
                if cell[0] == next or cell[1] == next:
                    ip, jp = i/self.puzzle_dimension, i%self.puzzle_dimension
                    l1 = abs(i1-ip)+abs(j1-jp)
                    if l1 < less:
                        less = l1

        return less

        # i2,j2 = self.goal_index
        # next = state[(i2*self.puzzle_dimension)+j2][1]
        # while next != 'x' and not(i1 == i2 and j1==j2):
        #     i2, j2, next = self.Check(i2, j2, next, state)


        # return abs(i1-i2)+abs(j1-j2) + 1/cnt


    def setAlgorithm(self):
        """Sets the uninformed search algorithm chosen"""    
        self.algorithm = search.astar_search


    def solve(self):
        """Calls the uninformed search algorithm chosen. """
        return self.algorithm(self)


    def goal_test(self, state):
        """ 
        Name of the method: Goal Test.
            
        Description: Searches for the goal, starting at the initial tile. The 
        movement between tiles is made by finding what the next tile in path 
        must, by using the coordinates of the initial tile. As it goes through the
        tiles, the coordinates of the next tile are registered and it is verified
        if there is any path to go to at those coordinates. If there isn't any 
        path to go to and the next tile isn't a goal then it is returned false 
        indicating that the path was cut and it still hasn't reach a goal. Otherwise 
        it found a goal and it is returned true.
            
        Parameters:
            self: Object of this class.
            state: One node of the tree that we want to check if it is the solution or not.
            
        Return: Returns 1 if the loaded puzzle is a solution, 0 otherwise. 
        """
        i,j = self.initial_index
        # find where the next tile in path must be
        next = state[(i*self.puzzle_dimension)+j][1]
        # move search to the next tile
        while next != 'x' and next != 'g':
            i, j, next, _ = self.Check(i, j, next, state)

        if next == 'x':
            return False
        elif next == 'g':
            return True
        else:
            print("Something went wrong.")
            exit()
    
    def Check(self, i, j, next, state):
        """ 
        Name of the method: Check
            
        Description: Checks if there is any path to go to in the RTB puzzle
            
        Parameters:
            self: object of the class RTBProblem
            i: index of tuple as a matrix
            j: index of tuple as a matrix
            next:
            state: One node of the tree that we want to check if it is the solution or not.
            
        Return: Returns the coordinates of the next tile in path and the next
        movement to reach it.
        """
        j_, i_ = j, i
        if next == 'l':
            j_-=1
            prev = 'r'
        elif next == 'r':
            j_+=1
            prev = 'l'
        elif next == 't':
            i_-=1
            prev = 'd'
        else:
            i_+=1
            prev = 't'

        if (0 <= j_ < self.puzzle_dimension) and (0 <= i_ < self.puzzle_dimension):
            if state[(i_*self.puzzle_dimension)+j_][0] == prev:
                return (i_, j_, state[(i_*self.puzzle_dimension)+j_][1], prev)
            elif state[(i_*self.puzzle_dimension)+j_][1] == prev:
                return (i_, j_, state[(i_*self.puzzle_dimension)+j_][0], prev)
            else:
                return (i_, j_,'x', prev)
        else:
            return (i,j,'x', prev)

if __name__ == '__main__':
    for files in listdir("teste"):
        if files[-3:] == "dat":
            with open("teste/"+files,"r") as fh:
                #print(files)
                start_time = time.time()
                teste = RTBProblem()
                teste.setAlgorithm()
                teste.load(fh)
                teste.solve()
                print(f"No ficheiro {files} demorou {time.time()-start_time}")