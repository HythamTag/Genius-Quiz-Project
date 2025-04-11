import time
from threading import Thread, Event

import serial
import serial.tools.list_ports
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from src.core.json_loader import read_json
from src.core.sound_engine import Sound_Action

Serial_char = read_json('src/resources/meterial_names/Serial_char.json')


class SerialApp(QMainWindow):
    time_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SerialApp, self).__init__(parent)

        ''' ############## Load the uit of the GUI ############## '''
        self.MainApp = parent

        ''' ############## grab object of class customSerial()  ############## '''
        self.serial = customSerial()

        ''' ############## Add BaudRates to Combobox  ############## '''
        self.MainApp.comboBox_baudrate.addItems(self.serial.baudratesDIC.keys())
        self.MainApp.comboBox_baudrate.setCurrentText('9600')
        self.serial.update_ports()

        ''' ############## Serial Port Events  ############## '''
        self.MainApp.Button_port.clicked.connect(self.update_ports)
        self.MainApp.Button_connect.clicked.connect(self.connect_serial)
        self.MainApp.Button_send.clicked.connect(self.send_data)
        self.MainApp.Button_clean.clicked.connect(self.clear_terminal)
        self.serial.data_available.connect(self.update_terminal)

        self.Current_Command = ''

        ''' ############## Both Teams  ############## '''
        self.MainApp.Button_bothteams.pressed.connect(lambda: self.MainApp.toggle_Buttons(False))
        self.MainApp.Button_bothteams.pressed.connect(lambda: self.serial.send_data('A'))
        self.MainApp.Button_bothteams.pressed.connect(lambda: Sound_Action.sound_Start20())

        ''' ############## Red Teams  ############## '''
        self.MainApp.Button_redteam.pressed.connect(lambda: self.MainApp.toggle_Buttons(False))
        self.MainApp.Button_redteam.pressed.connect(lambda: self.serial.send_data('R'))
        self.MainApp.Button_redteam.pressed.connect(lambda: Sound_Action.sound_Start20())

        ''' ############## Blue Teams  ############## '''
        self.MainApp.Button_blueteam.pressed.connect(lambda: self.MainApp.toggle_Buttons(False))
        self.MainApp.Button_blueteam.pressed.connect(lambda: self.serial.send_data('B'))
        self.MainApp.Button_blueteam.pressed.connect(lambda: Sound_Action.sound_Start20())

        ''' ############## Both Individuals  ############## '''
        self.MainApp.Button_bothindividual.pressed.connect(lambda: self.MainApp.toggle_Buttons(False))
        self.MainApp.Button_bothindividual.pressed.connect(lambda: self.serial.send_data('I'))
        self.MainApp.Button_bothindividual.pressed.connect(lambda: Sound_Action.sound_Start20())

        ''' ############## One Individual  ############## '''
        self.MainApp.Button_individual.pressed.connect(lambda: self.MainApp.toggle_Buttons(False))
        self.MainApp.Button_individual.pressed.connect(lambda: self.serial.send_data('S'))
        self.MainApp.Button_individual.pressed.connect(lambda: Sound_Action.sound_Start45())

        ''' ############## True Button  ############## '''
        self.MainApp.Button_true.pressed.connect(lambda: self.MainApp.toggle_Buttons(True))
        self.MainApp.Button_true.pressed.connect(lambda: self.serial.send_data('S'))
        self.MainApp.Button_true.pressed.connect(lambda: Sound_Action.sound_Correct())

        ''' ############## False Button  ############## '''
        self.MainApp.Button_false.pressed.connect(lambda: self.MainApp.toggle_Buttons(True))
        self.MainApp.Button_false.pressed.connect(lambda: self.serial.send_data('S'))
        self.MainApp.Button_false.pressed.connect(lambda: Sound_Action.sound_Wrong())

        ''' ############## Reset Buttons  ############## '''
        self.MainApp.Button_reset.pressed.connect(lambda: self.MainApp.toggle_Buttons(True))
        self.MainApp.Button_reset.pressed.connect(lambda: self.serial.send_data('S'))

        ''' ############## Serial Data  ############## '''
        self.serial.data_available.connect(
            lambda data: self.MainApp.Button_true.setEnabled(True)
                         or self.MainApp.Button_false.setEnabled(True)
                         or self.MainApp.Button_showAnswer.setEnabled(True)
                         or self.MainApp.label_whopressed.setText(data)
                         or Sound_Action.sound_Buzzer()
                         or Sound_Action.stop_song()
            if data in Serial_char

            else self.MainApp.Button_showAnswer.setEnabled(False)
                 or self.MainApp.Button_showAnswer.setEnabled(False)
                 or self.MainApp.Button_showAnswer.setEnabled(False))

        self.serial.data_available.connect(lambda: self.serial.clear_data())

        self.serial.data_available.connect(
            lambda data: self.MainApp.Cinema_Window.stop_timer() if data in Serial_char
            else data)

    def update_terminal(self, data, condition='READ'):
        # Append the data read from port
        self.Current_Command = str(data)
        log_message = condition + ': ' + data
        self.MainApp.textBrowser_terminal.append(log_message)

    def connect_serial(self):

        # if the Connect Button condition is False and pressed
        if self.MainApp.Button_connect.isChecked():

            # self.textBrowser_terminal.setTextColour()

            # Reading the Port name from th Port combobox
            port = self.MainApp.comboBox_port.currentText()

            # Reading the Baud rate from th Baud rate combobox
            baud = self.MainApp.comboBox_baudrate.currentText()

            # writing to terminal about the connection
            if self.MainApp.comboBox_port.currentText() == "":
                log_message = f'No port selected.\n Refresh ports and then try again'
                self.MainApp.textBrowser_terminal.append(log_message)
                self.MainApp.Button_connect.setChecked(False)
            else:
                log_message = f'Attempting connection at\n{port}: {self.serial.PortDic[port]}'

                self.MainApp.textBrowser_terminal.append(log_message)

                # Connect to the serial with Port & Baudrate
                self.serial.connect_serial(port, baud)

                # If couldn't connect to the port
                if self.serial.serialPort.is_open is False:
                    log_message = f' Permission error connecting to port\n' \
                                  f'  Is there another application connecting to the port?\n' \
                                  f' Error opening selected port\n'

                    self.MainApp.textBrowser_terminal.append(log_message)

                    # set the Connect Button to False condition
                    self.MainApp.Button_connect.setChecked(False)
                else:
                    # writing to terminal about the connection
                    log_message = f' Connected to machine!\n'
                    self.MainApp.textBrowser_terminal.append(log_message)
                    time.sleep(1)
                    self.serial.send_data('S')
                    self.MainApp.label_connection.setText('Connected')
                    self.MainApp.label_connection.setStyleSheet('border-radius: 40px;'
                                                                'background-color: rgba(0, 255, 0, 75);')

        else:
            # if the Connect Button Condition is True and pressed then Disconnect
            self.serial.disconnect_serial()
            self.MainApp.label_connection.setText('No Connection')
            self.MainApp.label_connection.setStyleSheet('border-radius: 40px;'
                                                        'background-color: rgba(245, 0, 0, 75);')

    def send_data(self):
        # Read data from the input text box
        data = self.MainApp.lineEdit_input.text()
        if self.serial.serialPort.is_open:
            self.update_terminal(data=data, condition='SENT')
            # send data to the connected port
            self.serial.send_data(data)

    def update_ports(self):
        # read all available ports and update ports list
        self.serial.update_ports()

        # clear the ports combo box
        self.MainApp.comboBox_port.clear()

        # add the ports list to ports combo box
        self.MainApp.comboBox_port.addItems(self.serial.PortDic.keys())

    def clear_terminal(self):
        # clear the terminal
        self.MainApp.textBrowser_terminal.clear()

    def closeEvent(self, e):
        # event to disconnect serial when widget is closed
        # closeEvent is and an event handler that is called with the given event when
        # Qt receives a window close request for a top-level widget from the window system.
        self.serial.disconnect_serial()


