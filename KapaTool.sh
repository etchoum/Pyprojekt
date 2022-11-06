#!/bin/bash
# welcome me and install manging dependencies
echo "Thank you for choosing automated mechanisms, OneJoon GmbH"
sudo apt update
sudo apt install git
git init
git clone https://github.com/etchoum/Pyprojekt.git

# enter the cloned github repository
cd Pyprojekt
sudo apt install python3.9
python3.9 -m pip install tabulate
python3.9 -m pip install openpyxl
python3.9 -m pip install pandas
python3.9 model.py
python3.9 pyscript.py
python3.9 KapaTool.py --auftrag 1006245
python3.9 KapaTool.py --psp_element G1006245
python3.9 Kapa.py

