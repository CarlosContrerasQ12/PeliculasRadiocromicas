import numpy as np
from PIL import Image
import SimpleITK as sitk
from scipy.optimize import curve_fit

def funcionReciprocaLineal(D,params):
	return params[0]+(params[1]/(D-params[2]))

def funcionRacionalLineal(D,params):
	return (params[0]+params[1]*D)/(D+params[2])
	
def funcionRacionalCuadratica(D,params):
	return (params[0]+params[1]*D+params[2]*D*D)/(D+params[3])	

def funcionRacionalCubica(D,params):
	return (params[0]+params[1]*D+params[2]*D*D+params[3]*D*D*D)/(D+params[4])	
	
def funcionExponencialPolinomica(D,params):
	return  params[0]+params[1]*(D**params[2])
	
def funcionLinealDB(D,params):
	return  params[0]+params[1]*(D)	
	

def guardar_calibracion(tipoCanal,tipoCurva,parametros,dosis,transmitancias,nombreArchivo):
	f=open(nombreArchivo,'a')
	f.write("Calibracion"+'\n')
	f.write("Nombre: "+nombreArchivo+'\n')
	f.write("Tipo Canal: "+tipoCanal+'\n')
	f.write("Tipo Curva: "+tipoCurva+'\n')
	f.write("parametros: "+','.join(map(str,parametros)+'\n')
	f.write("Dosis Usadas: "+','.join(map(str,dosis)+'\n')
	f.write("Transmitancias: "+','.join(map(str,transmitancias)+'\n')
	f.close()
	

	

		
		

class CalibracionImagen:
	def __init__(self,imagen,promsR,promsG,promsB,dosis,tipoCanal,tipoCurva,filtrar,corrLateral,corrBackground,nombreArchivo):
		self.T=[]
		self.promsR=promsR/65535.0
		self.promsG=promsG/65535.0
		self.promsB=promsB/65535.0
		self.dosis=dosis
		self.tipoCanal=tipoCanal
		self.tipoCurva=tipoCurva
		self.filtrar=filtrar
		self.corrLateral=corrLateral
		self.corrBackground=self.corrBackground
		self.parametrosOptimos=[]
		self.Covarianza=[]
		self.nombreArchivo=nombreArchivo
		def f():
			return 0
		self.funcionCali=f
		
	def generar_calibracion(self,nombreArchivo):

		if tipoCanal!="Multicanal":
			if tipoCanal=="Canal rojo":
				self.T=self.promsR
			elif tipoCanal=="Canal verde":
				self.T=self.promsG
			elif tipoCanal=="Canal azul":
				self.T=self.promsB
			elif tipoCanal=="Promedio RGB":
				for k in range(len(self.promsR)):
					self.T.append((self.promsR+self.promsG+self.promsB)/3.0)
					
			if !corrLateral:
				if tipoCurva="Reciproca Lineal":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionReciprocaLineal, dosis, self.T)
					def faux(D):
						return funcionReciprocaLineal(D,*self.parametrosOptimos)
					self.funcionCali=faux
				elif tipoCurva="Racional Lineal":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionRacionalLineal, dosis, self.T)
					def faux(D):
						return funcionRacionalLineal(D,*self.parametrosOptimos)
					self.funcionCali=faux
				elif tipoCurva="Racional Cuadratica":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionRacionalCuadratica, dosis, self.T)
					def faux(D):
						return funcionRacionalCuadratica(D,*self.parametrosOptimos)
					self.funcionCali=faux
				elif tipoCurva="Racional Cubica":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionRacionalCubica, dosis, self.T)
					def faux(D):
						return funcionRacionalCubica(D,*self.parametrosOptimos)
					self.funcionCali=faux
				elif tipoCurva="Exponencial Polinomica":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionExponencialPolinomica, dosis, self.T)
					def faux(D):
						return funcionExponencialPolinomica(D,*self.parametrosOptimos)
					self.funcionCali=faux
				elif tipoCurva="Lineal (Dosis bajas)":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionLinealDB, dosis, self.T)
					def faux(D):
						return funcionLinealDB(D,*self.parametrosOptimos)
					self.funcionCali=faux
		guardar_calibracion(self.tipoCanal,self.tipoCurva,self.parametrosOptimos,self.dosis,self.T,self.nombreArchivo)	
				
				
				
					

			

		
		


