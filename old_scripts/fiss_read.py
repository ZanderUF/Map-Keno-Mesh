import re 
import numpy as np
import fileinput

#------Read from KENO input------#
inputFiss = open('outputFissTemp', 'r+').readlines()
output = open('outputFissFinal','w')

inputF = inputFiss[1:-1]
total = 0.0
for line in inputF:
        if line.isspace():
                output.write(str(total) + '\n')
                total = 0.0 
        else:
                total = total + float(line)
