import search
import time 
from os import listdir

class RTBProblem(search.Problem):

    def __init__(self) -> None:
        # To save the initial state 
        self.initial = None
        # cordinates of the "start" tile
        self.start = None
        # the algoritm to be used
        self.algorithm = None
    
    def setAlgorithm(self):
        self.algorithm = search.breadth_first_graph_search
    
    def solve(self):
        return self.algorithm(self)

    def load(self, fh):
        state = []
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
                            blanks = blanks + [i, j]               
                        j += 1
                    
                    state = state + words
                    if(i == self.puzzle_dimension-1): break
                    i += 1
        state = state + blanks
        state = tuple(state)
        self.initial = state

    def translate(self, coord):
        return(coord[0]*self.puzzle_dimension + coord[1])

    def goal_test(self, state):
        # the first tile
        i, j = self.start[0], self.start[1]
        # find where the next tile in path must be
        next = state[self.translate((i,j))][8:]
        # move search to the next tile
        while next != "no" and next != "goal":
            i, j, next = self.check(state, i, j, next)
        if next == "no":
            return False
        elif next == "goal":
            return True
        else:
            print("tenso, algo deu merda")
            exit()

    def check(self, state, i, j, next):
        i, j = move(i, j, next)
        if i < 0 or j < 0 or i > self.puzzle_dimension-1 or j > self.puzzle_dimension-1:
            return i, j, "no"
        current = state[self.translate((i,j))].split("-")
        prev = reverse(next)
        if current[0] == prev:
            next = current[1]
        elif current[1] == prev:
            next = current[0]
        else:
            return i, j, "no"
        return i, j, next
    
    def actions(self, state):

        #TODO: make this a generator
        action_list = []
        blanks = state[self.puzzle_dimension**2:]
        n_blanks = int(len(blanks)/2)
        for b in range(n_blanks):
            # get coordinates of the "empty-cell" 
            i, j = blanks[b*2], blanks[b*2+1]
            if self.is_moveable(state, i, j+1):
                action_list.append((i,j,"right"))
            if self.is_moveable(state, i, j-1):
                action_list.append((i,j,"left"))
            if self.is_moveable(state, i+1, j):
                action_list.append((i,j,"down"))
            if self.is_moveable(state, i-1, j):
                action_list.append((i,j,"up"))
            
            

        return action_list

    def is_moveable(self, state, i,j):
        if i < 0 or j < 0 or i > self.puzzle_dimension-1 or j > self.puzzle_dimension-1:
            return False
        tile = state[self.translate((i,j))].split("-")
        if tile[0] == "initial" or tile[0] == "goal" or tile[-1] == "not" or tile[0] == "empty":
            return False
        else:
            return True


    def result(self, state, action):
        #print(action)
        i, j, dir = action
        if dir == "up":
            new_state = self.swap(state, (i, j), (i-1, j))
        elif dir == "down":
            new_state = self.swap(state, (i, j), (i+1, j))
        elif dir == "left":
            new_state = self.swap(state, (i, j), (i, j-1))
        elif dir == "right":
            new_state = self.swap(state, (i, j), (i, j+1))
            
        #print(new_state)
        return new_state
    
    def swap(self, state, first, second):
        new_state = list(state)
        blanks = new_state[self.puzzle_dimension**2:]
        new_state = new_state[:self.puzzle_dimension**2]
        new_state[self.translate(first)], new_state[self.translate(second)] =  new_state[self.translate(second)], new_state[self.translate(first)]
        
        n_blanks = int(len(blanks)/2)
        for b in range(n_blanks):
            # get coordinates of the "empty-cell" 
            if (blanks[b*2], blanks[b*2+1]) == first:
                blanks[b*2], blanks[b*2+1] = second[0], second[1]
        new_state = new_state + blanks    
        return tuple(new_state)



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

    for files in listdir("testes"):
        if files[-3:] == "dat":
            with open("testes/"+files,"r") as fh:
                #print(files)
                start_time = time.time()
                teste = RTBProblem()
                teste.setAlgorithm()
                teste.load(fh)
                teste.solve()
                print(f"No ficheiro {files} demorou {time.time()-start_time}")

    #rtbp = RTBProblem()
    # with open("testes/pub04.dat") as file:
    #     rtbp.load(file)
    #     # actions = rtbp.actions(rtbp.initial)
    #     # for action in actions:
    #     #     rtbp.result(rtbp.initial, action)
    #     rtbp.setAlgorithm()
    #     solution = rtbp.solve()
    #     print(solution.)

    # problem = RTBProblem()
    # t0 = time.process_time()
    # with open("testes/pub04.dat") as fh:
    #     problem.load(fh)
    # problem.setAlgorithm()
    # result = problem.solve()
    # t1 = time.process_time()

   
   
#comentário
#tamanho do puzzle
#configuração do puzzle linha por linha
#N caracteres separados por um espaço
#files termina com um espaço em branco