import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats.distributions import chi2

def f(x,a,b,c):
	return a*x**2+b*x+c
	
N=7
sig=0.05
mu=0.0

x=np.linspace(-2,2,N)
y=x**2+x-1+np.random.normal(mu,sig,N)
incer=y*0+sig

pOptim,pCov=curve_fit(f,x,y,sigma=incer)

def g(x):
	return f(x,*pOptim)
	
SR=np.sum(((y-g(x))/incer)**2)
print(SR)
print("La bondad de ajuste para el canal rojo es de ", chi2.sf(SR,len(x)-len(pOptim)))

plt.grid()	
plt.errorbar(x,y,color='b',yerr=incer,fmt='o')
xr=np.linspace(-2,2,100)
yr=g(xr)

plt.plot(xr,yr,'g--')
plt.plot(xr,xr**2+xr-1,'r--')
plt.show()


