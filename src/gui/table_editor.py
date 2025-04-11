import os
import re
import shutil

import pandas as pd
from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QTableWidgetItem, QFileDialog

from src.core import data_handler
from src.core.json_loader import read_json

from src.widgets.table_button import TableButton
from src.widgets.table_combo import TableCombo

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


class TableApp(QWidget):
    def __init__(self, parent=None):
        super(TableApp, self).__init__(parent)

        ''' ############## Load the uit of the GUI ############## '''
        self.MainApp = parent

        ''' ############## table list  ############## '''
        self.data_widget_tables = {'Geography': self.MainApp.tableWidget_data_Geography,
                                   'Historical': self.MainApp.tableWidget_data_Historical,
                                   'Literature': self.MainApp.tableWidget_data_Literature,
                                   'Science': self.MainApp.tableWidget_data_Science,
                                   'General': self.MainApp.tableWidget_data_General,
                                   'Sports': self.MainApp.tableWidget_data_Sports,
                                   'Technology': self.MainApp.tableWidget_data_Technology,
                                   'Brain': self.MainApp.tableWidget_data_Brain,
                                   'Cinema': self.MainApp.tableWidget_data_Cinema,
                                   'Songs': self.MainApp.tableWidget_data_Songs,
                                   'Sites': self.MainApp.tableWidget_data_Sites,
                                   'Promptitude': self.MainApp.tableWidget_data_Promptitude,
                                   'Pressure': self.MainApp.tableWidget_data_Pressure,
                                   'Penalties': self.MainApp.tableWidget_data_Penalties,
                                   'Luck_Wheel': self.MainApp.tableWidget_data_Luck_Wheel,
                                   }

        ''' ############## Initializing Dataframe ############## '''
        self.material_buttons_pos = []
        self.readFolder(data_dir)
        self.MainApp.data_df = data_handler.read_data(os.path.join(data_dir, data_file))
        self.update_table()

        ''' ############## Name of current material tab selected  ############## '''
        self.Current_DataTab = Ar2Eng_material[
            self.MainApp.tabWidget_data.tabText(self.MainApp.tabWidget_data.currentIndex())]

        ''' ############## Open Directory  ############## '''
        self.MainApp.Button_import.clicked.connect(self.importData)

        ''' ############## Export Directory  ############## '''
        self.MainApp.Button_export.clicked.connect(self.exportData)

        self.MainApp.Button_save.clicked.connect(self.saveData)

        ''' ############## Table font  ############## '''
        self.Table_Font = QtGui.QFont()
        self.Table_Font.setPointSize(20)
        self.Table_Font.setBold(True)
        self.Table_Font.setWeight(75)

    def readFolder(self, folder_path):

        dir_list = os.listdir(folder_path)

        file_paths = [os.path.join(folder_path, file) for file in dir_list if
                      file.split('.')[-1] in img_types + song_types]

        # try:
        if len(file_paths) != 0:

            pos_list = [re.findall('\[.+\]', file)[-1].replace('[', '').replace(']', '').split(',')[:-1] for file in
                        file_paths if '[' in file or ']' in file or ',' in file]

            self.material_buttons_pos = {mat[0]: [] for mat in pos_list}

            for list in pos_list:
                material = list[0]
                self.material_buttons_pos[material].append(int(list[1]))
        # except:
        #     pass

    def saveData(self):
        writer = pd.ExcelWriter(os.path.join(data_dir, data_file), engine='xlsxwriter')
        for material in En_materials_list:
            self.MainApp.data_df[material].to_excel(writer, sheet_name=material)
        writer.save()

    def exportData(self):

        dialog = QFileDialog(parent=self,
                             caption='Select Data Folder',
                             directory=os.path.expanduser("~"))

        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        folder_directory = dialog.getSaveFileName(self)[0]

        if folder_directory != '':
            self.saveData()
            if os.path.exists(folder_directory):
                dlg = QMessageBox(self)
                dlg.setStyleSheet("font-size: 15px;background-color: rgba(0, 0, 0, 75);")
                dlg.setIcon(QMessageBox.Icon.Warning)
                dlg.setWindowTitle("Genius")
                text = f"Genius warning:  Cannot create a file when that file already exists '{folder_directory}"
                dlg.setText(text)
                button = dlg.exec()
                button = QMessageBox.StandardButton(button)
                if button == QMessageBox.StandardButton.Ok:
                    return
            else:
                shutil.copytree(data_dir, folder_directory)

    def importData(self):

        # https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qfiledialog.html?highlight=qfiledialog#Option
        folder_directory = QFileDialog.getExistingDirectory(parent=self, caption='Select Data Folder',
                                                            directory=os.path.expanduser("~"))
        if folder_directory != '':
            self.readFolder(folder_directory)
            self.clearTables()

            dir_files = os.listdir(folder_directory)
            excel_files = [file for file in dir_files if file.endswith('.xlsx') or file.endswith('.xls')]
            excel_files_path = [os.path.join(folder_directory, file) for file in excel_files]
            no_excel = len(excel_files)

            dlg = QMessageBox(self)
            dlg.setStyleSheet("font-size: 15px;background-color: rgba(0, 0, 0, 75);")
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.setWindowTitle("Genius")

            if no_excel > 1 or no_excel == 0:
                text = f"Genius warning: There is more than one excel file in the directory " \
                       f"\n{excel_files}\nPlease be sure to add only one file." if no_excel > 1 \
                    else "Genius warning: There no excel files in the directory \nPlease be sure to put one."
                dlg.setText(text)
                button = dlg.exec()
                button = QMessageBox.StandardButton(button)
                if button == QMessageBox.StandardButton.Ok:
                    return
            else:
                Excel_path = excel_files_path[0]
                Excel_name = os.path.basename(Excel_path)
                xl = pd.ExcelFile(Excel_path)
                sheet_not_exist = []
                for material in En_materials_list:
                    if material not in xl.sheet_names:  # see all sheet names
                        sheet_not_exist.append(material)
                if len(sheet_not_exist) > 0:
                    text = f"Genius warning: Sheets {sheet_not_exist} is missing please be sure to add them"
                    dlg.setText(text)
                    button = dlg.exec()
                    button = QMessageBox.StandardButton(button)
                    if button == QMessageBox.StandardButton.Ok:
                        return
                else:
                    shutil.rmtree(data_dir)
                    shutil.copytree(folder_directory, data_dir)
                    os.rename(os.path.join(data_dir, Excel_name), os.path.join(data_dir, data_file))
                    self.MainApp.data_df = data_handler.read_data(os.path.join(data_dir, data_file))
                    self.update_table()

    def update_table(self):

        for En_material in En_materials_list:
            no_row = len(self.MainApp.data_df[En_material])

            self.data_widget_tables[En_material].setRowCount(no_row)

            no_col = len(self.MainApp.data_df[En_material].columns)

            self.data_widget_tables[En_material].setColumnCount(no_col)

            header_names = list(self.MainApp.data_df[En_material].columns)

            self.data_widget_tables[En_material].setHorizontalHeaderLabels(header_names)

            # print(re.findall('\[.+\]',img_new_name)[-1].replace('[','').replace(']',''))

            for row in range(len(self.MainApp.data_df[En_material])):

                for col in range(len(self.MainApp.data_df[En_material].columns)):

                    if self.MainApp.data_df[En_material].loc[row, 'type'] in ['i', 's'] and header_names[col] == 'que':
                        found = False
                        # print(self.material_buttons_pos)
                        # print(row)
                        if En_material in self.material_buttons_pos and row in self.material_buttons_pos[En_material]:
                            # self.MainApp.data_df[En_material].at[row, 'que'] = self.data_paths[(En_material, row)]
                            found = True

                        btn = TableButton(parent=self,
                                          text=Type_names[self.MainApp.data_df[En_material].at[row, 'type']],
                                          objectName=f'Button_{En_material}_{row}', found=found)

                        self.data_widget_tables[En_material].setCellWidget(row, col, btn)

                    else:
                        item = QTableWidgetItem(str(self.MainApp.data_df[En_material].iat[row, col]))
                        self.data_widget_tables[En_material].setItem(row, col, item)

                    if header_names[col] == 'type':
                        combo = TableCombo(parent=self,
                                           items=['Words', 'Image', 'Song'],
                                           objectName=f'Combo_{En_material}_{row}')

                        data_type = self.MainApp.data_df[En_material].at[row, 'type']
                        combo.setCurrentText(Type_names[data_type])
                        self.data_widget_tables[En_material].setCellWidget(row, col, combo)

            self.data_widget_tables[En_material].cellChanged.connect(self.update_df)
            self.data_widget_tables[En_material].resizeColumnsToContents()
            self.data_widget_tables[En_material].resizeRowsToContents()

    def clearTables(self):
        for table in self.data_widget_tables.values():
            table.clearContents()

    def update_df(self, row, col):
        try:
            material = '_'.join(self.MainApp.tabWidget_data.currentWidget().objectName().split('_')[2:])
            self.MainApp.data_df[material].iat[row, col] = str(self.data_widget_tables[material].item(row, col).text())
            self.MainApp.data_len = len(self)
        except:
            pass

    def __len__(self):
        index = self.MainApp.data_df[self.MainApp.material].index[
            # self.MainApp.data_df[self.MainApp.material]['ans'].isna()].tolist()
            self.MainApp.data_df[self.MainApp.material]['ans'] == ''].tolist()
        return index[0]
