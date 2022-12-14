from os import listdir
import search
import time

class RTBProblem(search.Problem):
    puzzle_dimension = None
    initial = None
    algorithm = None
    initial_index = None
    blank = None
    def __init__(self) -> None:
        self.blank = []
        pass
      

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
                        if word == "empty-cell":
                            self.blank.append((i,j))               
                        j += 1
                    
                    board.append(words)
                    if(i == self.puzzle_dimension-1): break
                    i += 1
        self.initial = board
        self.initial.append(self.blank)
        self.initial = *(tuple(row) for row in board),
        
     
        

    def Printb(self):
        print(self.board) 
    
    
    
    def result(self, state,action):
        """Return  the state that results from executing the given action""" 
        i,j,move = action   
        state = list(state)
        for g,tupple in enumerate(state[-1]):
            if tupple == (i,j):
                state[-1] = state[-1][:g] + state[-1][g+1:]
        if move == "up":
            state[i] = list(state[i])
            state[i-1] = list(state[i-1])
            state[i][j],state[i-1][j] = state[i-1][j],state[i][j]
            state[i] = tuple(state[i])
            state[i-1] = tuple(state[i-1])
            state[-1] = state[-1] + ((i-1,j),)         
            state = tuple(state)
            return state
        elif move == "down":
            state[i] = list(state[i])
            state[i+1] = list(state[i+1])
            state[i][j],state[i+1][j] = state[i+1][j],state[i][j]
            state[i] = tuple(state[i])
            state[i+1] = tuple(state[i+1])
            state[-1] = state[-1] + ((i+1,j),)   
            state = tuple(state)
            return state

        elif move == "left": 
            state[i] = list(state[i])
            state[i][j],state[i][j-1] = state[i][j-1],state[i][j]
            state[i] = tuple(state[i])
            state[-1] = state[-1] + ((i,j-1),)       
            state = tuple(state)
            return state

        elif move == "right":        
            state[i] = list(state[i])
            state[i][j],state[i][j+1] = state[i][j+1],state[i][j]
            state[i] = tuple(state[i])
            state[-1] = state[-1] + ((i,j+1),)   
            state = tuple(state)
            return state

    def actions(self, state):
        """Return the state that can be executed in the given state"""
        blank_spaces = list()
        
        for i,j in state[-1]:
            if(j+1 < self.puzzle_dimension):
                if((state[i][j+1])[-3:] != "not" and (state[i][j+1])[:7] != "initial"  and (state[i][j+1])[:4] != "goal"):
                    blank_spaces.append((i,j,"right"))
            if(0 <= i-1):
                if((state[i-1][j])[-3:] != "not" and (state[i-1][j])[:7] != "initial"  and (state[i-1][j])[:4] != "goal"):
                    blank_spaces.append((i,j,"up"))
            if( 0 <= j-1):
                if((state[i][j-1])[-3:] != "not" and (state[i][j-1])[:7] != "initial"  and (state[i][j-1])[:4] != "goal"):
                    blank_spaces.append((i,j,"left"))
            if(i+1 < self.puzzle_dimension):
                if((state[i+1][j])[-3:] != "not" and (state[i+1][j])[:7] != "initial"  and (state[i+1][j])[:4] != "goal"):
                    blank_spaces.append((i,j,"down"))
        
        return blank_spaces
        



        pass
    def goal_test(self, state):
        """Return  True if the state is a goal"""
        return self.isSolution(state)
    def setAlgorithm(self):
        """Sets the uninformed search algorithm chosen"""    
        self.algorithm = search.iterative_deepening_search
        pass
    def solve(self):
        """Calls the uninformed search algorithm chosen. """
        return self.algorithm(self)



    def isSolution(self,state):
        
        self.board = state[:-1]
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
    #print(next)
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

if __name__ == '__main__':
    for files in listdir("teste"):
        if files[-3:] == "dat":
            with open("teste/"+"pub07.dat","r") as fh:
                #print(files)
                start_time = time.time()
                teste = RTBProblem()
                teste.setAlgorithm()
                teste.load(fh)
                print(teste.solve())
                print(f"No ficheiro {files} demorou {time.time()-start_time}")


