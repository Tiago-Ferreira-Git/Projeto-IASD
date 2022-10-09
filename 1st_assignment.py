#just opens some examples to check if parsing is done right. Change it to be type .dat and this is basically the load func. board
# will be a list of lists (list of rows and each row is a list of col)
from os import listdir


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
    board = None
    initial_index = None
    def __init__(self) -> None:
        pass

    def load(self, fh):
        """Just opens some examples to check if parsing is done right. 
        Change it to be type .dat and this is basically the load func. 
        board will be a list of lists (list of rows and each row is a list of col)"""
        board = list()
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith('#'):
                continue
            else:
                words = line.split(" ")
                if len(words) == 1:
                    try:
                        puzzle_dimension = int(words[0])
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
        i,j = self.initial_index
        # find where the next tile in path must be
        next = self.board[i][j].split("-")
        next = next[1]
        # move search to the next tile
        while next != "no" and next != "goal":
            i, j, next = self.check(i, j, next)
            #print(i, j)
        if next == "no":
            return False
        elif next == "goal":
            return True
        else:
            print("tenso, algo deu merda")
            exit()

    def check(self, i, j, next):
        i, j = move(i, j, next)
        current = self.board[i][j].split("-")
        prev = reverse(next)
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


if __name__ == "__main__":
    
    for files in listdir():
        if files[-3:] == "dat":
            with open("pub08.dat","r") as fh:
                rtbp = RTBProblem()
                rtbp.load(fh)
                #rtbp.isSolution()
                #rtbp.printb()
                #print(files)
                print(rtbp.isSolution())


   
   
