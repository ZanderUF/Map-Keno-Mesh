#----File: map_xy_to_vals.py
#----Purpose:  Reads KENO output to gather fission densities & unit #s
#----          Converts to power density.  Creates artifical grid and 
#----          maps (x,y) coordinates to power/fiss densities & thermal 
#----          conductivity (read in from file)
#----          Power Density[units] = [W/cm^-3]
#----          Thermal conductivity[units] = [Wcm^-1C^-1]
#----

#---------------------------------------------------------------------#
import os
import re 
import numpy as np
import fileinput
import matplotlib.pyplot as plt
#---------------------------------------------------------------------#
DEBUG = 'FALSE'
#------------------FIRST PARSE THE KENO INPUT FILE--------------------#
kenoFile = 'keno_output_pktest'
kenoFileInput = open(kenoFile, 'r+')
outputFiss = open('outputFissTemp','w')
thermalFile = open('thermal_conductivity','r+')
outputUnitArray = ['     Unit #']
thermalArray = [' thermal Cond [W/(cm K)']
temperatureFile = open('temperatures','r+')
temperatureArray = ['Temp [k]']
#------Read thermal conductivity from file with order of unit---------# 
for line in thermalFile:
        thermalArray.append(float(line))
#------Read temperature from file with order of unit------------------#
#------***WILL EVENTUALL NEED TO GET FROM KENO INPUT------------------#
for line in temperatureFile:
        temperatureArray.append(float(line))
#------Find the fission density and corresponding unit numberi--------#
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
                                        outputUnitArray.append(int(line[15:18]))

outputFiss.flush()
inputFiss = open('outputFissTemp', 'r+').readlines()

#-----Add all the fission densities/region->total fission density/unit#
#-----Fission density [fissions/cm^3]----------------------------------#
#-----Multiple fission density by "kappa" [fission/energy]-------------#
#-----Kappa value is 3.1E-11 Joules/fission,from 192MeV/fission for U235
inputF = inputFiss[1:-1]
total = 0.0
inputFarray = ['Fission Density']
powerDenArray = ['Power Density']
kappa = 3.1E-11
for line in inputF:
        if line.isspace():
                powerDenArray.append( "%.18f" % (total * kappa))
                total = "%.11f" % total
                inputFarray.append(total)
                total = 0.0
        else:
                total = total + float(line)

output = '\n'.join('\t'.join(map(str,row)) for row in zip(inputFarray
        ,powerDenArray,outputUnitArray,thermalArray,temperatureArray))
with open('outputUnitFissFinal', 'w') as f:
        f.write(output)

#----------------CREATE DUMMY GRID BASED ON 2D UNIT NUMBER------------#
array_x_y_unit = []
x_pts =   []
y_pts =   []
z_pts =   []
color_z = []
#---------------GET THE UNIT NUMBERS FROM KENO ARRAY------------------#
#filename= raw_input("Enter the file name containing the array: ")

kenoDataArray = np.loadtxt('array_pktest')
class point_on_grid(object):
        def __init__(self,x,y,unit_num,tot_flux):
                self.x=x
                self.y=y
                self.unit_num=unit_num
                self.tot_flux=tot_flux
#---------------------------------------------------------------------#
tot_flux = .5 #---dummy value now
max_x=len(kenoDataArray)
max_y=len(kenoDataArray[0])
i=0
j=0
xpt=0.0
ypt=0.0
for i in range(max_x):
        for j in range(max_y):
                xpt = float(j*10.10)
                ypt= float(i*10.10)
                point = point_on_grid(xpt,ypt,kenoDataArray[i][j],tot_flux)
                array_x_y_unit.append(point)
                j+=1
        #ypt= i*10.105
        i+=1
for q in range (len(array_x_y_unit)):
        x_pts.append(round(array_x_y_unit[q].x,3) )
        y_pts.append(round(array_x_y_unit[q].y,3) )
        z_pts.append(int(array_x_y_unit[q].unit_num))

x_pts.insert(0,'X ')
y_pts.insert(0,'Y ')
z_pts.insert(0,'Unit #')
#-------Write out points and corresponding unit number----------------#
output = '\n'.join('\t'.join(map(str,row)) for row in zip(x_pts,y_pts,z_pts))
with open('outputXY-Unit', 'w') as f:
    f.write(output)
#---------------------------------------------------------------------#

#-------------PLOT XY GRID AND UNIT #s for Debugging------------------#
if plt == 'TRUE':
        plt.scatter(x_pts,y_pts,marker='.',s=150,c=z_pts)
        plt.show()
        
#------MAP X,Y,UNIT TO POWER/FISSION DENSITIES AND THERMAL COND--------#
inputDensity = np.loadtxt('outputUnitFissFinal',skiprows=1)
inputXYunit  = np.loadtxt('outputXY-unit',skiprows=1)

output = open('final-mapped-xy-densities.txt','w')
output.write( '{0:<10}'.format('X') + "   " + '{0:<10}'.format('Y')
+ "   " + '{0:<10}'.format('Unit ') + "   " + '{0:<10}'.format('Fiss Den')
+ "   " + '{0:<10}'.format('Power Den') 
+ "    " + '{0:<10}'.format('Therm-Cond') 
+ "    " + '{0:<10}'.format('Temperature') + '\n')
for lineXY in inputXYunit:
        for lineDen in inputDensity:
                if lineXY[2] == lineDen[2]:
                        output.write( '{0:<10}'.format(str(lineXY[0])) 
                        + "   " + '{0:<10}'.format(str(lineXY[1]))
                        + "   " + '{0:<10}'.format(str(lineXY[2]))  
                        + "   " + '{0:<10}'.format(str(lineDen[0]))
                        + "   " + '{0:<10}'.format(str(lineDen[1]))
                        + "   " + '{0:<10}'.format(str(lineDen[3])) 
                        + "   " + '{0:<10}'.format(str(lineDen[4])) 
                        +'\n' )

#-------------------------------CLEAN UP-------------------------------#
if DEBUG == 'True':
        #keep the temporary files
        pass
else:
        os.remove('outputFissTemp')
        os.remove('outputXY-unit')
        os.remove('outputUnitFissFinal')
