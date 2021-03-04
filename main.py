import sys
from PyQt5.QtWidgets import QApplication
import reversi 

print("welcome")
reversi.BS = int(input("Enter size: 8, 16\n")) 
while reversi.BS != 8 and reversi.BS !=16:
    reversi.BS = int(input("Enter size: 8 or 16\n")) 

while(True):
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        import qt
        ui = qt.ReversiUI()
        sys.exit(app.exec_())
