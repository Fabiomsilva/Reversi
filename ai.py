import copy
import math
import random
from time import process_time
import csv

# import some constants
from reversi import BS, EMPTY, BLACK, WHITE

inf = 999999 

# SCORE is the values of each position of the board
if BS == 8:                 
    SCORE = [
        [  500, -150, 30, 10, 10, 30, -150,  500],  
        [ -150, -250,  0,  0,  0,  0, -250, -150],  
        [   30,    0,  1,  2,  2,  1,    0,   30],  
        [   10,    0,  2, 16, 16,  2,    0,   30],  
        [   10,    0,  2, 16, 16,  2,    0,   30],  
        [   30,    0,  1,  2,  2,  1,    0,   30],  
        [ -150, -250,  0,  0,  0,  0, -250, -150],  
        [  500, -150, 30, 10, 10, 30, -150,  500],  
    ]
else:
    SCORE = [
        [  1000, -200,  50, 20,	20,  10,    10,	  10,	10,	  10, 	10,	 20,	20,	 50, -200, 1000],
        [  -200, -500,  0,   0,	 0,	  0,	 0,	   0,	 0,	   0,	 0,	  0,	 0,	  0, -500, -200],
        [    50,    0,  0,   0,	 0,	  0,	 0,	   5,	 5,	   5,	 0,	  0,	 0,	  0,	0,   50],
        [    20,    0,  0,   0,	 0,	  0,	 0,	   6,	 6,	   6,	 0,	  0,	 0,	  0,	0,   20],
        [    20,    0,  1,   2,	 3,	  4,	10,   10,	10,	  10,	 4,	  3,	 2,	  1,	0,   20],
        [    10,    0,  2,   3,	 4,	  5,	11,   12,	12,	  12,	 5,	  4,	 3,	  2,	0,   10],
        [    10,    0,  3,   4,	 5,	  6,	12,   15,	15,	  15,	 6,	  5,	 4,	  3,	0,   10],
        [    10,    0,  3,   4,	 5,	  6,	15,   16,	16,	  16,	 6,	  5,	 4,	  3,	0,   10],
        [    10,    0,  3,   4,	 5,	  6,	15,   16,	16,	  16,	 6,	  5,	 4,	  3,	0,   10],
        [    10,    0,  3,   4,	 5,	  6,	12,   15,	15,	  15,	 6,	  5,	 4,	  3,	0,   10],
        [    10,    0,  2,   3,	 4,	  5,	11,   12,	12,	  12,	 5,	  4,	 3,	  2,	0,   10],
        [    20,    0,  1,   2,	 3,	  4,	10,   10,	10,	  10,	 4,	  3,	 2,	  1,	0,   20],
        [    20,    0,  0,   0,	 0,	  0,	 0,	   6,	 6,	   6,	 0,	  0,	 0,	  0,	0,   20],
        [    50,    0,  0,   0,	 0,	  0,	 0,	   5,	 5,	   5,	 0,	  0,	 0,	  0,	0,   50],
        [  -200, -500,  0,   0,	 0,	  0,	 0,	   0,	 0,	   0,	 0,	  0,	 0,	  0, -500, -200],
        [  1000, -200, 50,  20, 20,  10,    10,   10,   10,   10,   10,  20,    20,  50, -200, 1000],
    ]

BONUS = 30          # corner bonus 

# depth final
AICONFIG = [
    (1, 4),
    (2, 6),
    (3, 8),
]

AICONFIG1 = [
    (1, 4),
    (2, 6),
    (3, 8),
]

AICONFIG2 = [
    (1, 4),
    (2, 6),
    (3, 8),
]

