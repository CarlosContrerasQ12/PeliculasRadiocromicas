from pydicom import dcmread
import pydicom
import numpy as np
import pymedphys
import matplotlib.pyplot as plt



ds1=dcmread('/home/carlos/Escritorio/Piramide_2.0/PiramideGamma.dcm')
ds2=dcmread('/home/carlos/Escritorio/Piramide_2.0/Piramide4laminas.dcm')
print(ds1)
print(ds2)

reference = ds1.pixel_array/np.max(ds1.pixel_array)
evaluation = ds2.pixel_array/np.max(ds2.pixel_array)

plt.imshow(reference)
plt.figure()
plt.imshow(evaluation)
plt.show()

#reference=reference/26.334
#evaluation=evaluation/26.334
print(evaluation.shape)
print(reference.shape)



x1=np.linspace(0,512*ds1.PixelSpacing[0],512)
y1=np.linspace(0,512*ds1.PixelSpacing[1],512)

x2=np.linspace(0,512*ds2.PixelSpacing[0],512)
y2=np.linspace(0,512*ds2.PixelSpacing[1],512)


"""
x1=np.linspace(0,300,768)
y1=np.linspace(0,400,1024)

x2=np.linspace(0,300,768)
y2=np.linspace(0,400,1024)
"""

ejes1=(x1,y1)
ejes2=(x2,y2)

dd=1
mm=1
interp=4
if dd==1:
	interp=4
if dd==2:
	interp=5
if dd==3:
	interp=10	
	


gamma_options = {
    'dose_percent_threshold': dd,
    'distance_mm_threshold': mm,
    'lower_percent_dose_cutoff':3,
    'interp_fraction':5,  # Should be 10 or more for more accurate results
    'max_gamma': 5,
    'random_subset': None,
    'local_gamma': False,
    'ram_available': 5*(2**29)  # 1/2 GB
}

gamma = pymedphys.gamma(
    ejes1, reference,
    ejes2, evaluation,
    **gamma_options)
    
plt.imshow(gamma)
valid_gamma = gamma[~np.isnan(gamma)]
pass_ratio = np.sum(valid_gamma <= 1) / len(valid_gamma)
print("El porentaje de aprovacion es",pass_ratio)

valid_gamma = gamma[~np.isnan(gamma)]
print(valid_gamma.shape)

plt.figure()
  
valid_gamma = gamma[~np.isnan(gamma)]
num_bins = (gamma_options['interp_fraction'] * gamma_options['max_gamma'])
bins = np.linspace(0, gamma_options['max_gamma'], num_bins + 1)
plt.hist(valid_gamma, bins, density=True)
#plt.set_xlim([0, gamma_options['max_gamma']])
pass_ratio = np.sum(valid_gamma <= 1) / len(valid_gamma)
print(pass_ratio)
plt.show()

