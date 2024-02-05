import pyuac # pip install pyuac
import subprocess
from tkinter import messagebox

def run_as_admin():
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:
        subprocess.run('slmgr /skms kms.digiboy.ir', shell=True)
        subprocess.run('slmgr /ato', shell=True)

        messagebox.showinfo(title='Успешно', message='Windows activated!\n')

if __name__ == '__main__':
    run_as_admin()

