from PyQt5.QtCore import Qt
import pyuac # pip install pyuac
import subprocess
from tkinter import messagebox
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDesktopWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer
import winreg
from PyQt5.QtGui import QIcon
import threading

class QWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.temp = self.get_windows_product_key_from_reg()

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)

        button = QPushButton('Activate Windows 10', self)
        button.clicked.connect(self.activate)

        button_2 = QPushButton('CHECK YOUR WINDOWS KEY', self)
        button_2.clicked.connect(self.doing)

        spacer_item = QWidget()
        spacer_item.setSizePolicy(button.sizePolicy())

        central_layout.addWidget(spacer_item)
        central_layout.addWidget(button)
        central_layout.addWidget(button_2)

        self.setCentralWidget(central_widget)

        self.setGeometry(0,0,400,70)
        self.setMaximumSize(400, 70)
        self.setMinimumSize(400, 70)

        self.setWindowTitle('ACTIVATOR')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ChangeTitle)
        self.timer.start(5000)

        self.center()

        self.icon_path = 'sharp.ico' 
        self.setWindowIcon(QIcon(self.icon_path))

    def center(self):
        screenGeometry = QDesktopWidget().screenGeometry()

        center_x = screenGeometry.center().x() - self.width() / 2
        center_y = screenGeometry.center().y() - self.width() / 2

        self.move(int(center_x), int(center_y))

    def run_command(self, command):
        result = subprocess.run(command, shell=True)
        return result.returncode == 0

    def activate(self):
        # Запуск команд в последовательности
        commands = [
            'slmgr /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX',
            'slmgr /skms xincheng213618.cn',
            'slmgr /ato',
        ]

        for command in commands:
            success = self.run_command(command)
            if not success:
                # Если команда не выполнена успешно, прерываем выполнение
                break

        if success:
            # Если все команды выполнены успешно, показываем сообщение об успешном выполнении
            QMessageBox.information(self, 'Успешно', 'Windows activated!')

    def decode_key(self, rpk):
        rpkOffset = 52
        i = 28
        szPossibleChars = "BCDFGHJKMPQRTVWXY2346789"
        szProductKey = ""

        while i >= 0:
            dwAccumulator = 0
            j = 14
            while j >= 0:
                dwAccumulator = dwAccumulator * 256
                d = rpk[j + rpkOffset]
                if isinstance(d, str):
                    d = ord(d)
                dwAccumulator = d + dwAccumulator
                rpk[j + rpkOffset] = int(dwAccumulator / 24) if int(dwAccumulator / 24) <= 255 else 255
                dwAccumulator = dwAccumulator % 24
                j = j - 1
            i = i - 1
            szProductKey = szPossibleChars[dwAccumulator] + szProductKey

            if ((29 - i) % 6) == 0 and i != -1:
                i = i - 1
                szProductKey = "-" + szProductKey
        return szProductKey


    def get_key_from_reg_location(self, key, value='DigitalProductID'):
        arch_keys = [0, winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY]
        for arch in arch_keys:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_READ | arch)
                value, type = winreg.QueryValueEx(key, value)
                return self.decode_key(list(value))
            except (FileNotFoundError, TypeError) as e:
                pass


    def get_windows_product_key_from_reg(self):
        return self.get_key_from_reg_location('SOFTWARE\Microsoft\Windows NT\CurrentVersion')

    def doing(self):
        if self.temp == 'BBBBB-BBBBB-BBBBB-BBBBB-BBBBB':
            from tkinter import messagebox
            messagebox.showerror(title="INFO", message="Windows not activated")
        elif self.temp is not None or self.temp != '':
            from tkinter import messagebox

            messagebox.showinfo(title="Windows is already activated", message=f"YOUR KEY IS: {self.temp}")

    def ChangeTitle(self):
        titles = ['ACTIVATOR', 'https://github.com/S4CBS/win10activator']
        current_title = self.windowTitle()

        current_index = titles.index(current_title) if current_title in titles else 0

        new_index = (current_index + 1) % len(titles)
        new_title = titles[new_index]

        self.setWindowTitle(new_title)
    

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:
        app = QApplication(sys.argv)
        wind = QWindow()
        wind.show()
        sys.exit(app.exec_())
