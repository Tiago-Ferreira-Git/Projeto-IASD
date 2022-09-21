
#funções para as classes
                    
#find_initial -> find where the initial piece is. Right now is N^2, will improve later.
def find_initial(board):
    for row in board:
        for column in row:
            if "initial" in (column.split("-")):
                return(board.index(row),row.index(column))
    
                    
def isSolution(board:list,tupple)->bool:
    #estava a pensar fazer isto recursivo como o stor mostrou hoje na aula
    recursive(board,tupple)
    pass


    
def recursive(board,position,last_position,flow):
    x,y = position
    word = (board[x][y].split("-"))
    
    if  puzzle_dimension -1 < x or  x <0 or  y<0 or y>puzzle_dimension -1 :      
        return False
    if "initial" in word:
        if word[1] == "left":
            return recursive(board,(x,y-1),["right","left"],"left")
        elif word[1] == "right":
            return recursive(board,(x,y+1),["right","left"],"right")
        elif word[1] == "down":
            return recursive(board,(x-1,y),["top","down"],"down")
        elif word[1] == "top":
            return recursive(board,(x+1,y),["top","down"],"top")
    if flow == "left":
        if "right" in word and not "goal" in word:
            if "down" in word:
                return recursive(board,(x+1,y),word,"down")
            elif "left" in word:
                return recursive(board,(x,y-1),word,"left")
            elif "top" in word:
                return recursive(board,(x-1,y),word,"top")
        elif "right" in word and "goal" in word:
            return True
        else:
            return False
    elif flow == "right":
        if "left" in word:
            if "down" in word:
                return recursive(board,(x+1,y),word,"down")
            elif "right" in word:
                return recursive(board,(x,y+1),word,"right")
            elif "top" in word:
                return recursive(board,(x-1,y),word,"top")
        elif "left" in word and "goal" in word:
            return True
        else:
            return False
    elif flow == "down":
        if "top" == word[1] and not "goal" in word:
            if "right" in word:
                return recursive(board,(x,y+1),word,"right")
            elif "left" in word:
                return recursive(board,(x,y-1),word,"left")
        elif "down" == word[1] and not "goal" in word:
            return recursive(board,(x+1,y),word,"down")
        elif "top" in word and "goal" in word:
            return True
        else:
            return False
    elif flow == "top":
        if "top" == word[1] and not "goal" in word:
            if "right" in word:
                return recursive(board,(x,y+1),word,"right")
            elif "left" in word :
                return recursive(board,(x,y-1),word,"left")
        elif "down" == word[1] and not "goal" in word:
            return recursive(board,(x-1,y),word,"top")
        elif "down" in word and "goal" in word:
            return True
        else:
            return False
    
        
    return True


#just opens some examples to check if parsing is done right. Change it to be type .dat and this is basically the load func. board
# will be a list of lists (list of rows and each row is a list of col)
for i in range(1,4):
    with open("exemplo{}.txt".format(i),"r") as file:
        board = list()
        for line in file:
            line = line.rstrip("\n")
            if line.startswith('#'):
                #comments
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

        print(recursive(board,find_initial(board),None,""))


#A. {“initial-left”, “initial-right”, “initial-top”, “initial-down”}
#B. {“goal-left”, “goal-right”, “goal-top”, “goal-down”}
#C. {“right-left-not”, “top-down-not”, “right-top-not”,“right-down-not”, “left-top-not”, “left-down-not”, “no-passage-not”}
#D. {“right-left”, “top-down”, “right-top”, “right-down”, “left-top”, “left-down”, “no-passage”}
#E. {“empty-cell”}

#comentário
#tamanho do puzzle
#configuração do puzzle linha por linha
#N caracteres separados por um espaço
#files termina com um espaço em branco