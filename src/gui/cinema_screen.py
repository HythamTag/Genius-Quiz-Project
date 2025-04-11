import signal

from PyQt6 import QtGui
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from src.core.sound_engine import Sound_Action

signal.signal(signal.SIGINT, signal.SIG_DFL)


class CinemaApp(QMainWindow):
    time_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(CinemaApp, self).__init__(parent)

        ''' ############## Load the uit of the GUI ############## '''
        self.ui = uic.loadUi('src/resources/ui/Cinema.ui', self)
        self.MainApp = parent
        self.label_cinemaQuestion.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label_cinemaAnswer.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        ''' ############## Increment Button  ############## '''
        self.MainApp.Button_right.clicked.connect(self.label_cinemaAnswer.clear)
        self.MainApp.Button_right.clicked.connect(
            lambda: self.label_cinemaQuestion.clear() if self.MainApp.Video_Window.video_finished else None)

        ''' ############## Decrement Button  ############## '''
        self.MainApp.Button_left.clicked.connect(self.label_cinemaAnswer.clear)
        self.MainApp.Button_left.clicked.connect(
            lambda: self.label_cinemaQuestion.clear() if self.MainApp.Video_Window.video_finished else None)

        ''' ############## Material List  ############## '''
        self.MainApp.listWidget_material.itemClicked.connect(self.label_cinemaAnswer.clear)
        self.MainApp.listWidget_material.itemClicked.connect(
            lambda: self.label_cinemaQuestion.clear() if self.MainApp.Video_Window.video_finished else None)

        ''' ############## Team Points  ############## '''
        self.MainApp.spinBox_bluepoints.textChanged.connect(self.label_bluePoints.setText)
        self.MainApp.spinBox_redpoints.textChanged.connect(self.label_redPoints.setText)

        # self.label_picture.setPixmap(QPixmap("4k.jpg"))
        self.threadpool = QThreadPool()

        self.current_time = 20
        self.ready_time = 3
        self.ready_before = False

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(lambda: self.start_timer())
        self.time_signal.connect(self.label_time.setText)

        self.MainApp.Button_bothteams.pressed.connect(self.timer.start)
        self.MainApp.Button_bothteams.pressed.connect(lambda: self.countdown_time(20))

        self.MainApp.Button_redteam.pressed.connect(self.timer.start)
        self.MainApp.Button_redteam.pressed.connect(lambda: self.countdown_time(20))

        self.MainApp.Button_blueteam.pressed.connect(self.timer.start)
        self.MainApp.Button_blueteam.pressed.connect(lambda: self.countdown_time(20))

        self.MainApp.Button_bothindividual.pressed.connect(self.timer.start)
        self.MainApp.Button_bothindividual.pressed.connect(lambda: self.countdown_time(20))

        self.MainApp.Button_individual.pressed.connect(self.timer.start)
        self.MainApp.Button_individual.pressed.connect(lambda: self.countdown_time(45, False))

        self.MainApp.Button_reset.pressed.connect(self.stop_timer)

        # self.shortcut = QtGui.QShortcut(QtGui.QKeySequence(Qt.Key.ALT | Qt.Key.Key_F), self)
        self.shortcut = QtGui.QShortcut(QtGui.QKeySequence(QObject.tr("Alt+f")), self)
        self.shortcut.activated.connect(self.Cinema_fullscreen)

    def Cinema_fullscreen(self):
        if self.isVisible():
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
                self.setFixedSize(self.width(), self.height())

    def countdown_time(self, time, ready_before=True, ready_time=3):
        self.label_time.setText(str(time))
        self.current_time = time + ready_time if ready_before else time
        self.ready_time = ready_time if ready_before else 0

    def start_timer(self):
        self.current_time -= 1

        if self.ready_time == 0:
            self.time_signal.emit(str(self.current_time))
        else:
            self.ready_time -= 1

        if self.current_time == 0:
            Sound_Action.sound_timeout()
            self.stop_timer()
            self.time_signal.emit('')
            self.MainApp.toggle_Buttons(True)

            # print('Done')
        else:
            if 0 < self.current_time < 5:
                Sound_Action.sound_time4()

            self.timer.start()
            # print(f'time : {self.current_time}')

    def stop_timer(self):
        self.timer.stop()
        self.current_time = 0
        self.MainApp.Serial_Window.serial.send_data('N')
        print('STOP!!!')
        self.label_time.setText('')
