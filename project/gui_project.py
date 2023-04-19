from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle("CITS4402 Project")
        # setting  the geometry of window
        self.setGeometry(0, 0, 400, 300)
        # Create an instance of label
        self.label = QLabel(self)

        # Load image
        self.pixmap = QPixmap('treege.png')

        # Set image to label
        self.label.setPixmap(self.pixmap)

        # Resize the label according to image size
        self.label.resize(self.pixmap.width(),
                        self.pixmap.height())

        # show the widgets
        self.show()



# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()