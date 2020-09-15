import numpy as np
from PIL import Image
import SimpleITK as sitk
from scipy.optimize import curve_fit

def funcionReciprocaLineal(D,p0,p1,p2):
	return p0+(p1/(D-p1))

def funcionRacionalLineal(D,p0,p1,p2):
	return (p0+p1*D)/(D+p2)
	
def funcionRacionalCuadratica(D,p0,p1,p2,p3):
	return (p0+p1*D+p2*D*D)/(D+p3)	

def funcionRacionalCubica(D,p0,p1,p2,p3,p4):
	return (p0+p1*D+p2*D*D+p3*D*D*D)/(D+p4)	
	
def funcionExponencialPolinomica(D,p0,p1,p2):
	return  p0+p1*(D**p2)
	
def funcionLinealDB(D,p0,p1):
	return  p0+p1*(D)	
	

def guardar_calibracion(tipoCanal,tipoCurva,parametros,dosis,transmitancias,nombreArchivo):
	f=open(nombreArchivo,'a')
	f.write("Calibracion"+'\n')
	f.write("Nombre: "+nombreArchivo+'\n')
	f.write("Tipo Canal: "+tipoCanal+'\n')
	f.write("Tipo Curva: "+tipoCurva+'\n')
	f.write("parametros: "+','.join(map(str,parametros))+'\n')
	f.write("Dosis Usadas: "+','.join(map(str,dosis))+'\n')
	f.write("Transmitancias: "+','.join(map(str,transmitancias))+'\n')
	f.close()
	

	

		
		

class CalibracionImagen:
	def __init__(self,promsR,promsG,promsB,dosis,tipoCanal,tipoCurva,corrLateral):
		self.T=[]
		self.promsR=promsR
		self.promsG=promsG
		self.promsB=promsB
		self.dosis=dosis
		self.tipoCanal=tipoCanal
		self.tipoCurva=tipoCurva
		self.corrLateral=corrLateral
		self.parametrosOptimos=[]
		self.Covarianza=[]
		def f():
			return 0
		self.funcionCali=f
		
	def generar_calibracion(self,nombreArchivo):

		if self.tipoCanal!="Multicanal":
			print("aca")
			if self.tipoCanal=="Canal rojo":
				self.T=self.promsR
			elif self.tipoCanal=="Canal verde":
				self.T=self.promsG
			elif self.tipoCanal=="Canal azul":
				self.T=self.promsB
			elif self.tipoCanal=="Promedio RGB":
				for k in range(len(self.promsR)):
					self.T.append((self.promsR+self.promsG+self.promsB)/3.0)
					
			if not self.corrLateral:
				print("aca2")
				if self.tipoCurva=="Reciproca lineal":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionReciprocaLineal, self.dosis, self.T)
					def faux(D):
						return funcionReciprocaLineal(D,*self.parametrosOptimos)
					self.funcionCali=faux
				elif self.tipoCurva=="Racional lineal":
					print("Legga a fitear")
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionRacionalLineal, self.dosis, self.T)
					print(self.parametrosOptimos)
					def faux(D):
						return funcionRacionalLineal(D,*self.parametrosOptimos)
					self.funcionCali=faux
				elif self.tipoCurva=="Racional cuadratica":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionRacionalCuadratica, self.dosis, self.T)
					def faux(D):
						return funcionRacionalCuadratica(D,*self.parametrosOptimos)
					self.funcionCali=faux
				elif self.tipoCurva=="Racional cubica":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionRacionalCubica, self.dosis, self.T)
					def faux(D):
						return funcionRacionalCubica(D,*self.parametrosOptimos)
					self.funcionCali=faux
				elif self.tipoCurva=="Exponencial polinomica":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionExponencialPolinomica, self.dosis, self.T)
					def faux(D):
						return funcionExponencialPolinomica(D,*self.parametrosOptimos)
					self.funcionCali=faux
				elif self.tipoCurva=="Lineal (Dosis bajas)":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionLinealDB, self.dosis, self.T)
					def faux(D):
						return funcionLinealDB(D,*self.parametrosOptimos)
					self.funcionCali=faux
		guardar_calibracion(self.tipoCanal,self.tipoCurva,self.parametrosOptimos,self.dosis,self.T,nombreArchivo)	
				
				
				
					

			

		
		


