import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test PyQt5")
        self.setGeometry(100, 100, 400, 300)
        self.label = QLabel("PyQt5 is working!", self)
        self.label.setGeometry(50, 50, 200, 50)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
