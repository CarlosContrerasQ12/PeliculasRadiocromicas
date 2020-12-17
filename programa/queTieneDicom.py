from pydicom import dcmread
import pydicom
import matplotlib.pyplot as plt
ds = dcmread('MapaMama.dcm')
ds2 = dcmread('piramide.dcm')
print(ds)
print(ds2)


plt.imshow(ds.pixel_array*ds.DoseGridScaling,cmap=plt.cm.gray)
plt.figure()
plt.imshow(ds2.pixel_array*ds2.DoseGridScaling,cmap=plt.cm.gray)
plt.show()
