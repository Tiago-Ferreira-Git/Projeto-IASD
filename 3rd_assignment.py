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
        
    def h(self,node):
        to_determine = self.h_determinate(node.state)
        return self.puzzle_dimension**2/to_determine

    def h_determinate(self, state):
        counter = 1
        i,j = self.initial_index
        # find where the next tile in path must be
        next = state[(i*self.puzzle_dimension)+j][1]
        # move search to the next tile
        while next != 'x' and next != 'g':
            i, j, next = self.Check(i, j, next, state)
            counter += 1

        i,j = self.goal_index
        next = state[(i*self.puzzle_dimension)+j][1]
        # move search to the next tile
        while next != 'x' and next != 'g':
            i, j, next = self.Check(i, j, next, state)
            counter += 1





        return counter


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
            i, j, next = self.Check(i, j, next, state)

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
            if state[(i*self.puzzle_dimension)+j][0] == prev:
                return (i, j, state[(i*self.puzzle_dimension)+j][1])
            elif state[(i*self.puzzle_dimension)+j][1] == prev:
                return (i, j, state[(i*self.puzzle_dimension)+j][0])
            else:
                return i, j,'x'
        else:
            return 0,0,'x'
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