import numpy as np
from connect4.policy import Policy
from typing import List
from math import sqrt, log
import time

class politica_carlos(Policy):

    def mount(self, time_out:int=10) -> None:
        self.time_out=time_out

    #C: cambié un poco la estructura, para no perderse

    def get_current_player(self,board):
        c_neg = np.count_nonzero(board == -1)
        c_pos = np.count_nonzero(board == 1)
        return -1 if c_neg == c_pos else 1

    #==Funciones==
    def wheighted_rng(self,board):
        legal = self.get_available_cols(board)
        if not legal:
            return None
        for preferred in [2, 3]:
            if preferred in legal:
                return preferred
        chosen = self.rng.choice(legal)
        return chosen
    def get_heights(self,board: np.ndarray) -> List[int]:# lo saque de clase 1
        HeightList=[0,0,0,0,0,0,0]
        for col in range(7):
            for row in range(6):
                if board[row,col] != 0:
                    HeightList[col] += 1

        return HeightList


    def play(self,col: int, p: int, board: np.ndarray):
        row = self.get_heights(board)[col]
        if row >= 6:
            raise ValueError(f"Column {col} is full!")
        board[5-row, col] = p
    #C: Y una función para determinar si ganamos
    def check_winner(self,board: np.ndarray, p: int) -> bool:
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
    #J: Modificar trials a que termine juegos y t sea la cantidad de juegos ( o el tiempo que tiene para hacerlo

    def get_available_cols(self,board):
        return [c for c in range(7) if self.get_next_row(c, board) is not None]
    def get_next_row(self,col,board):
        heights = self.get_heights(board)
        if heights[col] >= 6:
            return None  # columna llena
        return 5 - heights[col]

    def check_state(self,p: int, e: int, board: np.ndarray):
        def find3plus1(jugador,board):
            #horizontal
            for r in range(0,6):
                for c in range(0,4):
                    secuencia= board[r,c:c+4]
                    if list(secuencia).count(jugador) ==3 and list(secuencia).count(0)==1:
                        hueco=list(secuencia).index(0)
                        columna = c+hueco
                        if columna in self.get_available_cols(board) and self.get_next_row(columna,board) == r :
                            return columna
            #verticla
            for c in range(0,7):
                for r in range(0,3):
                    secuencia= [board[r+i,c]for i in range(4)]
                    if secuencia.count(jugador) ==3 and secuencia.count(0)==1:
                        hueco = secuencia.index(0)
                        fila=r +hueco
                        fila_real = self.get_next_row(c,board)

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
                        if  columna in self.get_available_cols(board) and self.get_next_row(columna,board) == fila :
                            return columna
            #daigonal izquierda
            for r in range(0,3):
                for c in range(3,7):
                    secuencia=[board[r+i,c-i] for i in range(4)]
                    if secuencia.count(jugador)==3 and secuencia.count(0)==1:
                        hueco= secuencia.index(0)
                        columna = c -hueco
                        fila = r +hueco
                        if columna in self.get_available_cols(board) and self.get_next_row(columna,board) == fila :
                            return columna
            return None
        #ganar
        col = find3plus1(p,board)
        legal = self.get_available_cols(board)
        if col is not None and col in legal:
            return col
        #bloquear
        col = find3plus1(e,board)
        if col is not None and col in legal:
            return col
        return None
    def act(self, s: np.ndarray) -> int:
        start_time=time.time()
        yo = self.get_current_player(s)
        enemigo = -yo

        self.rng = np.random.default_rng()

        col= self.check_state(yo,enemigo,s)
        if col is not None:
            return int(col)
        #macro
        if col is not None:
            return int(col)

        legal=self.get_available_cols(s)

        return self.MCTS_choose(s,yo,legal,start_time)
    class Nodo:
        def __init__(self,board,jugador,parent=None,move=None):
            self.board=board
            self.jugador=jugador
            self.parent=parent
            self.move=move
            self.children={}
            self.W=0
            self.N=0
            self.untried_moves=None
    def MCTS_choose(self,board,jugador,legal,start_time):
        root = self.Nodo(board.copy(),jugador)
        root.untried_moves= legal.copy()

        while time.time() -start_time < self.time_out:

            nodo= root
            tablero=board.copy()
            p_actual=jugador

            #seleccion
            while nodo.untried_moves == [] and nodo.children:
                nodo= self.MCTS_select(nodo)
                self.play(nodo.move,p_actual,tablero)
                p_actual=-p_actual
            #Expansion
            if nodo.untried_moves:
                move= nodo.untried_moves.pop()
                ntablero=tablero.copy()
                self.play(move,p_actual,ntablero)

                child= self.Nodo(ntablero,p_actual, parent=nodo, move=move)
                child.untried_moves= self.get_available_cols(ntablero)
                nodo.children[move]= child

                nodo=child
                tablero=ntablero
                p_actual=-p_actual

                #simulacion
                resultado=self.simular(tablero.copy(),nodo.jugador)

                #backpropagation
                self.backpropagate(nodo,resultado)
        mejor= max(root.children.items(),key=lambda x:x[1].N)[0]
        return mejor

    def MCTS_select(self,nodo):
        logN= log(nodo.N+1)
        C= 1.3
        def UCB(child):
            if child.N == 0:
                return float('inf')
            return (child.W/child.N)+ C * sqrt(logN/child.N)
        return max(nodo.children.values(), key=UCB)

    def backpropagate(self,nodo,resultado):
        while nodo is not None:
            nodo.N +=1
            nodo.W+=resultado
            nodo=nodo.parent

    def simular(self,board,jugador):
        while True:
            legal=self.get_available_cols(board)
            if not legal:
                return 0

            col = self.check_state(jugador,-jugador,board)

            if col is None:
                col= self.wheighted_rng(board)
            else:
                col= col

            self.play(col,jugador,board)

            if self.check_winner(board,jugador):
                return 1
            jugador=-jugador