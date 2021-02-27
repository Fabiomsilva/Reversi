from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import reversi 
from reversi import BS
import ai

if BS == 8:
    GRID_SIZE = 50
else:
    GRID_SIZE = 25  #Side length of a grid

# Constants that will affect how it looks
BOARD_SIZE = GRID_SIZE*BS+40 #520  # Side length of whole board, including margin
PIECE_SIZE = 21  # Diameter of circle that represents a piece
DOT_SIZE = 9  # Dot indicator of possible moves
IND_SIZE = 128  # The score indicator on the left, diameter of circle
IND_BOARD_SIZE = 150  # Same as above, side length of canvas

margin = (BOARD_SIZE - BS * GRID_SIZE) // 2  # Should be some 20
padding = (GRID_SIZE - PIECE_SIZE) // 2  # Should be some 10
d_padding = (GRID_SIZE - DOT_SIZE) // 2  # Should be some 25
ind_margin =  (IND_BOARD_SIZE - IND_SIZE) // 2

class ReversiUI(QWidget):
    def __init__(self):
        self.game = reversi.Reversi()
        self.ai = ai.Reversi_AI()
        BS = reversi.BS
        self.ai.setLevel(0)
        self.player1 = reversi.BLACK
        self.player2 = reversi.WHITE
        self.typeGameMode = 1                   # 1:Human-Computer, 2:Computer-Computer, 3:Human-Human

        # Create layout
        super(ReversiUI, self).__init__()
        self.master = QHBoxLayout()
        self.controlBar = QVBoxLayout()
        self.infoBar = QVBoxLayout()
        self.score_str = "{}"
        self.current_player = QLabel()
        self.current_player.setText("Current Player")
        self.current_player.setAlignment(Qt.AlignCenter)
        self.scoreLabelA = ScoreIndicator(reversi.BLACK)
        self.scoreLabelB = ScoreIndicator(reversi.WHITE)
        self.painter = PaintArea()
        self.painter.setFocusPolicy(Qt.StrongFocus)
        self.init_ui()

    def init_ui(self):
        # Insert elements into layout
        self.master.addLayout(self.controlBar)
        self.master.addWidget(self.painter)
        self.controlBar.addLayout(self.infoBar)
        self.infoBar.addWidget(self.scoreLabelA)
        self.infoBar.addWidget(self.scoreLabelB)
        self.infoBar.addWidget(self.current_player)

        self.reset_button = QPushButton("New Game")
        self.ai_move_button = QPushButton("AI Move")
        self.diffBox = QComboBox()
        self.diffBox.addItems(["1: Easy", "2: Medium", "3: Hard"])
        self.typeBox = QComboBox()
        self.typeBox.addItems(["1: Human-Computer", "2: Computer-Computer", "3: Human-Human"])
        self.ai_move_button = QPushButton("AI Move")
        self.ai_move_button.setHidden(False)

        self.controlBar.addWidget(self.ai_move_button)
        self.controlBar.addWidget(self.typeBox)
        self.controlBar.addWidget(self.diffBox)
        self.controlBar.addWidget(self.reset_button)

        # Add events
        def boardClick(event):
            """
            Event handler of mouse click on the "game board" canvas
            """
            ex, ey = event.x(), event.y()
            gx, gy = (ex - margin) // GRID_SIZE, (ey - margin) // GRID_SIZE
            rx, ry = ex - margin - gx * GRID_SIZE, ey - margin - gy * GRID_SIZE
            if 0 <= gx < BS and 0 <= gy < BS and \
                    abs(rx - GRID_SIZE / 2) < PIECE_SIZE / 2 > abs(ry - GRID_SIZE / 2):
                self.onClickBoard((gx, gy))

        def diffChange(index):
            """
            Event handler on "Difficulty" cascade menu changes
            """
            self.ai.setLevel(index)
            self.resetGame()
            self.update_ui

        def typeGame(index):
            """
            Event handler on "type" cascade menu changes
            1:Human-Computer, 2:Computer-Computer, 3:Human-Human
            """
            self.typeGameMode = index+1 

            if self.typeGameMode == 1: # Human-Computer
                self.ai_move_button.setHidden(False)
            if self.typeGameMode == 2: # Computer-Computer   
                self.ai_move_button.setHidden(False)
            if self.typeGameMode == 3: # Human-Human
                self.ai_move_button.setHidden(True)
            self.update_ui
            self.resetGame()
            

        self.reset_button.clicked.connect(self.resetGame)
        self.painter.mouseReleaseEvent = boardClick
        self.diffBox.currentIndexChanged.connect(diffChange)
        self.typeBox.currentIndexChanged.connect(typeGame)
        self.ai_move_button.clicked.connect(self.aiMove)
        
        
        self.setLayout(self.master)
        self.setWindowTitle("Reversi: IA FEUP")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint)

        self.show()
        self.resetGame()
        self.setFixedSize(self.size())

    def aiMove(self):
        """
        To perform an AI move
        """
        #means that is human vs computer and is human turn
        if self.game.current ==1 and self.typeGameMode == 1:         
            return
        # -----------------------------------#
        aiMove = self.ai.findBestStep(self.game)
        if aiMove == ():
            self.game.skipPut()
            self.game.toggle()
            return
        #means that is "Computer1" vs "computer2"
        if self.game.current ==1 and self.typeGameMode == 2:         
            self.current_player.setText("WHITE")
        else:
            self.current_player.setText("BLACK")
        # -----------------------------------#
        print("AI Move:", aiMove[0], aiMove[1])
        self.game.put(aiMove)
        self.update_ui(True)

    def human_computer(self, pos):
        if  self.game.current == 1:
            x, y = pos
            if not self.game.canPut(x, y):  # bad move, not possible move
                self.update_ui(True)
                return
            if not self.game.any():         # if does not have any available chance
                self.game.toggle()
                self.update_ui(True)
                return
            self.game.put(x, y)
            print("Human Move:", x,y)
            self.current_player.setText("WHITE")
            self.update_ui(True)    
        else:
            self.current_player.setText("BLACK")
    
    def human_human(self, pos):
        if  self.game.current == 1:
            x, y = pos
            if not self.game.canPut(x, y):  # bad move, not possible move
                self.update_ui(True)
                return
            if not self.game.any():         # if does not have any available chance
                self.game.toggle()
                self.update_ui(True)
                return
            self.game.put(x, y)
            self.current_player.setText("WHITE")
            self.update_ui(True)
        else:
            x, y = pos
            if not self.game.canPut(x, y):  # bad move, not possible move
                self.update_ui(True)
                return
            if not self.game.any():         # if does not have any available chance
                self.game.toggle()
                self.update_ui(True)
                return
            self.game.put(x, y)
            self.current_player.setText("BLACK")
            self.update_ui(True)

    def onClickBoard(self, pos):
        """
        Game event handler on clicking the board
        """ 
        i, x = pos
        #if there is one peace there i cant put another one
        if self.game.board[i][x] != 0:
            return
        if self.typeGameMode == 1: # Human-Computer
            self.human_computer(pos) 
        if self.typeGameMode == 3: # Human-Human
            self.human_human(pos)

        empty, black, white = self.game.chessCount
        if  empty == 0:
            if black == white:
                QMessageBox.information(self,"Tie!")
            elif black > white:
                QMessageBox.information(self, "Reversi", "Black Wins!")
            elif black < white:
                QMessageBox.information(self, "Reversi", "white Wins!")

    def update_board(self):
        """
        Wrapped function to update the appearance of the board

        Primarily, setting data for the actual painter function to process
        """
        _, ccBlack, ccWhite = self.game.chessCount
        self.scoreLabelA.setNumber(ccBlack)
        self.scoreLabelB.setNumber(ccWhite)
        self.scoreLabelA.update()
        self.scoreLabelB.update()
        self.painter.assignBoard(self.game.board)
        if self.player1 or self.player2:
            self.painter.assignDots(self.game.getAvailables())
        else:
            self.painter.assignDots(None)
        self.painter.update()

    def update_ui(self, force=False):
        """
        Workaround of UI getting stuck at waiting AI calculation

        See: https://stackoverflow.com/q/49982509/5958455
        """
        self.update_board()
        if force:
            QApplication.instance().processEvents()

    def resetGame(self):
        """
        Start over the game
        """
        self.game.reset()
        self.update_ui()
        self.current_player.setText("Current Player")

