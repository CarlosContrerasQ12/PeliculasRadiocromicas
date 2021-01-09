from pydicom import dcmread
import pydicom
import matplotlib.pyplot as plt
ds = dcmread('piramide2.dcm')
ds2 = dcmread('piramide.dcm')
print(ds)
print(ds2)

plt.axis('off')
plt.imshow(ds.pixel_array*ds.DoseGridScaling,cmap=plt.cm.gray)
plt.figure()

plt.axis('off')
plt.imshow(ds2.pixel_array*ds2.DoseGridScaling,cmap=plt.cm.gray)
plt.show()
