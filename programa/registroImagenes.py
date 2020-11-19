import numpy as np
import matplotlib.pyplot as plt
from pydicom import dcmread
import SimpleITK as sitk

mapaDosis1=np.load("PiramideDosis.npy") 

mapaDosis1=mapaDosis1/6.48   
plt.imshow(mapaDosis1,cmap=plt.cm.gray)
ds = dcmread('piramide2.dcm')
mapaDosis2=ds.pixel_array/np.max(ds.pixel_array)   
plt.figure()
plt.imshow(mapaDosis2,cmap=plt.cm.gray)
plt.show()

