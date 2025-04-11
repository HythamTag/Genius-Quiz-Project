import cv2
import numpy as np
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from src.core.sound_engine import Sound_Action


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    finished = pyqtSignal(bool)

    def __init__(self, path):
        super().__init__()
        self._run_flag = True
        self.path = path
        self.finished.emit(False)


    def run(self):
        self.finished.emit(False)
        self.video = cv2.VideoCapture(self.path)
        Sound_Action.sound_Background(True)
        fps = int(self.video.get(cv2.CAP_PROP_FPS))
        millisecs = int(1000.0 / fps)

        while self._run_flag:
            ret, cv_img = self.video.read()

            if ret:
                self.change_pixmap_signal.emit(cv_img)
            elif not ret:
                break
            if cv2.waitKey(millisecs) & 0x7F == ord('q'):
                break

        self.finished.emit(True)
        self.video.release()
        self.quit()

    def stop(self):
        try:
            self.finished.emit(True)
            self._run_flag = False
            # self.video.release()
            self.quit()
        except:
            pass


class VideoApp(QMainWindow):
    def __init__(self, parent=None):
        super(VideoApp, self).__init__(parent)

        ''' ############## Load the uit of the GUI ############## '''
        self.MainApp = parent

        self.MainApp.Button_movie.setCheckable(True)
        # self.MainApp.Button_movie.clicked.connect(self.MainApp.Button_movie.setCheckable)
        self.MainApp.Button_movie.clicked.connect(self.MainApp.Button_movie.setChecked)

        self.MainApp.Button_movie.clicked.connect(self.run_video)
        # self.MainApp.Button_left.clicked.connect(self.stop_video)
        # self.MainApp.Button_right.clicked.connect(self.stop_video)
        # self.MainApp.listWidget_material.itemClicked.connect(self.stop_video)
        self.MainApp.Button_reset.clicked.connect(self.stop_video)

        path = 'src/resources/ui/Resources/Movies/' + 'Geography' + '.avi'
        # create the video capture thread
        self.thread = VideoThread(path)
        
        self.video_finished = True;

    def stop_video(self):
        try:
            self.thread.stop()
            Sound_Action.sound_Background(False)
            self.MainApp.Cinema_Window.label_cinemaQuestion.clear()
        except:
            pass

    def run_video(self):
        rule1 = self.MainApp.Button_movie.isChecked()
        rule2 = self.MainApp.Button_showQuestion.isChecked()
        if rule1 and not rule2:
            self.MainApp.toggle_Buttons(False)
            self.MainApp.Button_showQuestion.setEnabled(False)
            self.MainApp.Cinema_Window.label_cinemaAnswer.setSizePolicy(QSizePolicy.Policy.Preferred,
                                                                        QSizePolicy.Policy.Ignored)
            # updating the video path
            path = 'src/resources/ui/Resources/Movies/' + self.MainApp.material + '.avi'
            # create the video capture thread
            self.thread = VideoThread(path)
            # connect its signal to the update_image slot
            self.thread.change_pixmap_signal.connect(self.update_image)
            # connect its signal to the cloesEvent slot
            self.thread.finished.connect(self.closeEvent)
            # start the thread
            self.thread.start()
        elif rule2:
            self.MainApp.Button_movie.setChecked(False)
            pass
        else:
            self.stop_video()
            self.MainApp.toggle_Buttons(True)
            self.MainApp.Button_showQuestion.setEnabled(True)

    def closeEvent(self, finished):
        self.video_finished = finished
        print(finished)
        if finished:
            self.MainApp.toggle_Buttons(True)
            self.MainApp.Button_showQuestion.setEnabled(True)
            self.MainApp.Button_movie.setChecked(False)
            self.MainApp.Cinema_Window.MainApp.Cinema_Window.label_cinemaQuestion.clear()
            pass

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.MainApp.Cinema_Window.MainApp.Cinema_Window.label_cinemaQuestion.setPixmap(qt_img)


    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)

        w = min(convert_to_Qt_format.width(),
                self.MainApp.Cinema_Window.label_cinemaQuestion.width() -
                4 * self.MainApp.Cinema_Window.label_cinemaQuestion.lineWidth())
        h = min(convert_to_Qt_format.height(), self.MainApp.Cinema_Window.label_cinemaQuestion.maximumHeight(),
                self.MainApp.Cinema_Window.frame_Top.height() -
                4 * self.MainApp.Cinema_Window.frame_Top.lineWidth())
        Q_image = convert_to_Qt_format.scaled(w, h, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                                              transformMode=Qt.TransformationMode.SmoothTransformation)
        return QtGui.QPixmap.fromImage(Q_image)
