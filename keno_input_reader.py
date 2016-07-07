import re 
import numpy as np
import fileinput

#------Read from KENO input------#
kenoFile = 'keno_output_pktest'
kenoFileInput = open(kenoFile, 'r+')
outputFiss = open('outputFissTemp','w')
outputUnit = open('outputUnitFinal','w')
outputUnitArray = []
#-----Parse keno input to find the fission density and corresponding unit number
for line in kenoFileInput:
        if "              unit      region   density     deviation    productions          density     deviation      fissions" in line:
                for line in kenoFileInput:
                        outputFiss.write(line[33:42] + '\n')
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

#-----Add all the fission densities per region -> total  fission density per unit
#-----Fission density [fissions/cm^3]
#-----Multiple fission density by "kappa" fission/energhy
#-----Kappa value is 3.1E-11 Joules/fission, from 192MeV/fission for U235
inputF = inputFiss[1:-1]
total = 0.0
inputFarray = []
powerDenArray = []
#kappa = 0.000000000031
kappa = 3.1E-11
for line in inputF:
        if line.isspace():
                powerDenArray.append( "%.18f" % (total * kappa))
                total = "%.11f" % total
                inputFarray.append(total)
                total = 0.0
        else:
                total = total + float(line)

output = '\n'.join('\t'.join(map(str,row)) for row in zip(inputFarray,powerDenArray,outputUnitArray))
with open('outputUnitFissFinal', 'w') as f:
    f.write(output)
