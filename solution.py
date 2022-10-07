#from os import listdir
#import time
import search

"""
Name of the class: RTBProblem
     
Methods:
    __init__: Initializes an object of this class.
    Load: Loads a RTB puzzle.
    Printb: Prints the RTB puzzle.
    isSolution: Verifies if the loaded RTB puzzle is the solution.
    Check: Checks if there is any path to go to in the RTB puzzle
    
Variables:
    board: Matrix that holds the loaded RTB puzzle board.
    initial_index: Holds the coordinates of the initial piece of the RTB puzzle.      
    puzzle_dimension: Int variable to save the dimension of the puzzle   
"""
class RTBProblem(search.Problem):
    board = None
    initial_index = None
    puzzle_dimension = None
    
    def __init__(self) -> None:
        pass
      
    
    """
    Name of the method: Load.
        
    Description: Loads a RTB puzzle board from the file object "fh" and stores 
    it as a matrix in the variable "board" of this class. As it loads the puzzle
    board it also finds where the initial piece of the puzzle is and stores it's 
    coordinates in the variable "initial_index" of this class. It also ignores
    all coments present in the file object. 
        
    Parameters:
        self: Object of this class.
        fh: Object that holds in text format the moves of each tile of a RTB puzzle.
        
    Return: Does not return anything.   
    """
    def load(self, fh):
        board = list()
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
                    i += 1
        self.board = board
     
        
     
    """
    Name of the method: Printb.
        
    Description: Prints the loaded RTB puzzle board.
        
    Parameters:
        self: Object of this class.
        
    Return: Does not return anything.  
    """     
    def Printb(self):
        print(self.board)    


     
        
    """ 
    Name of the method: isSolution.
        
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
        
    Return: Returns 1 if the loaded puzzle is a solution, 0 otherwise. 
    """                  
    def isSolution(self):
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



    """ 
    Name of the method: Check
        
    Description: Checks if there is any path to go to in the RTB puzzle
        
    Parameters:
        self: object of the class RTBProblem
        i: 
        j:
        next:
        
    Return: Returns the coordinates of the next tile in path and the next
    movement to reach it.
    """
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

           
""" 
Name of the function: move
    
Description: Simulates the movement of the ball between the tiles depending 
on the move to be made, passed by argument in the variable "next". As it moves 
to the next tile, it also updates the coordinates of the ball.
    
Parameters:
    i: Current coordinate of the ball on the rows of the puzzle
    j: Current coordinate of the ball on the columns of the puzzle
    next: next move to be made by the ball in the puzzle
    
Return: Returns the new coordinates of the ball in the RTB puzzle
"""   
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
        print("Something went wrong.")
        exit()
    return (i, j)



""" 
Name of the function: reverse
    
Description: Gets a string with the opposite direction passed in "str"
    
Parameters:
    str: String that holds a direction of a certain tile. 
    
Return: Returns a string 
"""   
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


"""
if __name__ == "__main__":
    
    for files in listdir():
        if files[-3:] == "dat":
            with open(files,"r") as fh:
                
                rtbp = RTBProblem()
                rtbp.Load(fh)
                start_time = time.time()
                print(rtbp.isSolution())
                print(f"No ficheiro {files} demorou {time.time()-start_time}")
""" 