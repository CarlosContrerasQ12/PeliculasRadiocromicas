import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
ima=tiff.imread('/home/carlos/Escritorio/Medidas Finales 2/planMama-16lines.tif')

plt.imshow((ima/((2**16)-1)))

plt.figure()

imaM=np.flip(ima,axis=0)
tiff.imsave("planMamaVolteado.tif",imaM)

plt.imshow((imaM/((2**16)-1)))

plt.show()



