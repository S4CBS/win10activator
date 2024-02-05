import os
import pyuac # pip install pyuac
import subprocess


if not pyuac.isUserAdmin():
    pyuac.runAsAdmin()
else:
    commands = [
        'slmgr /skms kms.digiboy.ir',
        'slmgr /ato'
    ]

for command in commands:
    subprocess.run(command, shell=True)