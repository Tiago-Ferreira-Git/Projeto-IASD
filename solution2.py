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
                    for word in words:
                        if len(word) > 7:
                            if word[:7] == "initial":
                                self.start = i           
                        i += 1                   
                    state = state + words
                    if(i == self.puzzle_dimension-1): break

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
        if i == -1:
            return -1, ""
        current = state[i].split("-")
        #print(current)
        prev = reverse(next)
        if current[0] == prev:
            return i, current[1]
        elif current[1] == prev:
            return i, current[0]
        else:
            return -1, ""

    
    def move(self, i, next):
        n = self.puzzle_dimension
        n2 = n**2
        r = i%n 
        if i == 0:
            if next == "top":
                return -1
            elif next == "down":
                return i+n
            elif next == "left":
                return -1
            elif next == "right":
                return i+1
            else:
                return -1
        # cell is in top-right corner
        elif i == n-1:
            if next == "top":
                return -1
            elif next == "down":
                return i+n
            elif next == "left":
                return i-1
            elif next == "right":
                return -1
            else:
                return -1
        # cell is in down-left corner
        elif i == n2-n:
            if next == "top":
                return i-n
            elif next == "down":
                return -1
            elif next == "left":
                return -1
            elif next == "right":
                return i+1
            else:
                return -1
        # cell is in down-right corner
        elif i == n2-1:
            if next == "top":
                return i-n
            elif next == "down":
                return -1
            elif next == "left":
                return i-1
            elif next == "right":
                return -1
            else:
                return -1
        # cell is in top row (not corners)
        elif i < n:
            if next == "top":
                return -1
            elif next == "down":
                return i+n
            elif next == "left":
                return i-1
            elif next == "right":
                return i+1
            else:
                return -1
        # cell is in bottom row (not corners)
        elif i >= n2-n:
            if next == "top":
                return i-n
            elif next == "down":
                return -1
            elif next == "left":
                return i-1
            elif next == "right":
                return i+1
            else:
                return -1
        # cell is in left row (not corners)
        elif r == 0:
            if next == "top":
                return i+1
            elif next == "down":
                return i+n
            elif next == "left":
                return -1
            elif next == "right":
                return i+1
            else:
                return -1
        # cell is in right row (not corners)
        elif r == n-1:
            if next == "top":
                return i+1
            elif next == "down":
                return i+n
            elif next == "left":
                return i-1
            elif next == "right":
                return -1
            else:
                return -1
        # cell is in the middle
        else:
            if next == "top":
                return i-n
            elif next == "down":
                return i+n
            elif next == "left":
                return i-1
            elif next == "right":
                return i+1
            else:
                return -1

    
    def actions(self, state):
        """
        1 -> "up"
        2 -> "down"
        3 -> "left"
        4 -> "right"
        """
        #TODO: make this a generator
        action_list = []
        i = 0
        n = self.puzzle_dimension
        n2 = n**2
        for cell in state:
            if cell[0] == 'e':
                r = i%n
                # cell is in top-left corner
                if i == 0:
                    if state[i+1][0] != 'e' and state[i+1][0] != 'g' and state[i+1][-3] != 'n' and state[i+1][0] != 'i': 
                        action_list.append((i, "r"))  
                    if state[i+n][0] != 'e' and state[i+n][0] != 'g' and state[i+n][-3] != 'n' and state[i+n][0] != 'i': 
                        action_list.append((i, "d"))
                # cell is in top-right corner
                elif i == n-1:
                    if state[i-1][0] != 'e' and state[i-1][0] != 'g' and state[i-1][-3] != 'n' and state[i-1][0] != 'i': 
                        action_list.append((i, "l"))
                    if state[i+n][0] != 'e' and state[i+n][0] != 'g' and state[i+n][-3] != 'n' and state[i+n][0] != 'i': 
                        action_list.append((i, "d"))
                # cell is in down-left corner
                elif i == n2-n:
                    if state[i+1][0] != 'e' and state[i+1][0] != 'g' and state[i+1][-3] != 'n' and state[i+1][0] != 'i': 
                        action_list.append((i, "r"))
                    if state[i-n][0] != 'e' and state[i-n][0] != 'g' and state[i-n][-3] != 'n' and state[i-n][0] != 'i': 
                        action_list.append((i, "u"))
                # cell is in down-right corner
                elif i == n2-1:
                    if state[i-1][0] != 'e' and state[i-1][0] != 'g' and state[i-1][-3] != 'n' and state[i-1][0] != 'i': 
                        action_list.append((i, "l"))
                    if state[i-n][0] != 'e' and state[i-n][0] != 'g' and state[i-n][-3] != 'n' and state[i-n][0] != 'i': 
                        action_list.append((i, "u"))
                # cell is in top row (not corners)
                elif i < n:
                    if state[i+1][0] != 'e' and state[i+1][0] != 'g' and state[i+1][-3] != 'n' and state[i+1][0] != 'i': 
                        action_list.append((i, "r"))
                    if state[i-1][0] != 'e' and state[i-1][0] != 'g' and state[i-1][-3] != 'n' and state[i-1][0] != 'i': 
                        action_list.append((i, "l"))
                    if state[i+n][0] != 'e' and state[i+n][0] != 'g' and state[i+n][-3] != 'n' and state[i+n][0] != 'i': 
                        action_list.append((i, "d"))
                # cell is in bottom row (not corners)
                elif i >= n2-n:
                    if state[i+1][0] != 'e' and state[i+1][0] != 'g' and state[i+1][-3] != 'n' and state[i+1][0] != 'i': 
                        action_list.append((i, "r"))
                    if state[i-1][0] != 'e' and state[i-1][0] != 'g' and state[i-1][-3] != 'n' and state[i-1][0] != 'i': 
                        action_list.append((i, "l"))
                    if state[i-n][0] != 'e' and state[i-n][0] != 'g' and state[i-n][-3] != 'n' and state[i-n][0] != 'i': 
                        action_list.append((i, "u"))
                # cell is in left row (not corners)
                elif r == 0:
                    if state[i+1][0] != 'e' and state[i+1][0] != 'g' and state[i+1][-3] != 'n' and state[i+1][0] != 'i': 
                        action_list.append((i, "r"))
                    if state[i+n][0] != 'e' and state[i+n][0] != 'g' and state[i+n][-3] != 'n' and state[i+n][0] != 'i': 
                        action_list.append((i, "d"))
                    if state[i-n][0] != 'e' and state[i-n][0] != 'g' and state[i-n][-3] != 'n' and state[i-n][0] != 'i': 
                        action_list.append((i, "u"))
                    
                    
                # cell is in right row (not corners)
                elif r == n-1:
                    if state[i-1][0] != 'e' and state[i-1][0] != 'g' and state[i-1][-3] != 'n' and state[i-1][0] != 'i': 
                        action_list.append((i, "l"))
                    if state[i+n][0] != 'e' and state[i+n][0] != 'g' and state[i+n][-3] != 'n' and state[i+n][0] != 'i': 
                        action_list.append((i, "d"))
                    if state[i-n][0] != 'e' and state[i-n][0] != 'g' and state[i-n][-3] != 'n' and state[i-n][0] != 'i': 
                        action_list.append((i, "u"))
                # cell is in the middle
                else:
                    if state[i+1][0] != 'e' and state[i+1][0] != 'g' and state[i+1][-3] != 'n' and state[i+1][0] != 'i': 
                        action_list.append((i, "r"))
                    if state[i-1][0] != 'e' and state[i-1][0] != 'g' and state[i-1][-3] != 'n' and state[i-1][0] != 'i': 
                        action_list.append((i, "l"))
                    if state[i+n][0] != 'e' and state[i+n][0] != 'g' and state[i+n][-3] != 'n' and state[i+n][0] != 'i': 
                        action_list.append((i, "d"))
                    if state[i-n][0] != 'e' and state[i-n][0] != 'g' and state[i-n][-3] != 'n' and state[i-n][0] != 'i': 
                        action_list.append((i, "u"))
            i+=1
        return action_list

    def result(self, state, action):
        #print(action)
        n = self.puzzle_dimension
        i, dir = action
        if dir == "u":
            new_state = self.swap(state, i, i-n)
        elif dir == "d":
            new_state = self.swap(state, i, i+n)
        elif dir == "l":
            new_state = self.swap(state, i, i-1)
        elif dir == "r":
            new_state = self.swap(state, i, i+1)
            
        #print(new_state)
        return new_state
    
    def swap(self, state, i1, i2):
        new_state_ = list(state)
        new_state = new_state_[:]
        new_state[i1], new_state[i2] =  new_state[i2], new_state[i1]
        return tuple(new_state)





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

    # for files in listdir("testes"):
    #     if files[-3:] == "dat":
    #         with open("testes/"+files,"r") as fh:
    #             #print(files)
    #             start_time = time.time()
    #             teste = RTBProblem()
    #             teste.setAlgorithm()
    #             teste.load(fh)
    #             teste.solve()
    #             print(f"No ficheiro {files} demorou {time.time()-start_time}")

    rtbp = RTBProblem()
    with open("testes/pub07.dat") as file:
        rtbp.load(file)
        # print(rtbp.initial)
        # print(rtbp.goal_test(rtbp.initial))
        # actions = rtbp.actions(rtbp.initial)
        # print(actions)
        # for action in actions:
        #     print(rtbp.result(rtbp.initial, action))
        rtbp.setAlgorithm()
        solution = rtbp.solve()
        print(solution)

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