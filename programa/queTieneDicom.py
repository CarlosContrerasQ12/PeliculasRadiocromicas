from pydicom import dcmread
import pydicom
import matplotlib.pyplot as plt
ds = dcmread('Maplo.dcm')
print(ds.top())
print(ds.DoseGridScaling)

plt.imshow(ds.pixel_array)
plt.show()
