import copy
import math
import random

# import some constants
from reversi import BS, EMPTY, BLACK, WHITE

inf = 999999 
MIN_NODES = 10000
MIN_TICK = 1000
if BS == 8:
    SCORE = [
        [  500, -150, 30, 10, 10, 30, -150,  500],  # noqa: E201, E241
        [ -150, -250,  0,  0,  0,  0, -250, -150],  # noqa: E201, E241
        [   30,    0,  1,  2,  2,  1,    0,   30],  # noqa: E201, E241
        [   10,    0,  2, 16, 16,  2,    0,   30],  # noqa: E201, E241
        [   10,    0,  2, 16, 16,  2,    0,   30],  # noqa: E201, E241
        [   30,    0,  1,  2,  2,  1,    0,   30],  # noqa: E201, E241
        [ -150, -250,  0,  0,  0,  0, -250, -150],  # noqa: E201, E241
        [  500, -150, 30, 10, 10, 30, -150,  500],  # noqa: E201, E241
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

class Reversi_AI:
    def __init__(self):
        self.nodeCount = 0
        self.depth = 1
        self.maxDepth = 1
        self.final = 4
        self.aiLevel = 0
        self.setLevel()
   
    def heuristicScore(self, game, player):
        self.nodeCount += 1
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
        self.nodeCount += 1
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
        game.put(step)                                   # atention, this function put the peace and do toggle !!
        score = self.heuristicScore(game, player)
        game.undo()
        return score

    def heuristicSearch(self, game, player, depth, alpha, beta):
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
        if level is None:
            level = self.aiLevel

        self.aiLevel = level
        self.depth, self.final = AICONFIG[level]

    def findBestStep(self, game):
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
        self.nodeCount = 0
        self.maxDepth = self.depth
        save_board = copy.deepcopy(game.board)
        save_player = player
        rscore, rstep = self.heuristicSearch(game, player, self.maxDepth, -inf, inf)
        game.board = save_board.copy()
        game.current = save_player
        return rstep