class customSerial(QObject):
    data_available = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.serialPort = serial.Serial()
        self.serialPort.timeout = 1

        self.baudratesDIC = {
            '1200': 1200,
            '2400': 2400,
            '4800': 4800,
            '9600': 9600,
            '19200': 19200,
            '38400': 38400,
            '57600': 57600,
            '115200': 115200
        }
        self.PortDic = {}

        # Hilos
        self.thread = None
        self.alive = Event()

        self.serial_log = ''

    def update_ports(self):
        # real all available ports and update ports list
        for port, description, hwid in serial.tools.list_ports.comports():
            self.PortDic[str(port)] = {'description': str(description), 'hwid': str(hwid)}
        # print(self.PortDic)

    def connect_serial(self, port, baud):
        try:
            self.serial_log = 'Connecting to serial port %s' % port
            self.serialPort.port = port
            self.serialPort.baud = baud
            self.serialPort.open()
        except:
            self.serial_log = ''
            # print("ERROR SERIAL")

        if self.serialPort.is_open:
            self.start_thread()

    def disconnect_serial(self):
        self.stop_thread()
        self.serialPort.close()

    def read_serial(self):
        while self.alive.isSet() and self.serialPort.is_open:
            data = self.serialPort.readline().decode("utf-8").strip()
            if len(data) > 1:
                self.data_available.emit(data)

    def send_data(self, data):
        # if connected to port then send data to port
        if self.serialPort.is_open:
            message = str(data) + "\n"
            self.serialPort.write(message.encode())

    def clear_data(self):
        # if connected to port then send data to port
        if self.serialPort.is_open:
            message = ''
            self.serialPort.write(message.encode())

    def start_thread(self):
        self.thread = Thread(target=self.read_serial)
        self.thread.setDaemon(True)
        self.alive.set()
        self.thread.start()

    def stop_thread(self):
        if self.thread is not None:
            self.alive.clear()
            self.thread.join()
            self.thread = None
