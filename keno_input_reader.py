import re 
import numpy as np
import fileinput

#------Read from KENO input------#
kenoFile = 'keno_output_pktest'
kenoFileInput = open(kenoFile, 'r+')
outputFiss = open('outputFissTemp','w')
outputUnit = open('outputUnitFinal','w')
outputUnitArray = []
outputFissArray = []
for line in kenoFileInput:
        if "              unit      region   density     deviation    productions          density     deviation      fissions" in line:
                for line in kenoFileInput:
                        outputFiss.write(line[33:42] + '\n')
                        outputFissArray.append(line[33:42])
                        if "  global unit" in line: 
                                break        
                        if line[15:18].isspace():
                                pass 
                        else:
                                if line == '\n':
                                        pass
                                else:
#                                        outputUnit.write(line[15:18] + '\n')
                                        outputUnitArray.append(line[15:18])
outputFiss.flush()
#inputUnit = open('outputUnitFinal','r+')
inputFiss = open('outputFissTemp', 'r+').readlines()
#output = open('outputFissFinal','w')

inputF = inputFiss[1:-1]
total = 0.0
inputFarray = []
for line in inputF:
        if line.isspace():
                inputFarray.append(total)
                total = 0.0
        else:
                total = total + float(line)

output = '\n'.join('\t'.join(map(str,row)) for row in zip(inputFarray,outputUnitArray))
with open('outputUnitFissFinal', 'w') as f:
    f.write(output)
