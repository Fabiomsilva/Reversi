BS = 8 

EMPTY = 0
BLACK = 1
WHITE = 2
HASH_KEY = 18446744073709551557


class Reversi:
    """
    The Reversi game board and core mechanism
    """
    def __init__(self):
        self.board = None
        self.current = None
        self.reset()

    def reset(self):
        """
        Resets the game board to its initial state
        """
        # Use double list comprehensions to avoid referring to same sub-list
        self.board = [[EMPTY for _ in range(BS)] for _ in range(BS)]
        self.board[int(BS/2-1)][int(BS/2-1)] = self.board[int(BS/2)][int(BS/2)] = BLACK  # The starting pieces
        self.board[int(BS/2-1)][int(BS/2)] = self.board[int(BS/2)][int(BS/2-1)] = WHITE
        self.current = BLACK

    def toggle(self):
        """
        Toggle move
        """
        # A trick used commonly in code golfs
        self.current = [BLACK, WHITE][self.current == BLACK]

    def check_original(self, x, y, dx, dy, player=None, operate=False, func=lambda *a: None):
        """
        Checks if a move can turn any other pieces in a given direction

        Parameters:
            x, y:    The position of the move
            dx, dy:  Specify a direction
            player:  Who
            operate: Perform the actual move after checking
            func:    Anything additive to perform

        Return: A boolean value indicating changes
        """
        if player is None:  # Process default value
            player = self.current

        found = False
        c = 0
        while True:
            x += dx
            y += dy
            if not (0 <= x < BS and 0 <= y < BS):
                break
            chess = self.board[x][y]
            if chess == EMPTY:      # if empty cant place because i only can plance if there is some peace in the neighbour
                break
            elif chess == player:   # if there is one peace of the current player
                found = True
                break
            else:
                c += 1

        if c > 0 and found:
            if operate:
                while c > 0:
                    x -= dx
                    y -= dy
                    self.board[x][y] = player
                    func(x, y)
                    c -= 1
            return True
        return False

    def check(self, x, y, dx, dy, player=None, operate=False, func=lambda *a: None):
        """
        Checks if a move can turn any other pieces in a given direction

        Parameters:
            x, y:    The position of the move
            dx, dy:  Specify a direction
            player:  Who
            operate: Perform the actual move after checking
            func:    Anything additive to perform

        Return: A boolean value indicating changes
        """
        if player is None:  # Process default value
            player = self.current

        found = False
        c = 0
        while True:
            x += dx
            y += dy
            if not (0 <= x < BS and 0 <= y < BS):
                break
            chess = self.board[x][y]
            if chess == EMPTY:      # if empty cant place because i only can plance if there is some peace in the neighbour
                break
            elif chess == player:   # if there is one peace of the current player
                found = True
                break
            else:
                c += 1

        if c > 0 and found:
            if operate:
                while c > 0:
                    x -= dx
                    y -= dy
                    self.board[x][y] = player
                    func(x, y)
                    c -= 1
            return True
        return False

    def canPut(self, x, y, player=None):
        """
        Determine if a player can put a move at a given position by checking
        all BS directions around this spot
        """
        if player is None:
            player = self.current

        if self.board[x][y] != EMPTY:
            return False
        # any() and list comprehension is slower
        return self.check(x, y, -1, -1, player) or self.check(x, y, 1, 1, player) or \
            self.check(x, y, -1, 0, player) or self.check(x, y, 1, 0, player) or \
            self.check(x, y, -1, 1, player) or self.check(x, y, 1, -1, player) or \
            self.check(x, y, 0, -1, player) or self.check(x, y, 0, 1, player)

    def getAvailables(self, player=None):
        """
        Get positions of all available moves for a player
        """
        if player is None:
            player = self.current

        return [(x, y) for x in range(BS) for y in range(BS) if self.canPut(x, y, player)]

    def any(self, player=None):
        """
        Check if a player can move now (for skipping moves)
        """
        if player is None:
            player = self.current
        # Usually True, use a generator expression hoping to save some calculation
        return any(self.canPut(x, y, player) for x in range(BS) for y in range(BS))

    @property
    def over(self):
        """
        Is game over? (Both sides cannot move)
        """
        return (not self.any(BLACK)) and (not self.any(WHITE))

    def at(self, x, y):
        return self.board[x][y]

    @property
    def chessCount(self):
        """
        Get the current score

        Returns a list, [empty, black, white]
        """
        # Relies on EMPTY, BLACK, WHITE == 0, 1, 2
        cc = [0, 0, 0]

        for x in range(BS):
            for y in range(BS):
                cc[self.board[x][y]] += 1
        return cc

    def put(self, x, y=None, player=None):
        """
        Perform a move at a given position.

        Accepts a tuple at parameter 1, or two numbers at parameters 1 and 2
        """
        if y is None:
            # Unpack the tuple
            x, y = x
        if self.board[x][y] != EMPTY:
            return False
        if player is None:
            player = self.current

        changes = []  # Save changes for undo

        def saveChange(x, y):
            changes.append((x, y))

        self.check(x, y, -1, -1, player, True, saveChange)
        self.check(x, y, 1, 1, player, True, saveChange)
        self.check(x, y, -1, 0, player, True, saveChange)
        self.check(x, y, 1, 0, player, True, saveChange)
        self.check(x, y, -1, 1, player, True, saveChange)
        self.check(x, y, 1, -1, player, True, saveChange)
        self.check(x, y, 0, -1, player, True, saveChange)
        self.check(x, y, 0, 1, player, True, saveChange)

        if len(changes) == 0:  # Not movable
            return False

        self.board[x][y] = player
        changes.append((x, y))
        self.toggle()
        self.skipPut()
        return True

    def skipPut(self):
        """
        If a player cannot move, they should skip
        """
        if self.any(self.current):
            return False
        self.toggle()
        return True

    def copy(self):
        """
        Create a copy of this Reversi game
        """
        game = Reversi()
        game.board = [list(col) for col in self.board]
        game.current = self.current
        return game

    def __hash__(self):
        res = 0
        for x in range(BS):
            for y in range(BS):
                res = (3 * res + self.board[x][y]) % HASH_KEY
        return res ^ (1 + self.current)

