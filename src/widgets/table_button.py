import os
import shutil

from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QFileDialog

from src.core.json_loader import read_json
from src.core.sound_engine import Sound_Action

img_types = ['png', 'jpg', 'bmp']
song_types = ['mp3', 'ogg', 'wav', 'm4a']

''' ############## Material list  ############## '''
Ar2Eng_material = read_json('src/resources/meterial_names/Ar2En_materials.json')
En_materials_list = read_json('src/resources/meterial_names/EN_materials.json')
Ar_materials_list = read_json('src/resources/meterial_names/Ar_materials.json')
En2Ar_material = read_json('src/resources/meterial_names/En2Ar_materials.json')

Type_names = read_json('src/resources/meterial_names/Type_name.json')
data_path = read_json('src/resources/meterial_names/Data_path.json')
data_dir = list(data_path.keys())[0]
data_file = data_path[data_dir]




class TableButton(QPushButton):
    def __init__(self, parent, text='', objectName=None, found=False):
        super().__init__(parent)

        self.TableApp = parent

        if found:
            self.setStyleSheet('font-size: 22px;border-radius: 40px;background-color: rgba(0, 255, 0, 75);')
        else:
            self.setStyleSheet('font-size: 22px;background-color: rgba(255, 0, 0, 75);')

        self.setText(text)

        self.setObjectName(objectName)

        self.clicked.connect(self.ok)

    def ok(self):

        material = '_'.join(self.TableApp.MainApp.tabWidget_data.currentWidget().objectName().split('_')[2:])
        row = self.TableApp.data_widget_tables[material].currentRow()
        col = self.TableApp.MainApp.data_df[material].columns.get_loc('que')

        file_type = "Image Files (*.png *.jpg *.bmp)" \
            if self.text() == 'Image' \
            else "Sound Files (*.mp3 *.ogg *.wav *.m4a) "

        old_file_path = \
            QFileDialog.getOpenFileName(self, "Select Excel file to import", os.path.expanduser("~"), file_type)[0]

        if old_file_path != '':
            file_name = os.path.basename(old_file_path)
            file_end = file_name.split(r".")[-1]
            # file_new_name = f'{"".join(file_name.split(r".")[:-1])}_[{material},{row},{col}].{file_end}'
            file_new_name = f'[{material},{row},{col}].{file_end}'
            new_file_path = os.path.join(data_dir, file_new_name)

            file_paths = [os.path.join(data_dir, file) for file in os.listdir(data_dir)
                          if file.split('.')[-1] in img_types + song_types]

            for file in file_paths:
                if f'[{material},{row},{col}]' in file:
                    os.remove(file)

            if self.text() == 'Song':
                try:
                    print(old_file_path)
                    Sound_Action.play_song(old_file_path)
                    Sound_Action.stop_song()
                except:
                    # print("Bad Format")
                    dlg = QMessageBox(self)
                    dlg.setStyleSheet("font-size: 15px;background-color: rgba(0, 0, 0, 75);")
                    dlg.setIcon(QMessageBox.Icon.Warning)
                    dlg.setWindowTitle("Genius")
                    dlg.setText(f"Genius warning: Unable to import {old_file_path} "
                                f"as a sound file (bad format or not readable)")
                    button = dlg.exec()
                    button = QMessageBox.StandardButton(button)
                    if button == QMessageBox.StandardButton.Ok:
                        pass
                    return

            shutil.copy(old_file_path, new_file_path)
            self.TableApp.MainApp.data_df[material].iat[row, col] = os.path.join(data_dir, file_new_name)
            self.setStyleSheet('font-size: 22px;border-radius: 40px;background-color: rgba(0, 255, 0, 75);')
            # print(row, col, material)
            # print(tabulate(self.TableApp.MainApp.data_df[material], headers='keys', tablefmt='psql'))

