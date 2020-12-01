import numpy as np
from claseCalibracion import *
import tifffile as tiff
import matplotlib.pyplot as plt
from filtradoImagenes import *

dosis=np.load('dosisMulti.npy')
pR=np.load('RMultiTrans.npy')
pG=np.load('GMultiTrans.npy')
pB=np.load('BMultiTrans.npy')
incer=np.load('IncerMulti.npy')
calibr=CalibracionImagen(pR,pG,pB,incer,dosis,"Multicanal","Racional lineal")
calibr.generar_calibracion("multicanal.calibr")

dta=leer_Calibracion("multicanal.calibr")

ima=tiff.imread("/home/carlos/Escritorio/Medidas Finales 2/cuadrado5Gy-16lines.tif")
#ima= filtrar_imagen(ima,"mediana")
araySinIrra=0*ima
ceR=araySinIrra[:,:,0]+dta["Ceros"][0][0]
ceG=araySinIrra[:,:,1]+dta["Ceros"][1][0]
ceB=araySinIrra[:,:,2]+dta["Ceros"][2][0]

#araySinIrra=np.dstack((ceR,ceG,ceB))*(2**16)
arraySinIrra=tiff.imread("/home/carlos/Escritorio/Medidas Finales 2/FondeCero-16lines.tif")
#oDimage= np.log10(araySinIrra/ima)
oDimage=(ima)/((2**16)-1)

trans=dta["funcionTaD"]
deltas=oDimage*0
rojo=oDimage[:,:,0]
verde=oDimage[:,:,1]
azul=oDimage[:,:,2]
deltas=dta["funcionCalDel"](rojo,verde,azul)


mapaDosis=trans(deltas,rojo,verde,azul)
#mapaDosis=trans(rojo)

ins=np.where(mapaDosis<0)
mapaDosis[ins]=0
ins=np.where(np.isnan(mapaDosis))
mapaDosis[ins]=5
ins=np.where(mapaDosis>20)
mapaDosis[ins]=0

ins=np.where(deltas<0.7)
deltas[ins]=1
ins=np.where(np.isnan(deltas))
deltas[ins]=1
ins=np.where(deltas>10)
deltas[ins]=1


        
plt.imshow(deltas,cmap=mpl.cm.gray)
plt.colorbar()
plt.figure()
plt.imshow(mapaDosis,cmap=mpl.cm.gray)
plt.show()
