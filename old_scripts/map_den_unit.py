import re 
import numpy as np
import fileinput
import numpy as np

#------Read from KENO input------#
#inputDensity = open('outputFissTemp', 'r+').readlines()
#inputXYunit = open('outputXY-unit','r+').readlines()
inputDensity = np.loadtxt('outputUnitFissFinal',skiprows=1)
inputXYunit  = np.loadtxt('outputXY-unit',skiprows=1)

output = open('mapped-den-unit','w')
output.write( '{0:<10}'.format('X') + "   " + '{0:<10}'.format('Y')
+ "   " + '{0:<10}'.format('Unit ') + "   " + '{0:<10}'.format('Fiss Den')
+ "   " + '{0:<10}'.format('Power Den') + "    " + '{0:<10}'.format('Thermal Cond') + '\n')
for lineXY in inputXYunit:
        for lineDen in inputDensity:   
                if lineXY[2] == lineDen[2]:
                        output.write( '{0:<10}'.format(str(lineXY[0])) + "   " + '{0:<10}'.format(str(lineXY[1])) 
                        + "   " + '{0:<10}'.format(str(lineXY[2])) + "   " + '{0:<10}'.format(str(lineDen[0])) 
                        + "   " + '{0:<10}'.format(str(lineDen[1])) + "   " + '{0:<10}'.format(str(lineDen[3])) +'\n' )
                        
