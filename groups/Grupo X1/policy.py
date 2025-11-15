import numpy as np
from connect4.policy import Policy
from typing import List

# mejorar el contra aleatorio
class politica_epica(Policy):

    def mount(self) -> None:
        pass

    #C: cambié un poco la estructura, para no perderse
    def act(self, s: np.ndarray) -> int:
        #==Variables==
        yo= -1 #no se como sacar si soy 1 o -1 asi que por ahora soy 1
        enemigo = 1
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
                        print(HeightList)
                    else: break
            return HeightList
        # para vencer aleatorios tenemos que bloquear si van a ganar, una especie de subtrial
        # y ganar si estamos cerca, luego nos centramos en que aprenda de verdad
        def play(col: int, p: int, board: np.ndarray):
            h = get_heights(self, board)
            board[5-h[col],col] = p
        #C: Y una función para determinar si ganamos
        def check_winner(board: np.ndarray):
            for row in range(6):
                for col in range(7):
                    if col + 3 < 6 and all(board[row, col + i] == yo for i in range(4)):#hor
                        return yo 
                    if row + 3 < 6 and all(board[row + i, col] == yo for i in range(4)):# ver
                        return yo
                    if row + 3 < 6 and col + 3 < 7 and all(board[row + i, col + i] == yo for i in range(4)):# Dd
                        return yo
                    if row + 3 < 6 and col - 3 >= 0 and all(board[row + i, col - i] == yo for i in range(4)):# Da
                        return yo
            return None
        #C: Ahora la función que hace trials
        def trial(self, t:int) -> List[int]:
            win_rate=[0,0,0,0,0,0,0]
            for i in range(t):
                test_s = s.copy()
                available_cols = [c for c in range(7) if test_s[0, c] == 0]
                for col in available_cols:
                    print("Columna: ",col)
                    play(col, yo, test_s) #C: prueba jugar cada columna como primer movimiento
                    winner = None
                    tries = 0
                    while 0 in test_s and winner == None and tries<8: #C: Aqui vuelve a el comportamiento que ya tenías
                        play(rng.choice(available_cols), enemigo, test_s)
                        if check_state() != None:
                            play(check_state(), yo, test_s)
                        else:
                            play(wheighted_rng(), yo, test_s)
                        tries+=1
                        print("Intento ",tries)
                        if check_winner(test_s) == yo: #C: aqui llevamos cuenta de si ganamos con esa decisión o no
                            winner = yo
                            win_rate[col]+=1
                return win_rate
        available_cols = [c for c in range(7) if s[0, c] == 0]
        def check_state():
            for cols in available_cols:
                tab2 = s.copy()
                h= get_heights(self, board=tab2)        
                tab2[5-h[cols],cols]=yo
                for row in range(6): #cambiar el row col
                    for col in range(4):#hor
                        if (tab2[row, col] == yo and tab2[row, col+1] == yo and tab2[row, col+2] == yo and tab2[row, col+3] == yo):
                                return cols
                for r in range(3):
                    for c in range(7):#ver
                        if (tab2[r, c] == yo and tab2[r+1, c] == yo and tab2[r+2, c] == yo and tab2[r+3, c] == yo):
                                return cols
                for r in range(3):
                    for c in range(4):#diagonal
                        if (tab2[r, c] == yo and tab2[r+1, c+1] == yo and tab2[r+2, c+2] == yo and tab2[r+3, c+3] == yo):
                                return cols
                for r in range(3):
                    for c in range(3, 7):#otro diagonal
                        if (tab2[r, c] == yo and tab2[r+1, c-1] == yo and tab2[r+2, c-2] == yo and tab2[r+3, c-3] == yo):
                            return cols
                #esto no fue mi mejor idea, si se les ocurre algo mejor porfa cambienlo
            for cols in available_cols:
                tab2 = s.copy()
                h= get_heights(self, board=tab2)        
                tab2[5-h[cols],cols]=enemigo
                for row in range(6): #cambiar el row col
                    for col in range(4):#hor
                        if (tab2[row, col] == enemigo and tab2[row, col+1] == enemigo and tab2[row, col+2] == enemigo and tab2[row, col+3] == enemigo):
                                return cols
                for r in range(3):
                    for c in range(7):#ver
                        if (tab2[r, c] == enemigo and tab2[r+1, c] == enemigo and tab2[r+2, c] == enemigo and tab2[r+3, c] == enemigo):
                                return cols
                for r in range(3):
                    for c in range(4):#diagonal
                        if (tab2[r, c] == enemigo and tab2[r+1, c+1] == enemigo and tab2[r+2, c+2] == enemigo and tab2[r+3, c+3] == enemigo):                              return cols
                for r in range(3):
                    for c in range(3, 7):#otro diagonal
                        if (tab2[r, c] == enemigo and tab2[r+1, c-1] == enemigo and tab2[r+2, c-2] == enemigo and tab2[r+3, c-3] == enemigo):
                                return cols
                #Reitero, porfa si tienen una mejor idea cambienlo, esta horrible esto
                return None
        
        ver = int(1) #para cambiar entre el basico y el MCTS cuando lo tenga
        if(check_state() != None): #C: Cambie el if para no tener que redundar tanto, y dejé lo que habia antes
            return check_state()
        else:
            if ver==0:
                return wheighted_rng()
            else:
                #C: La idea es que hace un numero de trials, y luego elige la opción que mejor resultado dió, la cosa es que solo hace eso jaja
                test_restults = trial(self, t=10)
                if all(prob == 0 for prob in test_restults): #C: si no encotró una opcion mejor, elige una al azar
                    return wheighted_rng()
                else:
                    return test_restults.index(max(test_restults))
        
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
