import numpy as np
from connect4.policy import Policy
from typing import List

# mejorar el contra aleatorio
class politica_epica(Policy):

    def mount(self) -> None:
        pass

    #C: cambié un poco la estructura, para no perderse
    def act(self, s: np.ndarray) -> int:
        # Determinar si yo soy -1 o 1
        def get_current_player(board):
            c_neg = np.count_nonzero(board == -1)
            c_pos = np.count_nonzero(board == 1)
            return -1 if c_neg == c_pos else 1

        yo = get_current_player(s)
        enemigo = -yo

        rng = np.random.default_rng()

        #==Funciones==
        def wheighted_rng():
            if(get_heights(self, board=s)[2]<=5): #si no hay piezas colocadas coloca en espacio 3 para tener el medio
                    return 2
            elif(get_heights(self, board=s)[3]<=5):
                    return 3
            return rng.choice(available_cols)
        def get_heights(self, board: np.ndarray) -> List[int]:# lo saque de clase 1
            HeightList=[0,0,0,0,0,0,0]
            for col in range(7):
                for row in reversed(range(6)):
                    if board[row,col] != 0:
                        HeightList[col] += 1
                    else: break
            return HeightList
        # para vencer aleatorios tenemos que bloquear si van a ganar, una especie de subtrial
        # y ganar si estamos cerca, luego nos centramos en que aprenda de verdad
        def play(col: int, p: int, board: np.ndarray):
            h = get_heights(self, board)
            board[5-h[col],col] = p
        #C: Y una función para determinar si ganamos
        def check_winner(board: np.ndarray, p: int) -> bool:
            for row in range(6):
                for col in range(7):
                    if col + 3 < 6 and all(board[row, col + i] == p for i in range(4)):#hor
                        return True
                    if row + 3 < 6 and all(board[row + i, col] == p for i in range(4)):# ver
                        return True
                    if row + 3 < 6 and col + 3 < 7 and all(board[row + i, col + i] == p for i in range(4)):# Dd
                        return True
                    if row + 3 < 6 and col - 3 >= 0 and all(board[row + i, col - i] == p for i in range(4)):# Da
                        return True
            return False
        #C: Ahora la función que hace trials
        def trial(self, t:int) -> List[int]:
            win_rate={0:0,1:0,2:0,3:0,4:0,5:0,6:0}
            for i in range(t):
                test_s = s.copy()
                available_cols = [c for c in range(7) if test_s[0, c] == 0]
                for col in available_cols:
                    #print("Columna: ",col)
                    play(col, yo, test_s) #C: prueba jugar cada columna como primer movimiento
                    winner = None
                    tries = 0
                    while 0 in test_s and winner == None and tries<8: #C: Aqui vuelve a el comportamiento que ya tenías
                        if check_state(enemigo, yo) != None:
                            play(check_state(enemigo, yo), enemigo, test_s)
                        else:
                            play(rng.choice(available_cols), enemigo, test_s)
                        
                        if check_state(yo, enemigo) != None:
                            play(check_state(yo, enemigo), yo, test_s)
                        else:
                            play(wheighted_rng(), yo, test_s)
                        tries+=1
                        #print("Intento ",tries)
                        if check_winner(test_s, yo): #C: aqui llevamos cuenta de si ganamos con esa decisión o no
                            winner = yo
                            win_rate[col]+=1
                        elif check_winner(test_s, enemigo):
                            winner = enemigo
                            win_rate[col]-=1
            filtered_win_rate = {}
            for col in available_cols:
                filtered_win_rate[col] = win_rate[col]
            return filtered_win_rate
        available_cols = [c for c in range(7) if s[0, c] == 0]
        def check_state(p: int, e: int):
            for cols in available_cols:
                tab2 = s.copy()
                h= get_heights(self, tab2)        
                tab2[5-h[cols],cols]=p
                for row in range(6): #cambiar el row col
                    for col in range(4):#hor
                        if (tab2[row, col] == p and tab2[row, col+1] == p and tab2[row, col+2] == p and tab2[row, col+3] == p):
                            return cols
                for r in range(3):
                    for c in range(7):#ver
                        if (tab2[r, c] == p and tab2[r+1, c] == p and tab2[r+2, c] == p and tab2[r+3, c] == p):
                            return cols
                for r in range(3):
                    for c in range(4):#diagonal
                        if (tab2[r, c] == p and tab2[r+1, c+1] == p and tab2[r+2, c+2] == p and tab2[r+3, c+3] == p):
                            return cols
                for r in range(3):
                    for c in range(3, 7):#otro diagonal
                        if (tab2[r, c] == p and tab2[r+1, c-1] == p and tab2[r+2, c-2] == p and tab2[r+3, c-3] == p):
                            return cols
                #esto no fue mi mejor idea, si se les ocurre algo mejor porfa cambienlo
            for cols in available_cols:
                tab2 = s.copy()
                h= get_heights(self, tab2)        
                tab2[5-h[cols],cols]=e
                for row in range(6): #cambiar el row col
                    for col in range(4):#hor
                        if (tab2[row, col] == e and tab2[row, col+1] == e and tab2[row, col+2] == e and tab2[row, col+3] == enemigo):
                                #print("check")
                                return cols
                for r in range(3):
                    for c in range(7):#ver
                        if (tab2[r, c] == e and tab2[r+1, c] == e and tab2[r+2, c] == e and tab2[r+3, c] == e):
                                #print("check")
                                return cols
                for r in range(3):
                    for c in range(4):#diagonal
                        if (tab2[r, c] == e and tab2[r+1, c+1] == e and tab2[r+2, c+2] == e and tab2[r+3, c+3] == e):
                            #print("check") 
                            return cols
                for r in range(3):
                    for c in range(3, 7):#otro diagonal
                        if (tab2[r, c] == e and tab2[r+1, c-1] == e and tab2[r+2, c-2] == e and tab2[r+3, c-3] == e):
                                #print("check")
                                return cols
                #Reitero, porfa si tienen una mejor idea cambienlo, esta horrible esto
            return None
        print(s)
        ver = int(1) #para cambiar entre el basico y el MCTS cuando lo tenga
        if check_state(yo, enemigo) != None: #C: Cambie el if para no tener que redundar tanto, y dejé lo que habia antes
            print(check_state(yo, enemigo))
            return check_state(yo, enemigo)
        else:
            if ver==0:
                return wheighted_rng()
            else:
                #C: La idea es que hace un numero de trials, y luego elige la opción que mejor resultado dió, la cosa es que solo hace eso jaja
                test_restults = trial(self, t=10)
                if all(prob == 0 for prob in test_restults): #C: si no encotró una opcion mejor, elige una al azar
                    return wheighted_rng()
                else:
                    print ("Test results: ",test_restults)
                    print ("Selected Action: ", list(test_restults.keys())[list(test_restults.values()).index(max(list(test_restults.values())))])
                    return list(test_restults.keys())[list(test_restults.values()).index(max(list(test_restults.values())))]
        
        # for row in range(6): # codigo de clase 1 detector de ganar, del cual me inspire
        #     for col in range(7):
        #         player = board[row, col]
        #         if player == 0:
        #             continue
        #         if col + 3 < 6 and all(board[row, col + i] == player for i in range(4)):#hor
        #             return player 
        #         if row + 3 < 6 and all(board[row + i, col] == player for i in range(4)):# ver
        #             return player 
        #         if row + 3 < 6 and col + 3 < 7 and all(board[row + i, col + i] == player for i in range(4)):# Dd
        #             return player 
        #         if row + 3 < 6 and col - 3 >= 0 and all(board[row + i, col - i] == player for i in range(4)):# Da
        #             return player
            #C: pondré una función de prueba para hacer jugadas (osea para jugar en el tablero imaginario)
