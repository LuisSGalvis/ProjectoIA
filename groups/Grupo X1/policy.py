import numpy as np
from connect4.policy import Policy
from typing import List

# mejorar el contra aleatorio
class politica_epica(Policy):

    
    def mount(self) -> None:
        pass

    
    def act(self, s: np.ndarray) -> int:
        yo=1 #no se como sacar si soy 1 o -1 asi que por ahora soy 1
        enemigo = -yo
        ver = int(0) #para cambiar entre el basico y el MCTS cuando lo tenga
        if(ver==0):#si tienen mejor idea para esta parte apliquenla porque si esta estupida 
                   #y no fue buena idea en retrospectiva. Galvis
            def get_heights(self) -> List[int]:# lo saque de clase 1
                HeightList=[0,0,0,0,0,0,0]
                for col in range(7):
                    for row in reversed(range(6)):
                        if s[row,col] != 0:
                            HeightList[col] += 1
                            print(HeightList)
                        else: break
                return HeightList
            # para vencer aleatorios tenemos que bloquear si van a ganar, una especie de subtrial
            # y ganar si estamos cerca, luego nos centramos en que aprenda de verdad
            pv = bool(False) # veo victoria en mi proximo turno?
            pd = bool(False) # veo derrota en mi proximo turno?
            rng = np.random.default_rng()
            available_cols = [c for c in range(7) if s[0, c] == 0]
            for cols in available_cols:
                tab2 = s.copy()
                h= get_heights(tab2)        
                tab2[5-h[cols],cols]=1
                for row in range(6): #cambiar el row col
                    for col in range(4):#hor
                        if (tab2[row, col] == 1 and tab2[row, col+1] == 1 and tab2[row, col+2] == 1 and tab2[row, col+3] == 1):
                                pv = True
                                return cols
                for r in range(3):
                    for c in range(7):#ver
                        if (tab2[r, c] == 1 and tab2[r+1, c] == 1 and tab2[r+2, c] == 1 and tab2[r+3, c] == 1):
                                pv = True
                                return cols
                for r in range(3):
                    for c in range(4):#diagonal
                        if (tab2[r, c] == 1 and tab2[r+1, c+1] == 1 and tab2[r+2, c+2] == 1 and tab2[r+3, c+3] == 1):
                                pv = True
                                return cols
                for r in range(3):
                    for c in range(3, 7):#otro diagonal
                        if (tab2[r, c] == 1 and tab2[r+1, c-1] == 1 and tab2[r+2, c-2] == 1 and tab2[r+3, c-3] == 1):
                            pv = True
                            return cols
                #esto no fue mi mejor idea, si se les ocurre algo mejor porfa cambienlo
            for cols in available_cols:
                tab2 = s.copy()
                h= get_heights(tab2)        
                tab2[5-h[cols],cols]=-1
                for row in range(6): #cambiar el row col
                    for col in range(4):#hor
                        if (tab2[row, col] == -1 and tab2[row, col+1] == -1 and tab2[row, col+2] == -1 and tab2[row, col+3] == -1):
                                pd = True
                                return cols
                for r in range(3):
                    for c in range(7):#ver
                        if (tab2[r, c] == -1 and tab2[r+1, c] == -1 and tab2[r+2, c] == -1 and tab2[r+3, c] == -1):
                                pd = True
                                return cols
                for r in range(3):
                    for c in range(4):#diagonal
                        if (tab2[r, c] == -1 and tab2[r+1, c+1] == -1 and tab2[r+2, c+2] == -1 and tab2[r+3, c+3] == -1):
                                pd = True
                                return cols
                for r in range(3):
                    for c in range(3, 7):#otro diagonal
                        if (tab2[r, c] == -1 and tab2[r+1, c-1] == -1 and tab2[r+2, c-2] == -1 and tab2[r+3, c-3] == -1):
                                pd = True
                                return cols
                #Reitero, porfa si tienen una mejor idea cambienlo, esta horrible esto
            if(pv==False and pd==False):
                if(get_heights(s)[2]<=5): #si no hay piezas colocadas coloca en espacio 3 para tener el medio
                     return 2
                elif(get_heights(s)[3]<=5):
                     return 3
                return rng.choice(available_cols)

            
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
            
