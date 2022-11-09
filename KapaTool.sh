#!/bin/bash
# welcome me and install manging dependencies
echo "Thank you for choosing automated mechanisms, OneJoon GmbH"
sudo apt update
sudo apt install git
git init
git clone https://github.com/etchoum/Pyprojekt.git
sudo apt install vim

# enter the cloned github repository
cd Pyprojekt
sudo apt install python3.9
sudo apt install pip
python3.9 -m pip install tabulate
python3.9 -m pip install openpyxl
python3.9 -m pip install pandas
python3.9 -m pip install matplotlib
python3.9 model.py
python3.9 KapaTool.py --auftrag 1306280 # 1308284 # 1006245
python3.9 KapaTool.py --psp_element G10066 # G10074
python3.9 Kapa.py

