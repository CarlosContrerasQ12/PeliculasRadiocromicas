from pydicom import dcmread
import pydicom
import numpy as np
import pymedphys
import matplotlib.pyplot as plt



ds1=dcmread('TPS_270.dcm')
ds2=dcmread('Medido_270.dcm')

print(ds2)
print(ds1)


reference = ds1.pixel_array/np.max(ds1.pixel_array)
evaluation = ds2.pixel_array/np.max(ds1.pixel_array)

plt.imshow(reference)
plt.figure()
plt.imshow(evaluation)

plt.show()


#reference=reference/26.334
#evaluation=evaluation/26.334
print(evaluation.shape)
print(reference.shape)



x1=np.linspace(0,300,768)
y1=np.linspace(0,400,1024)

x2=np.linspace(0,300,768)
y2=np.linspace(0,400,1024)

ejes1=(x1,y1)
ejes2=(x2,y2)
gamma_options = {
    'dose_percent_threshold': 2,
    'distance_mm_threshold': 2,
    'lower_percent_dose_cutoff':5,
    'interp_fraction':30,  # Should be 10 or more for more accurate results
    'max_gamma': 5,
    'random_subset': None,
    'local_gamma': False,
    'ram_available': 5*(2**29)  # 1/2 GB
}

gamma = pymedphys.gamma(
    ejes1, reference,
    ejes2, evaluation,
    **gamma_options)
    
print(gamma.shape)   
print(gamma)
plt.imshow(gamma)
plt.show()
valid_gamma = gamma[~np.isnan(gamma)]
pass_ratio = np.sum(valid_gamma <= 1) / len(valid_gamma)
print(pass_ratio)

valid_gamma = gamma[~np.isnan(gamma)]
print(valid_gamma.shape)

 
  
valid_gamma = gamma[~np.isnan(gamma)]
num_bins = (gamma_options['interp_fraction'] * gamma_options['max_gamma'])
bins = np.linspace(0, gamma_options['max_gamma'], num_bins + 1)
plt.hist(valid_gamma, bins, density=True)
#plt.set_xlim([0, gamma_options['max_gamma']])
pass_ratio = np.sum(valid_gamma <= 1) / len(valid_gamma)
print(pass_ratio)
plt.show()

