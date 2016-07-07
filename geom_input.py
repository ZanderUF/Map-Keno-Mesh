import re 
import numpy as np
import fileinput

#------Read from KENO input------#
kenoFile = 'keno_output_pktest'
kenoFileInput = open(kenoFile, 'r+')
outputGeom = open('outputGeom','w')

for line in kenoFileInput:
        if "geometry description input" in line:
                for line in kenoFileInput:
                        if "*************** data reading completed ***************" in line:
                                break
                        else:
                                if line.isspace():
                                        pass
                                else:
                                        outputGeom.write(line) 
