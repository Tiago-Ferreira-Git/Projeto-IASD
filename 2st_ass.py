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
        initial_blank = False
        blanks = None
        first = 0
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
                    board.append(words)
                    for index,word in enumerate(words):
                        if len(word) > 7:
                            if word[:7] == "initial":
                                self.initial_index = (i,j)
                        if word == "empty-cell":     
                            if not initial_blank:
                                initial_blank = True
                                first = (i * self.puzzle_dimension)+j
                                blanks = (i,j)
                            else:
                                board[blanks[0]][blanks[1]] = f"{i}{j}"
                                blanks = (i,j)             
                        j += 1

                    if(i == self.puzzle_dimension-1): break
                    i += 1
        #self.initial = board
        #self.initial.append(self.blank)
        print(board)
        self.initial = *(tuple(row) for row in board), + (first),
        
     
        

    def Printb(self):
        print(self.board) 
    
    
    
    def result(self, state,action):
        """Return  the state that results from executing the given action""" 
        print()
        i,j,move,prev = action[0]
        
        state = list(state) 
        if prev !="i":
            state[prev[0]] = list(state[prev[0]])         
            
        if move == "up":
            state[i] = list(state[i])
            state[i-1] = list(state[i-1])
            state[i][j],state[i-1][j] = state[i-1][j],state[i][j]
            if prev != "i": 
                print(type(state[prev[0]][prev[1]]))
                state[prev[0]][prev[1]] = f"{i-1}{j}"
            else:
                state[-1] = ((i-1) * self.puzzle_dimension)+j
            state[i] = tuple(state[i])
            state[i-1] = tuple(state[i-1])
            if prev != "i":
                if(type(state[prev[0]]) != tuple): state[prev[0]] = tuple(state[prev[0]])
            state = tuple(state)
        elif move == "down":
            state[i] = list(state[i])
            state[i+1] = list(state[i+1])
            state[i][j],state[i+1][j] = state[i+1][j],state[i][j]
            if prev != "i": 
                state[prev[0]][prev[1]] = f"{i+1}{j}"
            else:
                state[-1] = ((i+1) * self.puzzle_dimension)+j
            state[i] = tuple(state[i])
            state[i+1] = tuple(state[i+1])
            if prev != "i":
                if(type(state[prev[0]]) != tuple): state[prev[0]] = tuple(state[prev[0]])
            
            state = tuple(state)

        elif move == "left": 
            state[i] = list(state[i])
            state[i][j],state[i][j-1] = state[i][j-1],state[i][j]
            if prev != "i": 
                state[prev[0]][prev[1]] = f"{i}{j-1}"
            else:
                state[-1] = ((i) * self.puzzle_dimension)+j-1
            state[i] = tuple(state[i])   
            if prev != "i":
                if(type(state[prev[0]]) != tuple): state[prev[0]] = tuple(state[prev[0]])
             
            state = tuple(state)

        elif move == "right":        
            state[i] = list(state[i])
            state[i][j],state[i][j+1] = state[i][j+1],state[i][j]
            state[i] = tuple(state[i])
            if prev != "i": 
                state[prev[0]][prev[1]] = f"{i}{j+1}"
            else:
                state[-1] = ((i) * self.puzzle_dimension)+j+1
            if prev != "i":
                if(type(state[prev[0]]) != tuple): state[prev[0]] = tuple(state[prev[0]])
            
            state = tuple(state)
        return state

    def actions(self, state):
        """Return the state that can be executed in the given state"""
        blank_spaces = list()
        initial = state[-1]
        i = int(initial/self.puzzle_dimension)
        j = initial%self.puzzle_dimension
        next = state[i][j]
        blank_spaces.append(self.verify(i,j,state,"i"))
        while True:
            g,h = next
            g,h = int(g),int(h) 
            if state[g][h][0] == "e" :break   
            i,j = state[g][h]
            i,j = int(i),int(j)
            blank_spaces.append(self.verify(g,h,state,(i,j)))
            i,j = g,h
            next = state[i][j]

            
       
        
        return blank_spaces
        
    def verify(self,i,j,state,condition):
        actions = list()
        if(j+1 < self.puzzle_dimension and len(state[i][j+1]) != 2):
            if((state[i][j+1])[-3] != "n" and (state[i][j+1])[0] != "i"  and (state[i][j+1])[0] != "g"):
                actions.append((i,j,"right",condition))
        if(0 <= i-1 and len(state[i-1][j]) != 2):
            if((state[i-1][j])[-3] != "n" and (state[i-1][j])[0] != "i"  and (state[i-1][j])[0] != "g"):
                actions.append((i,j,"up",condition))
        if( 0 <= j-1 and len(state[i][j-1]) != 2):
            if((state[i][j-1])[-3] != "n" and (state[i][j-1])[0] != "i"  and (state[i][j-1])[0] != "g"):
                actions.append((i,j,"left",condition))
        if(i+1 < self.puzzle_dimension and len(state[i+1][j]) != 2):
            if((state[i+1][j])[-3] != "n" and (state[i+1][j])[0] != "i"  and (state[i+1][j])[0] != "g"):
                actions.append((i,j,"down",condition))
        return actions
    def goal_test(self, state):
        """Return  True if the state is a goal"""
        return self.isSolution(state)
    def setAlgorithm(self):
        """Sets the uninformed search algorithm chosen"""    
        self.algorithm = search.breadth_first_graph_search
        pass
    def solve(self):
        """Calls the uninformed search algorithm chosen. """
        return self.algorithm(self)



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
            if len(current) == 2:
                return i, j, "no"
            elif current[0] == prev:
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
    #for files in listdir("teste"):
        #if files[-3:] == "dat":
            #files
    with open("teste/"+"pub05.dat","r") as fh:
        #print(files)
        start_time = time.time()
        teste = RTBProblem()
        teste.setAlgorithm()
        teste.load(fh)
        print(teste.initial)
        print(teste.solve())

            #print(f"No ficheiro {files} demorou {time.time()-start_time}")


