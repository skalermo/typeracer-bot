import sys
from PySide2 import QtWidgets
# from PySide2.QtCore import QTimer


from bot import Bot
from gui.view import Ui_MainWindow
from gui.controller import Controller


def main():
    app = QtWidgets.QApplication(sys.argv)
    model = Bot()
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ctrl = Controller(app, model, ui)
    ui.getTextBtn.clicked.connect(ctrl.get_text)
    ui.startRaceBtn.clicked.connect(ctrl.start_race)
    ui.solveChallengeBtn.clicked.connect(ctrl.solve_challenge)
    ui.closeAll.clicked.connect(ctrl.close_all)
    ui.speedSlider.valueChanged.connect(ctrl.speed_changed_slider)
    ui.speedLine.textChanged.connect(ctrl.speed_changed_editText)

    MainWindow.show()
    MainWindow.move(1280, 0)
    MainWindow.setFixedSize(MainWindow.size())
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

