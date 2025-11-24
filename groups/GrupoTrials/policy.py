import numpy as np
from connect4.policy import Policy
from typing import List

class politica_rara(Policy):

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
        def wheighted_rng(board):
            legal = get_available_cols(board)
            if not legal:
                return None
            for preferred in [2, 3]:
                if preferred in legal:
                    return preferred
            chosen = rng.choice(legal)
            return chosen
        def get_heights(board: np.ndarray) -> List[int]:# lo saque de clase 1
            HeightList=[0,0,0,0,0,0,0]
            for col in range(7):
                for row in range(6):
                    if board[row,col] != 0:
                        HeightList[col] += 1

            return HeightList
        # para vencer aleatorios tenemos que bloquear si van a ganar, una especie de subtrial
        # y ganar si estamos cerca, luego nos centramos en que aprenda de verdad
        def play(col: int, p: int, board: np.ndarray):
            row = get_heights(board)[col]
            if row >= 6:
                raise ValueError(f"Column {col} is full!")
            board[5-row, col] = p
        #C: Y una función para determinar si ganamos
        def check_winner(board: np.ndarray, p: int) -> bool:
            for row in range(6):
                for col in range(7):
                    if col + 3 < 7 and all(board[row, col + i] == p for i in range(4)):#hor
                        return True
                    if row + 3 < 6 and all(board[row + i, col] == p for i in range(4)):# ver
                        return True
                    if row + 3 < 6 and col + 3 < 7 and all(board[row + i, col + i] == p for i in range(4)):# Dd
                        return True
                    if row + 3 < 6 and col - 3 >= 0 and all(board[row + i, col - i] == p for i in range(4)):# Da
                        return True
            return False
        #C: Ahora la función que hace trials
        def trial(t:int) -> dict:
            win_rate={0:0,1:0,2:0,3:0,4:0,5:0,6:0}
            for i in range(t):
                test_s = s.copy()
                for col in  get_available_cols(test_s) :
                    #print("Columna: ",col)
                    temp_board= test_s.copy()
                    play(col, yo, temp_board) #C: prueba jugar cada columna como primer movimiento
                    winner = None
                    tries = 0
                    while 0 in temp_board and winner is None: #C: Aqui vuelve a el comportamiento que ya tenías
                        legal= get_available_cols(temp_board)

                        col_enemy = check_state(enemigo,yo, temp_board)
                        if col_enemy is not None and col_enemy in legal:
                            play(col_enemy,enemigo,temp_board)
                        elif legal:
                            play(rng.choice(legal),enemigo,temp_board)

                        legal=get_available_cols(temp_board)
                        col_me= check_state(yo, enemigo,temp_board)
                        if col_me is not None and col_me in legal:
                            play(col_me, yo, temp_board)
                        elif legal:
                            play(wheighted_rng(temp_board),yo, temp_board)

                        if check_winner(temp_board, yo): #C: aqui llevamos cuenta de si ganamos con esa decisión o no
                            winner = yo
                            win_rate[col]+=1
                        elif check_winner(temp_board, enemigo):
                            winner = enemigo
                            win_rate[col]-=1


            filtered_win_rate = {c: win_rate[c] for c in range(7) if s[0, c] == 0}
            return filtered_win_rate
        def get_available_cols(board):
            return [c for c in range(7) if get_next_row(c, board) is not None]
        def get_next_row(col,board):
            heights = get_heights(board)
            if heights[col] >= 6:
                return None  # columna llena
            return 5 - heights[col]

        def check_state(p: int, e: int, board: np.ndarray):
            def find3plus1(jugador,board):
                #horizontal
                for r in range(0,6):
                    for c in range(0,4):
                        secuencia= board[r,c:c+4]
                        if list(secuencia).count(jugador) ==3 and list(secuencia).count(0)==1:
                            hueco=list(secuencia).index(0)
                            columna = c+hueco
                            if columna in get_available_cols(board) and get_next_row(columna,board) == r :
                                return columna
                #verticla
                for c in range(0,7):
                    for r in range(0,3):
                        secuencia= [board[r+i,c]for i in range(4)]
                        if secuencia.count(jugador) ==3 and secuencia.count(0)==1:
                            hueco = secuencia.index(0)
                            fila=r +hueco
                            fila_real = get_next_row(c,board)

                            if  fila_real is not None and fila_real == fila :
                                return c
                #diagonal derecha
                for r in range(0,3):
                    for c in range(0,4):
                        secuencia= [board[r+i,c+i] for i in range(4)]
                        if secuencia.count(jugador) == 3 and secuencia.count(0)==1:
                            hueco = secuencia.index(0)
                            columna = c +hueco
                            fila= r + hueco
                            if  columna in get_available_cols(board) and get_next_row(columna,board) == fila :
                                return columna
                #daigonal izquierda
                for r in range(0,3):
                    for c in range(3,7):
                        secuencia=[board[r+i,c-i] for i in range(4)]
                        if secuencia.count(jugador)==3 and secuencia.count(0)==1:
                            hueco= secuencia.index(0)
                            columna = c -hueco
                            fila = r +hueco
                            if columna in get_available_cols(board) and get_next_row(columna,board) == fila :
                                return columna
                return None
            #ganar
            col = find3plus1(p,board)
            legal = get_available_cols(board)
            if col is not None and col in legal:
                return col
            #bloquear
            col = find3plus1(e,board)
            if col is not None and col in legal:
                return col
            #random
            legal = get_available_cols(board)
            print(legal)
            if legal:
                chosen = wheighted_rng(board)
                return chosen
            return None
        col= check_state(yo,enemigo,s)
        if col is not None:
            return col
        else:
            test_results=trial(100)
            if all(prob == 0 for prob in test_results): #C: si no encotró una opcion mejor, elige una al azar
                return wheighted_rng(s)
            keys = list(test_results.keys())
            vals = list(test_results.values())
            return keys[vals.index(max(vals))]


