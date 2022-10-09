import search


class RTBProblem(search.Problem):
    puzzle_dimension = None
    initial = None
    algorithm = None
    initial_index = None
    def __init__(self) -> None:
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
                         
                        
                        j += 1
                    
                    board.append(words)
                    i += 1
        self.initial = board
     
        

    def Printb(self):
        print(self.board) 
    
    
    
    def result(self, state,action):
        """Return  the state that results from executing the given action"""   
        pass
    def actions(self, state):
        """Return the state that can be executed in the given state"""

        pass
    def goal_test(self, state):
        """Return  True if the state is a goal"""
        return self.isSolution(state)
    def setAlgorithm(self):
        """Sets the uninformed search algorithm chosen"""    
        self.algorithm = search.breadth_first_graph_search() 
        pass
    def solve(self):
        """Calls the uninformed search algorithm chosen. """
        return self.algorithm(self)





    def isSolution(self,state):
        # find the initial tile
        i,j = self.initial_index
        # find where the next tile in path must be
        next = state[i][j].split("-")
        next = next[1]
        # move search to the next tile
        while next != "no" and next != "goal":
            i, j, next = self.check(i, j, next,state)
            #print(i, j)
        if next == "no":
            return False
        elif next == "goal":
            return True
        else:
            exit()

    def check(self, i, j, next,state):
        i, j = self.move(i, j, next)
        current = state.split("-")
        prev = self.reverse(next)
        #print(prev)
        if current[0] == prev:
            next = current[1]
        elif current[1] == prev:
            next = current[0]
        else:
            return i, j, "no"
        return i, j, next

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