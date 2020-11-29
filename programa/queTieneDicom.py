from pydicom import dcmread
import pydicom
import matplotlib.pyplot as plt
ds = dcmread('piramide2.dcm')
print(ds)
print(ds.DoseGridScaling)


plt.imshow(ds.pixel_array*ds.DoseGridScaling,cmap=plt.cm.gray)
plt.show()
