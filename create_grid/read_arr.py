#-- Read array from KENO and have corespond to x,y axis 
#-- for plotting fluxes
#--
#---------------------Declarations---------------------------
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
#---------------------Variables------------------------------
array_x_y_unit = []
x_pts =   []
y_pts =   []
z_pts =   []
color_z = []
#---------------GET THE UNIT NUMBERS FROM KENO ARRAY----------
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
	z_pts.append(array_x_y_unit[q].unit_num)

#-------Write out points and corresponding unit number------#         
output = '\n'.join('\t'.join(map(str,row)) for row in zip(x_pts,y_pts,z_pts))
with open('outputUnit.txt', 'w') as f:
    f.write(output)
#-------------------------------------------------------------

#---------Assign flux for each unit------------

#-------------PLOT-------------------------------------------
plt.scatter(x_pts,y_pts,marker='.',s=150,c=z_pts)

plt.show()
