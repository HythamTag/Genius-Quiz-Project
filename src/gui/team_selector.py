import os

import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QFileDialog
from src.core import mqtt_control


# Teams_Names = pd.read_excel()


class TeamApp(QWidget):
    def __init__(self, parent=None):
        super(TeamApp, self).__init__(parent)

        ''' ############## Load the uit of the GUI ############## '''
        self.MainApp = parent

        ''' ############## Initializing Dataframe ############## '''
        self.Team_Names = None

        topics_R = ["Red/R", "Red/R1", "Red/R2", "Red/R3", "Red/R4"]
        topics_B = ["Blue/B", "Blue/B1", "Blue/B2", "Blue/B3", "Blue/B4"]
        client_id_R = ['Team-R', 'Team-R1', 'Team-R2', 'Team-R3', 'Team-R4']
        client_id_B = ['Team-B', 'Team-B1', 'Team-B2', 'Team-B3', 'Team-B4']

        self.server_R = [mqtt_control.MqttServer(clien_id, topic) for clien_id, topic in zip(client_id_R, topics_R)]
        self.server_B = [mqtt_control.MqttServer(clien_id, topic) for clien_id, topic in zip(client_id_B, topics_B)]

        for server_R, server_B in zip(self.server_R, self.server_B):
            server_R.run()
            server_B.run()

        self.comboBoxes_R = [self.MainApp.comboBox_R1, self.MainApp.comboBox_R2, self.MainApp.comboBox_R3, self.MainApp.comboBox_R4]
        self.comboBoxes_B = [self.MainApp.comboBox_B1, self.MainApp.comboBox_B2, self.MainApp.comboBox_B3, self.MainApp.comboBox_B4]

        self.MainApp.Button_team_browse.clicked.connect(self.importData)

        self.MainApp.comboBox_R.currentIndexChanged.connect(self.updateData)

        self.MainApp.comboBox_B.currentIndexChanged.connect(self.updateData)

        self.MainApp.Button_team_refresh.clicked.connect(self.refresh)
        self.MainApp.Button_team_update.clicked.connect(self.update_screens)
        self.MainApp.Button_team_clear.clicked.connect(self.clear_screens)

    def importData(self):
        # https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qfiledialog.html?highlight=qfiledialog#Option

        file_directory = QFileDialog.getOpenFileNames(parent=self, caption='Select Teams Excel File',
                                                      directory=os.path.expanduser("~"), filter="*.xlsx;;*.xls")
        if len(file_directory[0]) != 0:
            self.file_directory = file_directory[0][0]

            self.MainApp.Button_team_refresh.setEnabled(True)
            self.MainApp.Button_team_update.setEnabled(True)
            self.MainApp.Button_team_clear.setEnabled(True)

            self.refresh()

    def refresh(self):
        print(self.file_directory)
        self.Teams_df = pd.read_excel(self.file_directory, index_col=None)
        self.Teams_Name = self.Teams_df.columns.to_list()

        prev_R = self.MainApp.comboBox_R.currentText()
        prev_B = self.MainApp.comboBox_B.currentText()

        self.MainApp.comboBox_R.clear()
        self.MainApp.comboBox_B.clear()

        self.MainApp.comboBox_R.addItems(self.Teams_Name)
        self.MainApp.comboBox_B.addItems(self.Teams_Name)

        if prev_R in self.Teams_Name:
            self.MainApp.comboBox_R.setCurrentText(prev_R)

        if prev_B in self.Teams_Name:
            self.MainApp.comboBox_B.setCurrentText(prev_B)

        self.updateData()

    def updateData(self):

        current_R_Team = self.MainApp.comboBox_R.currentText()
        if current_R_Team != '' and current_R_Team in self.Teams_df.columns:
            Team_R_Names_list = self.Teams_df[current_R_Team].to_list()
            Team_R_Names_list = [x for x in Team_R_Names_list if str(x) != 'nan']
            self.clearCombo('r')
            for index, combo_box in enumerate(self.comboBoxes_R):
                combo_box.addItems(Team_R_Names_list)
                combo_box.setCurrentText(Team_R_Names_list[index])
        else:
            self.clearCombo()

        current_B_Team = self.MainApp.comboBox_B.currentText()
        if current_B_Team != '' and current_B_Team in self.Teams_df.columns:
            Team_B_Names_list = self.Teams_df[current_B_Team].to_list()
            Team_B_Names_list = [x for x in Team_B_Names_list if str(x) != 'nan']
            self.clearCombo('b')
            for index, combo_box in enumerate(self.comboBoxes_B):
                combo_box.addItems(Team_B_Names_list)
                combo_box.setCurrentText(Team_B_Names_list[index])
        else:
            self.clearCombo()

    def clearCombo(self, team='a'):

        if team == 'r':
            for combo_box in self.comboBoxes_R:
                combo_box.clear()
        if team == 'b':
            for combo_box in self.comboBoxes_B:
                combo_box.clear()
        else:
            for combo_box in self.comboBoxes_R:
                combo_box.clear()
            for combo_box in self.comboBoxes_B:
                combo_box.clear()

    def update_screens(self):

        R_current_text = self.MainApp.comboBox_R.currentText()
        B_current_text = self.MainApp.comboBox_B.currentText()

        if len(R_current_text.split()) > 1:
            R_current_text = R_current_text.split()[0] + ' ' + R_current_text.split()[1]

        if len(B_current_text.split()) > 1:
            B_current_text = B_current_text.split()[0] + ' ' + B_current_text.split()[1]

        self.server_R[0].publish(R_current_text)
        self.server_B[0].publish(B_current_text)

        for server_R, server_B, combo_R, combo_B in zip(self.server_R[1:], self.server_B[1:], self.comboBoxes_R, self.comboBoxes_B):
            R_current_text = combo_R.currentText()
            B_current_text = combo_B.currentText()
            if len(R_current_text.split()) > 1:
                R_current_text = R_current_text.split()[0] + ' ' + R_current_text.split()[1]
            if len(B_current_text.split()) > 1:
                B_current_text = B_current_text.split()[0] + ' ' + B_current_text.split()[1]

            server_R.publish(R_current_text)
            server_B.publish(B_current_text)

    def clear_screens(self):
        self.server_R[0].publish('')
        self.server_B[0].publish('')

        for server_R, server_B, combo_R, combo_B in zip(self.server_R[1:], self.server_B[1:], self.comboBoxes_R, self.comboBoxes_B):
            server_R.publish('')
            server_B.publish('')
