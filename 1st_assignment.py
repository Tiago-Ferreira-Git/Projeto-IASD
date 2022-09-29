#just opens some examples to check if parsing is done right. Change it to be type .dat and this is basically the load func. board
# will be a list of lists (list of rows and each row is a list of col)



def get_board():
    """Just opens some examples to check if parsing is done right. 
        Change it to be type .dat and this is basically the load func. 
        board will be a list of lists (list of rows and each row is a list of col)"""

    for i in range(3,4):
        with open("exemplo{}.txt".format(i),"r") as file:
            board = list()
            for line in file:
                line = line.rstrip("\n")
                if line.startswith('#'):
                    continue
                else:
                    word = line.split(" ")
                    if len(word) == 1:
                        try:
                            puzzle_dimension = int(word[0])
                        except ValueError: 
                            print("Dimension not valid")
                            exit()
                    else:
                        board.append(word)
    return(board)


class RTBProblem():

    def __init__(self) -> None:
        pass

    def load(self, fh):
        """Just opens some examples to check if parsing is done right. 
        Change it to be type .dat and this is basically the load func. 
        board will be a list of lists (list of rows and each row is a list of col)"""

        for i in range(1,2):
            with open("exemplo{}.txt".format(i),"r") as file:
                board = list()
                for line in file:
                    line = line.rstrip("\n")
                    if line.startswith('#'):
                        continue
                    else:
                        word = line.split(" ")
                        if len(word) == 1:
                            try:
                                puzzle_dimension = int(word[0])
                            except ValueError: 
                                print("Dimension not valid")
                                exit()
                        else:
                            board.append(word)
        self.board = [['right-down', 'right-left', 'right-left', 'initial-left'], ['right-top', 'right-left', 'right-left', 'left-down'], ['goal-right', 'right-left', 'right-left', 'left-top'], ['empty-cell', 'empty-cell', 'right-left', 'empty-cell']]

    def printb(self):
        print(self.board)    

    def find_initial(self):
        """find initial -> find where the initial piece is. 
            Right now is N^2, will improve later."""

        for row in self.board:
            for column in row:
                if "initial" in (column.split("-")):
                    return(self.board.index(row), row.index(column))
        
    def isSolution(self):
        # find the initial tile
        i,j = self.find_initial()
        print(i, j)
        # find where the next tile in path must be
        next = self.board[i][j].split("-")
        next = next[1]
        # move search to the next tile
        while next != "no" and next != "goal":
            i, j, next = self.check(i, j, next)
            print(i, j)
        if next == "no":
            return 0
        elif next == "goal":
            return 1
        else:
            print("tenso, algo deu merda")
            exit()

    def check(self, i, j, next):
        i, j = move(i, j, next)
        current = self.board[i][j].split("-")
        prev = reverse(next)
        print(prev)
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


if __name__ == "__main__":
    rtbp = RTBProblem()
    rtbp.load("exemplo3.txt")
    rtbp.printb()
    print(rtbp.isSolution())
    

   
   
#comentário
#tamanho do puzzle
#configuração do puzzle linha por linha
#N caracteres separados por um espaço
#files termina com um espaço em branco