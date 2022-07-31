#!/bin/bash
# welcome me
echo "Thank you for choosing slurm"
# export the pfad for the programming application
# it is important to live no space inbetween the definition(=) of variables
PFAD_python="/scratch1/users/etchoum/PROJECT/webpage/venv/bin/python3.9"
export python3=$PFAD_python
# export exports the variable assignment to child processes of the shell in which the export command was ran .
# or just run 'module load python/3.9.0'; then to execute pythonscript, just 'python argp.py' .
# check if any typing errors are in the pythonscript
pycodestyle=/scratch1/users/etchoum/PROJECT/webpage/venv/lib/python3.9/site-packages/pycodestyle.py
python $pycodestyle --show-source --show-pep8 argp.py
# or do directly:
# python /scratch1/users/etchoum/PROJECT/webpage/venv/lib/python3.9/site-packages/pycodestyle.py --show-source --show-pep8 argp.py ;
# kindly adapt the pfads, if Python3 or pycodestyle is somewhere provided for all users ;
# also it is possible to create a funtion 'check_errors' for that by following syntax:
check_errors () {
   python $pycodestyle --show-source --show-pep8 $1
}
# and execute it by 'check_errors argp.py'
# proceed to execute the original pythonscript from the exported python pfad
$python3 ./argp.py
$python3 ./argp.py -m
