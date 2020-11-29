import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
nombres=["/home/carlos/Escritorio/Medidas Finales 2/0GyPos5-16lines.tif",
"/home/carlos/Escritorio/Medidas Finales 2/02GyPos5-16lines.tif",
"/home/carlos/Escritorio/Medidas Finales 2/05GyPos5-16lines.tif",
"/home/carlos/Escritorio/Medidas Finales 2/1GyPos5-16lines.tif",
"/home/carlos/Escritorio/Medidas Finales 2/2GyPos5-16lines.tif",
"/home/carlos/Escritorio/Medidas Finales 2/4GyPos5-16lines.tif",
"/home/carlos/Escritorio/Medidas Finales 2/6GyPos5-16lines.tif",
"/home/carlos/Escritorio/Medidas Finales 2/8GyPos5-16lines.tif",
"/home/carlos/Escritorio/Medidas Finales 2/10GyPos5-16lines.tif",
"/home/carlos/Escritorio/Medidas Finales 2/12GyPos5-16lines.tif",
"/home/carlos/Escritorio/Medidas Finales 2/15GyPos5-16lines.tif",
"/home/carlos/Escritorio/Medidas Finales 2/20GyPos5-16lines.tif"]

arreglos=[]
forma=(3,4)
xmax=0
ymax=0
for nombre in nombres:
	arr=tiff.imread(nombre)
	x,y,z=arr.shape
	if x>xmax:
		xmax=x
	if y>ymax:
		ymax=y
	arreglos.append(arr)
print(xmax)
print(ymax)
arrfinal=np.zeros(shape=(forma[0]*xmax,forma[1]*ymax,3))	

i=0
j=0
for arr in arreglos:
	arrfinal[i*xmax:i*xmax+arr.shape[0],j*ymax:j*ymax+arr.shape[1],:]=arr
	i+=1
	if i>forma[0]-1:
		i=0
		j+=1
esa=arrfinal/2**16		
plt.imshow(esa)
plt.show()		
tiff.imsave("imagenTotal.tif",arrfinal)	
leido=tiff.imread("imagenPromediada.tif")
plt.imshow(leido/2**16	)
plt.show()		
		
