from package.ui.modMonUI import Ui_MainWindow
from PyQt4 import QtGui
import sys
import qdarkstyle
import fancyqt.firefox
import logging
import globals


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoveLogger(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        logger.info("LoveLogger() __Init__")


def run():
    app = QtGui.QApplication(sys.argv)
    # setup stylesheet
    if globals.darkUI:
        app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    elif globals.fancyUI:
        app.setStyleSheet(fancyqt.firefox.style)
    form = LoveLogger()
    form.show()
    app.exec_()
    app.deleteLater()
    sys.exit(0)
