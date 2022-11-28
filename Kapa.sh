#!/bin/bash
sudo apt update
sudo apt install git
git init
gi clone https://github.com/etchoum/Pyprojekt.git
sudo apt install vim
cd Pyprojekt
sudo apt install python3.9
sudo apt install pip
python3.9 -m pip install pandas
python3.9 -a 1307068
python3.9 Kapa.py -s IN_BEARBEITUNG,ZU_PLANEN
python3.9 Kapa.py -p G10064
python3.9 Kapa.py -p G10064 -d
python3.9 Kapa.py
python3.9 model.py
