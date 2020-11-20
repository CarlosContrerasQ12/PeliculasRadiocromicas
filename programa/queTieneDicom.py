from pydicom import dcmread
import pydicom
import matplotlib.pyplot as plt
ds = dcmread('Pirana.dcm')
print(ds)
print(ds.DoseGridScaling)


plt.imshow(ds.pixel_array*ds.DoseGridScaling/6.49,cmap=plt.cm.gray)
plt.show()
