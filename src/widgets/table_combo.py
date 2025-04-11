from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QTableWidgetItem

from src.core.json_loader import read_json
from src.widgets.table_button import TableButton


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

class TableCombo(QComboBox):
    def __init__(self, parent, items=None, objectName=None):
        super().__init__(parent)
        self.TableApp = parent

        # setting the font of combo box
        self.setStyleSheet('font-size: 22px')

        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

        # adding list of items to combo box
        self.addItems(items)

        # setting the object name of the combo box
        self.setObjectName(objectName)

        self.currentTextChanged.connect(self.getComboValue)

    def getComboValue(self, text):
        material = '_'.join(self.TableApp.MainApp.tabWidget_data.currentWidget().objectName().split('_')[2:])

        row = self.TableApp.data_widget_tables[material].currentRow()
        col = self.TableApp.MainApp.data_df[material].columns.get_loc('que')

        if row >= 0:
            self.TableApp.MainApp.data_df[material].at[row, 'type'] = Type_names[text]

            # print(tabulate(self.TableApp.MainApp.data_df[material], headers='keys', tablefmt='psql'))
            if text == 'Words':
                self.TableApp.data_widget_tables[material].removeCellWidget(row, col)
                text = QTableWidgetItem(self.TableApp.MainApp.data_df[material].iat[row, col])
                self.TableApp.data_widget_tables[material].setItem(row, col, text)
            else:
                self.TableApp.data_widget_tables[material].setItem(row, col, QTableWidgetItem(''))
                btn = TableButton(parent=self.TableApp,
                                  text=self.currentText(),
                                  objectName=f'Button_{material}_{row}')
                self.TableApp.data_widget_tables[material].setCellWidget(row, col, btn)


    def wheelEvent(self, ev):
        # 31 here crossponds to mouse scroll
        # https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtcore/qevent.html?highlight=qevent#QEvent
        if ev.type() == QtCore.QEvent.registerEventType(31):
            ev.ignore()

