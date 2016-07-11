import re 
import numpy as np
import fileinput

#------Read from KENO input------#
kenoFile = 'keno_output_pktest'
kenoFileInput = open(kenoFile, 'r+')
outputFiss = open('outputFissTemp','w')
thermalFile = open('thermal_conductivity','r+')
outputUnitArray = ['     Unit #']
thermalArray = [' thermal Cond [W/(cm C)']
#------Read thermal conductivity from file with order of values equivalent to corresponding unit #
for line in thermalFile:
        thermalArray.append(float(line))
#------Parse keno input to find the fission density and corresponding unit number
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

#-----Add all the fission densities per region -> total  fission density per unit
#-----Fission density [fissions/cm^3]
#-----Multiple fission density by "kappa" fission/energhy
#-----Kappa value is 3.1E-11 Joules/fission, from 192MeV/fission for U235
inputF = inputFiss[1:-1]
total = 0.0
inputFarray = ['Fission Density']
powerDenArray = ['Power Density']
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

output = '\n'.join('\t'.join(map(str,row)) for row in zip(inputFarray,powerDenArray,outputUnitArray,thermalArray))
with open('outputUnitFissFinal', 'w') as f:
        f.write(output)


#----------------CREATE DUMMY GRID BASED ON 2D UNIT NUMBER------------#
array_x_y_unit = []
x_pts =   []
y_pts =   []
z_pts =   []
color_z = []
#---------------GET THE UNIT NUMBERS FROM KENO ARRAY---------
filename= raw_input("Enter the file name containing the array: ")

#-------------------Read in total----------------------------
data = np.loadtxt(filename)
class point_on_grid(object):
        def __init__(self,x,y,unit_num,tot_flux):
                self.x=x
                self.y=y
                self.unit_num=unit_num
                self.tot_flux=tot_flux
#-------------------------------------------------------------
tot_flux = .5
max_x=len(data)
max_y=len(data[0])
i=0
j=0
color = 'blue'
xpt=0.0
ypt=0.0
for i in range(max_x):
        for j in range(max_y):
                xpt = float(j*10.10)
                ypt= float(i*10.10)
                point = point_on_grid(xpt,ypt,data[i][j],tot_flux)
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
#-------Write out points and corresponding unit number--------
output = '\n'.join('\t'.join(map(str,row)) for row in zip(x_pts,y_pts,z_pts))
with open('outputXY-Unit', 'w') as f:
    f.write(output)
#-------------------------------------------------------------

#-------------PLOT--------------------------------------------
#plt.scatter(x_pts,y_pts,marker='.',s=150,c=z_pts)
#plt.show()