class PaintArea(QWidget):
    """
    The class that handles the drawing of the game board
    """

    def __init__(self, board=None):
        super(PaintArea, self).__init__()
        self.board = board
        self.dots = None

        self.setPalette(QPalette(Qt.white))
        self.setAutoFillBackground(True)
        self.setMinimumSize(BOARD_SIZE, BOARD_SIZE)

        self.penConfig = \
            [Qt.black, 2, Qt.PenStyle(Qt.SolidLine), Qt.PenCapStyle(Qt.RoundCap), Qt.PenJoinStyle(Qt.MiterJoin)]
        self.noPen = \
            QPen(Qt.black, 2, Qt.PenStyle(Qt.NoPen), Qt.PenCapStyle(Qt.RoundCap), Qt.PenJoinStyle(Qt.MiterJoin))
        brushColorFrame = QFrame()
        brushColorFrame.setAutoFillBackground(True)
        brushColorFrame.setPalette(QPalette(Qt.white))
        self.brushConfig = Qt.white, Qt.SolidPattern
        self.update()

    def assignBoard(self, board):
        # Copy the board to avoid accidental change to original board
        self.board = [list(i) for i in board]

    def assignDots(self, dots):
        # This one won't change, no need to copy
        self.dots = dots

    def paintEvent(self, QPaintEvent):
        """
        Called by QWidget (superclass) when an update event arrives
        """
        if self.board is None:
            raise ValueError("Cannot paint an empty board!")
        p = QPainter(self)

        self.penConfig[0] = Qt.darkGray
        p.setPen(QPen(*self.penConfig))
        p.setBrush(QBrush(*self.brushConfig))
        # Draw the grids
        for i in range(BS+1):
            A = QPoint(margin, margin + i * GRID_SIZE)
            B = QPoint(BOARD_SIZE - margin, margin + i * GRID_SIZE)
            p.drawLine(A, B)
            A = QPoint(margin + i * GRID_SIZE, margin)
            B = QPoint(margin + i * GRID_SIZE, BOARD_SIZE - margin)
            p.drawLine(A, B)

        self.penConfig[0] = Qt.black
        p.setPen(QPen(*self.penConfig))
        # Draw game pieces
        for i in range(BS):
            for j in range(BS):
                if self.board[i][j] == 0:
                    continue
                fillColor = [None, Qt.black, Qt.white]
                p.setBrush(QBrush(fillColor[self.board[i][j]], Qt.SolidPattern))
                p.drawEllipse(QRect(
                    margin + padding + i * GRID_SIZE, margin + padding + j * GRID_SIZE,
                    PIECE_SIZE, PIECE_SIZE))

        # Draw dot indicators if available
        if self.dots is not None:
            p.setPen(self.noPen)
            p.setBrush(QBrush(Qt.darkGreen, Qt.SolidPattern))
            for x, y in self.dots:
                p.drawEllipse(QRect(
                    margin + d_padding + x * GRID_SIZE, margin + d_padding + y * GRID_SIZE,
                    DOT_SIZE, DOT_SIZE))

