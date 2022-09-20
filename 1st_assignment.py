#just opens some examples to check if parsing is done right. Change it to be type .dat and this is basically the load func. board
# will be a list of lists (list of rows and each row is a list of col)
for i in range(1,4):
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
                else:
                    board.append(word)

#funções para as classes
                    
#find initial -> find where the initial piece is. Right now is N^2, will improve later.
def find_initial(board):
    for row in board:
        for column in row:
            if "initial" in (column.split("-")):
                return(board.index(row),row.index(column))
                    
def isSolution(board:list,tupple)->bool:
    #estava a pensar fazer isto recursivo como o stor mostrou hoje na aula
    recursive(board)
    pass

print(find_initial(board))

    
    
   
   
   
   
   
#comentário
#tamanho do puzzle
#configuração do puzzle linha por linha
#N caracteres separados por um espaço
#files termina com um espaço em branco