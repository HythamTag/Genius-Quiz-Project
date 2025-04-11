
import signal
import sys

from PyQt6 import QtGui
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication

import qdarktheme
from src.core import serial_control
from src.core.json_loader import read_json
from src.core.sound_engine import Sound_Action
from src.gui import cinema_screen, table_editor, video_player, team_selector

signal.signal(signal.SIGINT, signal.SIG_DFL)

''' ############## Material list  ############## '''
En_materials_list = read_json('src/resources/meterial_names/EN_materials.json')
Ar_materials_list = read_json('src/resources/meterial_names/Ar_materials.json')
En2Ar_material = read_json('src/resources/meterial_names/En2Ar_materials.json')
Ar2Eng_material = read_json('src/resources/meterial_names/Ar2En_materials.json')
Type_names = read_json('src/resources/meterial_names/Type_name.json')
Serial_char = read_json('src/resources/meterial_names/Serial_char.json')

class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        # self.setAttribute(Qt.WindowType.WA_TranslucentBackground, True)

        ''' ############## Load the uit of the GUI ############## '''
        uic.loadUi('src/resources/ui/Mainui_updated.ui', self)

        ''' ############## Load the uit of the GUI ############## '''
        self.Cinema_Window = cinema_screen.CinemaApp(self)
        self.Serial_Window = serial_control.SerialApp(self)
        self.Table_Window = table_editor.TableApp(self)
        self.Video_Window = video_player.VideoApp(self)
        self.Teams_Window = team_selector.TeamApp(self)
        self.Button_cinema.clicked.connect(lambda: self.Cinema_Window.show())


        ''' ############## Question Button  ############## '''
        self.Button_showQuestion.setCheckable(True)
        self.Button_showQuestion.clicked.connect(self.Button_showQuestion.setChecked)
        self.Button_showQuestion.clicked.connect(self.Button_showAnswer.setCheckable)
        self.Button_showQuestion.clicked.connect(self.Button_showAnswer.setEnabled)
        self.Button_showQuestion.clicked.connect(self.Show_Question)

        ''' ############## Answer Button  ############## '''
        self.Button_showAnswer.setCheckable(False)
        self.Button_showAnswer.setEnabled(False)
        self.Button_showAnswer.clicked.connect(self.Button_showAnswer.setChecked)
        self.Button_showAnswer.clicked.connect(self.Show_Answer)

        ''' ############## Increment Button  ############## '''
        self.Button_right.clicked.connect(lambda: self.Button_showQuestion.setChecked(False))
        self.Button_right.clicked.connect(lambda: self.Button_showAnswer.setChecked(False))
        self.Button_right.clicked.connect(lambda: self.Button_showAnswer.setCheckable(False))
        self.Button_right.clicked.connect(lambda: self.Button_showAnswer.setEnabled(False))
        self.Button_right.clicked.connect(self.label_question.clear)
        self.Button_right.clicked.connect(self.label_answer.clear)
        self.Button_right.clicked.connect(Sound_Action.stop_song)
        self.Button_right.clicked.connect(self.increment)

        ''' ############## Decrement Button  ############## '''
        self.Button_left.clicked.connect(lambda: self.Button_showQuestion.setChecked(False))
        self.Button_left.clicked.connect(lambda: self.Button_showAnswer.setChecked(False))
        self.Button_left.clicked.connect(lambda: self.Button_showAnswer.setCheckable(False))
        self.Button_left.clicked.connect(lambda: self.Button_showAnswer.setEnabled(False))
        self.Button_left.clicked.connect(self.label_question.clear)
        self.Button_left.clicked.connect(self.label_answer.clear)
        self.Button_left.clicked.connect(Sound_Action.stop_song)
        self.Button_left.clicked.connect(self.decrement)

        ''' ############## Material List  ############## '''
        self.listWidget_material.setCurrentRow(0)
        self.listWidget_material.itemClicked.connect(lambda: self.label_index.setText('1'))
        self.listWidget_material.itemClicked.connect(lambda: self.Button_showQuestion.setChecked(False))
        self.listWidget_material.itemClicked.connect(lambda: self.Button_showAnswer.setChecked(False))
        self.listWidget_material.itemClicked.connect(lambda: self.Button_showAnswer.setCheckable(False))
        self.listWidget_material.itemClicked.connect(lambda: self.Button_showAnswer.setEnabled(False))
        self.listWidget_material.itemClicked.connect(self.label_question.clear)
        self.listWidget_material.itemClicked.connect(self.label_answer.clear)
        self.Button_left.clicked.connect(Sound_Action.stop_song)
        self.listWidget_material.itemClicked.connect(self.update_material)
        self.pushButton_fullscreen.clicked.connect(self.fullscreen)

        ''' ############## Current Command ############## '''
        self.Current_Command = 0

        ''' ############## Current Material ############## '''
        self.material = Ar2Eng_material[self.listWidget_material.currentItem().text()]

        ''' ############## Current Material ############## '''
        self.data_len = len(self.Table_Window)

        ''' ############## Current Question Index ############## '''
        self.index = 1

        ''' ############## Current Question Type ############## '''
        self.type = str(self.data_df[self.material].at[self.index - 1, 'type'])

        ''' ############## current image ############## '''
        self.image = 0

        self.shortcut = QtGui.QShortcut(QtGui.QKeySequence(QObject.tr("Alt+f")), self)
        self.shortcut.activated.connect(self.fullscreen)

    def fullscreen(self):
        if self.isVisible():
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
                self.setFixedSize(self.width(), self.height())

    def Show_Question(self):
        self.update_data()

    def Show_Answer(self):
        Question_Checked = self.Button_showQuestion.isChecked() is True
        Answer_Checked = self.Button_showAnswer.isChecked() is True

        if Question_Checked and Answer_Checked:

            if self.type == 'i':
                self.Cinema_Window.label_cinemaAnswer.clear()

                self.Cinema_Window.label_cinemaAnswer.setSizePolicy(QSizePolicy.Policy.Preferred,
                                                                    QSizePolicy.Policy.Ignored)

                self.label_answer.setText(self.lineEdit_answer.text())
                self.label_answer.setScaledContents(True)

                self.Cinema_Window.label_cinemaAnswer.setText(self.lineEdit_answer.text())
                self.Cinema_Window.label_cinemaAnswer.setAlignment(Qt.AlignmentFlag.AlignHCenter)

                self.update_Cinema_Image()

            else:
                self.label_answer.setText(self.lineEdit_answer.text())
                self.label_answer.setScaledContents(True)

                self.Cinema_Window.label_cinemaAnswer.setText(self.lineEdit_answer.text())
                self.Cinema_Window.label_cinemaAnswer.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        else:
            self.label_answer.clear()
            self.Cinema_Window.label_cinemaAnswer.clear()

            if self.type == 'i':
                self.update_Cinema_Image()

    def update_material(self):
        self.index = 1
        self.material = Ar2Eng_material[self.listWidget_material.currentItem().text()]
        self.data_len = len(self.Table_Window)
        self.type = str(self.data_df[self.material].at[self.index - 1, 'type'])

        self.lineEdit_answer.setText(str(self.data_df[self.material].at[self.index - 1, 'ans']))
        self.lineEdit_question.setText(str(self.data_df[self.material].at[self.index - 1, 'que']))

    def increment(self):
        if self.index + 1 <= self.data_len:
            self.index += 1
            self.type = str(self.data_df[self.material].at[self.index - 1, 'type'])

            question = str(self.data_df[self.material].at[self.index - 1, 'ans'])
            answer = str(self.data_df[self.material].at[self.index - 1, 'que'])

            self.lineEdit_answer.setText(str(question))
            self.lineEdit_question.setText(str(answer))
            self.label_index.setText(str(self.index))

    def decrement(self):
        if self.index - 1 >= 1:
            self.index -= 1
            self.type = str(self.data_df[self.material].at[self.index - 1, 'type'])
            question = str(self.data_df[self.material].at[self.index - 1, 'ans'])
            answer = str(self.data_df[self.material].at[self.index - 1, 'que'])

            self.lineEdit_answer.setText(str(question))
            self.lineEdit_question.setText(str(answer))
            self.label_index.setText(str(self.index))

    def update_data(self):
        Question_Checked = self.Button_showQuestion.isChecked() is True

        if self.type == 'w' and Question_Checked:

            self.Cinema_Window.label_cinemaAnswer.setSizePolicy(QSizePolicy.Policy.Preferred,
                                                                QSizePolicy.Policy.Expanding)

            self.Cinema_Window.label_cinemaAnswer.setScaledContents(True)

            self.label_question.setText(self.lineEdit_question.text())
            self.label_question.setScaledContents(True)

            self.Cinema_Window.label_cinemaQuestion.setText(self.lineEdit_question.text())
            self.Cinema_Window.label_cinemaQuestion.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        elif self.type == 'i' and Question_Checked:

            self.Cinema_Window.label_cinemaAnswer.setSizePolicy(QSizePolicy.Policy.Preferred,
                                                                QSizePolicy.Policy.Ignored)
            self.update_Main_Image()

            self.update_Cinema_Image()

        elif self.type == 's' and Question_Checked:

            self.Cinema_Window.label_cinemaAnswer.setSizePolicy(QSizePolicy.Policy.Preferred,
                                                                QSizePolicy.Policy.Expanding)

            Sound_Action.play_song(file_path=str(self.lineEdit_question.text()))

        elif Question_Checked is False:

            Sound_Action.stop_song()

            self.label_question.clear()
            self.label_answer.clear()

            self.Cinema_Window.label_cinemaQuestion.clear()
            self.Cinema_Window.label_cinemaAnswer.clear()

    def toggle_Buttons(self, condition):
        self.Button_bothteams.setEnabled(condition)
        self.Button_bothindividual.setEnabled(condition)
        self.Button_redteam.setEnabled(condition)
        self.Button_blueteam.setEnabled(condition)
        self.Button_individual.setEnabled(condition)
        self.Button_true.setEnabled(condition)
        self.Button_false.setEnabled(condition)
        self.Button_showAnswer.setEnabled(condition)
        self.Button_showChoice.setEnabled(condition)

    def update_Cinema_Image(self):
        # w = min(self.image.width(),
        #         self.Cinema_Window.label_cinemaQuestion.width() -
        #         4 * self.Cinema_Window.label_cinemaQuestion.lineWidth())
        #
        # h = min(self.image.height(), self.Cinema_Window.label_cinemaQuestion.maximumHeight(),
        #         self.Cinema_Window.frame_Top.height() -
        #         4 * self.Cinema_Window.frame_Top.lineWidth())

        w = self.Cinema_Window.label_cinemaQuestion.width() - 4 * self.Cinema_Window.label_cinemaQuestion.lineWidth()
        h = self.Cinema_Window.frame_Top.height() - 4 * self.Cinema_Window.frame_Top.lineWidth()

        new_image = self.image.scaled(w, h, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                                      transformMode=Qt.TransformationMode.SmoothTransformation)

        self.Cinema_Window.label_cinemaQuestion.setPixmap(new_image)
        self.Cinema_Window.label_cinemaQuestion.setScaledContents(False)

    def update_Main_Image(self):
        self.image = QtGui.QPixmap(self.lineEdit_question.text())
        w = min(self.image.width(), self.label_question.maximumWidth() -
                4 * self.label_question.lineWidth())
        h = min(self.image.height(), self.label_question.maximumHeight(), self.height() // 6)
        new_image = self.image.scaled(w, h, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                                      transformMode=Qt.TransformationMode.SmoothTransformation)
        self.label_question.setPixmap(new_image)
        self.label_question.setScaledContents(False)


def main():
    app = QApplication(sys.argv)
    myapp = MyApp()
    app.setStyleSheet(qdarktheme.load_stylesheet())
    myapp.show()
    app.exec()


if __name__ == '__main__':
    main()

