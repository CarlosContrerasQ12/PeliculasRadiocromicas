import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import tifffile as tiff
import cv2
from pydicom import dcmread

ds = dcmread('piramide2.dcm')
x=np.linspace(-5,5,512)
y=np.linspace(-5,5,512)

z=ds.pixel_array/np.max(ds.pixel_array)

plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
plt.title('Mapa TPS')
plt.figure()
plt.contour(x, y, z - 0.5, levels = [0],colors=['red'])
plt.title('Isodosis TPS')
plt.figure()


def funcionRacional(x,a,b,c):
	return (a+b*x)/(c+x)


"""
def funcionRacional(x,a,b):
	return a*x/(1-b*x)
"""
R=np.genfromtxt('Rhp.txt')
G=np.genfromtxt('Ghp.txt')
B=np.genfromtxt('Bhp.txt')
dosis=np.genfromtxt('dosishp.txt')

"""
R=1-R
G=1-G
B=1-B
"""

parameR,covaR=curve_fit(funcionRacional,dosis,R-R[0] )
parameG,covaG=curve_fit(funcionRacional,dosis, G-G[0])
parameB,covaB=curve_fit(funcionRacional,dosis,B-B[0] )


x=np.linspace(dosis[0],dosis[-1],100)
yR=funcionRacional(x,*parameR)
yG=funcionRacional(x,*parameG)
yB=funcionRacional(x,*parameB)

plt.grid()
plt.scatter(dosis,R-R[0],marker='x',color='r')
plt.scatter(dosis,G-G[0],marker='x',color='g')
plt.scatter(dosis,B-B[0],marker='x',color='b')
plt.plot(x,yR,'r--')
plt.plot(x,yG,'g--')
plt.plot(x,yB,'b--')


plt.figure()


def inversaRacional(x):
	return (parameR[2]*x-parameR[0])/(parameR[1]-x)



print(dosis)
print(funcionRacional(dosis,*parameR))
print(R-R[0])

arrayMama=tiff.imread('pira69.tif')
kernel = np.ones((5,5),np.float32)/25
arrayMama = cv2.filter2D(arrayMama,-1,kernel)
arrayMama=arrayMama/2**8
arrayMama=arrayMama[:,:,0]
arrayMama=1-arrayMama
arrayMama=arrayMama-R[0]


plt.imshow(arrayMama*2**8,cmap=plt.cm.gray)
plt.title('Canal rojo plan escaneado')
plt.figure()

scale_percent = 60

width = int(arrayMama.shape[1] * scale_percent / 100)
height = int(arrayMama.shape[0] * scale_percent / 100)

dsize = (width, height)

arrayCom=cv2.resize(arrayMama, dsize, interpolation = cv2.INTER_NEAREST)
plt.imshow(arrayCom,cmap=plt.cm.gray)
plt.title('Canal rojo plan escaneado resize')
plt.figure()
print(arrayCom)


dosis5=inversaRacional(arrayCom)
ins=np.where(dosis5>10)
dosis5[ins]=0
ins=np.where(dosis5<0)
dosis5[ins]=0
dosis5=dosis5/np.mean(dosis5[220:246,280:312])
plt.imshow(dosis5,cmap=plt.cm.gray)
plt.title('Mapa de dosis con la calibracion')

print(dosis5)

plt.figure()

x=np.linspace(-5,5,width)
y=np.linspace(-5,5,height)
plt.contour(x, y, dosis5 - 0.5, levels = [0],colors=['red'])
plt.title('Isodosis con la calibracion')
plt.show()

"""
arrayMama=arrayMama-np.mean(arrayMama[0:25][0:25])
print(np.max(arrayMama))
print(np.min(arrayMama))
mapaDosis=inversaRacional(arrayMama)

mapaDosis=mapaDosis/np.max(mapaDosis)
print(mapaDosis)
plt.imshow(mapaDosis,cmap=plt.cm.gray)
plt.show()
"""