class Reversi_AI:
    def __init__(self):
        self.depth = 1
        self.maxDepth = 1
        self.final = 4
        self.aiLevel = 0
        self.dif1 = 0
        self.dif2 = 0
        self.setLevel()
   
    def heuristicScore(self, game, player):
        '''
        calculates heuristic score acording to the SCORE defined for each place of the board
        '''
        c1, c2, s1, s2 = 0, 0, 0, 0
        board = game.board
        for x in range(BS):
            for y in range(BS):
                chess = board[x][y]
                if chess == EMPTY:
                    continue
                liberty = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        tx, ty = x + dx, y + dy
                        if 0 <= tx < BS and 0 <= ty < BS and board[tx][ty] == EMPTY:
                            liberty += 1
                if chess == player:
                    c1 += 1
                    s1 += SCORE[x][y] 
                else:
                    c2 += 1
                    s2 += SCORE[x][y]
        if c1 == 0:
            return -inf
        if c2 == 0:
            return inf
        if c1 + c2 == BS ** 2:
            if c1 > c2:
                return inf
            if c2 > c1:
                return -inf


        def checkCorner(pos, adjacents, dpos):
            """
            check (start, adjacents, diagonal position)
            """
            nonlocal s1, s2

            x, y = pos
            dx, dy = dpos
            chess = board[x][y]
            if chess != EMPTY:
                for cx, cy in adjacents:
                    chess = board[cx][cy]
                    if chess == EMPTY:
                        continue
                    if chess == player:
                        s1 += SCORE[cx][cy]
                    else:
                        s2 += SCORE[cx][cy]
                
                tx, ty = x, y
                for i in range(0, BS - 2):
                    tx += dx
                    if board[tx][ty] != chess:
                        break
                    if player == chess:
                        s1 += BONUS
                    else:
                        s2 += BONUS

                tx, ty = x, y
                for i in range(0, BS - 2):
                    ty += dy
                    if board[tx][ty] != chess:
                        break
                    if player == chess:
                        s1 += BONUS
                    else:
                        s2 += BONUS
        
        checkCorner((0, 0), [(0, 1), (1, 0), (1, 1)], (1, 1))                                               # top left corner 
        checkCorner((BS - 1, 0), [(BS - 2, 0), (BS - 2, 1), (BS - 1, 1)], (-1, 1))                          # top right corner
        checkCorner((0, BS - 1), [(0, BS - 2), (1, BS - 2), (1, BS - 1)], (1, -1))                          # bottom left corner
        checkCorner((BS - 1, BS - 1), [(BS - 2, BS - 2), (BS - 2, BS - 1), (BS - 1, BS - 2)], (-1, -1))     # bottom right corner

        return s1 - s2

    def exactScore(self, game, player):
        """
        check (start, adjacents, diagonal position)
        """
        _, ccBlack, ccWhite = game.chessCount
        score = 0
        if ccBlack > ccWhite:
            score = inf
        elif ccBlack < ccWhite:
            score = -inf
        if player == WHITE:
            score = -score
        return score

    def getHeuristicScore(self, game, player, step):
        '''
        returns heuristicScore for the position of the current player acordind to the step
        '''
        game.put(step)                                   
        score = self.heuristicScore(game, player)
        game.undo()
        return score

    def heuristicSearch(self, game, player, depth, alpha, beta):
        '''
        returns the score and the best move to archive this score wit minmax implementation
        '''
        if depth <= 0:
            return self.heuristicScore(game, player), ()

        maxMode = (game.current == player)
        score = -inf-1 if maxMode else inf+1
        steps = game.getAvailables()
        bestStep = ()

        if len(steps) > 0:
            hValue = {}
            for step in steps:
                hValue[step] = self.getHeuristicScore(game, player, step)
            steps = sorted(steps, key=lambda s: hValue[s], reverse=maxMode)

            if depth == 1:
                step = steps[0]
                return hValue[step], step
            for step in steps:
                game.put(step)
                rscore, rstep = self.heuristicSearch(game, player, depth - 1, alpha, beta)
                game.undo()
                if maxMode:
                    if rscore > score:
                        score, bestStep = rscore, step
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break
                else:
                    if rscore < score:
                        score, bestStep = rscore, step
                    beta = min(beta, score)
                    if alpha >= beta:
                        break
        else:
            if not game.over:
                game.skipPut()
                return self.exactScore(game, player), ()
            else:
                return self.exactScore(game, player), ()
        return score, bestStep

    def setLevel(self, level=None):
        '''
        Defines AI level if the type of the game was human vs computer
        '''
        if level is None:
            level = self.aiLevel

        self.aiLevel = level
        self.depth, self.final = AICONFIG[level]
    
    def setLevel_ai_comp(self, level=None, c_player=None):
        '''
        Update AI level if the type of the game was computer vs computer
        '''
        if c_player == 1:
            self.dif1=level
        if c_player == 2:
            self.dif2=level

    def check_ai_level(self, c_player):
        '''
        Defines AI level (by GUI comboBox) if the type of the game was computer vs computer
        '''
        if c_player == 1:
            self.depth, self.final = AICONFIG1[self.dif1]

        if c_player == 2:
            self.depth, self.final = AICONFIG2[self.dif2]
        
    def findBestStep(self, game):
        '''
        finds best step. If hte total amount of peaces were less than 20% return a random move but
        if the amout was higher then 20% return according to heuristic search
        '''
        player = game.current
        steps = game.getAvailables()
        _, ccBlack, ccWhite = game.chessCount
        cc = ccBlack + ccWhite
        if len(steps) <= 0:
            return ()

        # Random mode if the total amount of peaces were less then 20% of all 
        if cc <= (BS **2)*0.2:
            randSteps = []
            for x, y in steps:
                if 2 <= x < BS - 2 and 2 <= y < BS - 2:
                    randSteps.append((x, y))
            if len(randSteps) > 0:
                return random.choice(randSteps)

        # Heuristic search
        self.maxDepth = self.depth
        save_board = copy.deepcopy(game.board)
        save_player = player
        start = process_time()                                      # to count the processing time
        rscore, rstep = self.heuristicSearch(game, player, self.maxDepth, -inf, inf)
        stop = process_time()                                       # to count the processing time
        game.board = save_board.copy()
        game.current = save_player
        
        #collect data to csv file
        time_elapsed = stop-start
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow([str(BS),str(time_elapsed),str(self.dif1+1), str(self.dif2+1)])
        return rstep