class ScoreIndicator(QWidget):
    """
    The class that handles the drawing of the score indicator on the left
    """

    def __init__(self, color):
        super(ScoreIndicator, self).__init__()
        self.color = color
        self.number = None
        self.borderPen = \
            QPen(Qt.black, 3, Qt.PenStyle(Qt.SolidLine), Qt.PenCapStyle(Qt.RoundCap), Qt.PenJoinStyle(Qt.MiterJoin))

        self.setAutoFillBackground(False)
        self.setMinimumSize(IND_BOARD_SIZE, IND_BOARD_SIZE)

    def setNumber(self, n):
        self.number = n

    def paintEvent(self, event):
        p = QPainter(self)

        b = QRect(ind_margin, ind_margin, IND_SIZE, IND_SIZE)
        # Draw background circles
        if self.color == reversi.BLACK:
            p.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        elif self.color == reversi.WHITE:
            p.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        else:
            raise ValueError("Invalid color set!")
        p.setPen(self.borderPen)
        p.drawEllipse(b)

        # Add numbers (text)
        if self.color == reversi.BLACK:
            p.setPen(QPen(Qt.white, 48))
        elif self.color == reversi.WHITE:
            p.setPen(QPen(Qt.black, 48))
        p.setFont(QFont("Arial", 48, QFont.Bold))
        p.drawText(b, Qt.AlignCenter, str(self.number))
