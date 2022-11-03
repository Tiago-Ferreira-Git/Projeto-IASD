import search
import time 
from os import listdir

ACTIONS = 0

class RTBProblem(search.Problem):

    def __init__(self) -> None:
        # To save the initial state 
        self.initial = None
        # cordinates of the "start" tile
        self.start = None
        # the algoritm to be used
        self.algorithm = None
    
    def setAlgorithm(self):
        self.algorithm = search.iterative_deepening_search #depth_first_graph_search
    
    def solve(self):
        return self.algorithm(self)

    def load(self, fh):
        state = []
        for line in fh:          
            line = line.rstrip("\n")           
            if line.startswith('#'):
                continue       
            else:        
                words = line.split(" ")
                if len(words) == 1:
                    try:
                        self.puzzle_dimension = int(words[0])
                        i = self.puzzle_dimension + 2
                        for _ in range(i):
                            state.append('border')
                    except ValueError: 
                        print("Dimension not valid")
                        exit()
                else:
                    state.append('border')
                    i+=1
                    for word in words:
                        if len(word) > 7:
                            if word[:7] == "initial":
                                self.start = i           
                        i += 1                   
                    state = state + words
                    state.append('border')
                    i+=1
                    if(i == self.puzzle_dimension-1): break
        for _ in range(self.puzzle_dimension + 2):
            state.append('border')
        self.initial = tuple(state)

    def goal_test(self, state):
        # the first tile
        i = self.start
        # find where the next tile in path must be
        next = state[i][8:]
        # move search to the next tile
        while next != "goal":
            #print(i, next)
            i, next = self.check(state, i, next)
            if i == -1:
                return False
        return True

    def check(self, state, i, next):
        i = self.move(i, next)
        current = state[i].split("-")
        if len(current) == 1:
            return -1, ""
        prev = reverse(next)
        if current[0] == prev:
            return i, current[1]
        elif current[1] == prev:
            return i, current[0]
        else:
            return -1, ""

    def move(self, i, next):
        if next == "top":
            return i - (self.puzzle_dimension + 2)
        if next == "down":
            return i + (self.puzzle_dimension + 2)
        if next == "left":
            return i-1
        if next == "right":
            return i+1

    
    def actions(self, state):
        #TODO: make this a generator
        global ACTIONS
        ACTIONS += 1
        action_list = []
        i = 0
        n = self.puzzle_dimension + 2
        for i in range(n+1, n*n-n-1):
            if state[i][0] == 'e':
                if not(state[i+1][0] == 'e' or state[i+1][-3] == 'n' or state[i+1][0] == 'b' or state[i+1][0] == 'g'  or state[i+1][0] == 'i' ): 
                    action_list.append((i, "r"))
                if not(state[i-1][0] == 'e' or state[i-1][-3] == 'n' or state[i-1][0] == 'b' or state[i-1][0] == 'g'  or state[i-1][0] == 'i' ): 
                        action_list.append((i, "l"))
                if not(state[i+n][0] == 'e' or state[i+n][-3] == 'n' or state[i+n][0] == 'b' or state[i+n][0] == 'g'  or state[i+n][0] == 'i' ): 
                        action_list.append((i, "d")) 
                if not(state[i-n][0] == 'e' or state[i-n][-3] == 'n' or state[i-n][0] == 'b' or state[i-n][0] == 'g'  or state[i-n][0] == 'i' ): 
                        action_list.append((i, "t"))
        return action_list

    def result(self, state, action):
        #print(action)
        n = self.puzzle_dimension+2
        i, dir = action
        if dir == "t":
            return self.swap(state, i, i-n)
        elif dir == "d":
            return self.swap(state, i, i+n)
        elif dir == "l":
            return self.swap(state, i, i-1)
        elif dir == "r":
            return self.swap(state, i, i+1)
    
    def swap(self, state, i1, i2):
        new_state_ = list(state)
        new_state = new_state_[:]
        new_state[i1], new_state[i2] =  new_state[i2], new_state[i1]
        return tuple(new_state)

    def printb(self, state):
        i = 0
        n = self.puzzle_dimension +2
        for i in range(n):
            print(state[i*n:i*n+n])



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
                print(teste.solve())
                print(f"No ficheiro {files} demorou {time.time()-start_time}")
    print(ACTIONS)

    # rtbp = RTBProblem()
    # with open("testes/pub01.dat") as file:
    #     rtbp.load(file)
    #     rtbp.printb(rtbp.initial)
    #     #print(rtbp.goal_test(rtbp.initial))
    #     #actions = rtbp.actions(rtbp.initial)
    #     #print(actions)
    #     #for action in actions:
    #     #    print(rtbp.printb(rtbp.result(rtbp.initial, action)))
    #     rtbp.setAlgorithm()
    #     solution = rtbp.solve()
    #     print(solution)

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