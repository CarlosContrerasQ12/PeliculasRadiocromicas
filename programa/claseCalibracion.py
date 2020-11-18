import numpy as np
from PIL import Image
import SimpleITK as sitk
from scipy.optimize import curve_fit
import dill

def funcionReciprocaLineal(x,p0,p1,p2):
	return p0+(p1/(x-p1))

def funcionRacionalLineal(x,p0,p1,p2):
	return (p0+p1*x)/(x+p2)
	
def funcionInversaRacionalLineal(y,p0,p1,p2):
	return (p0-p2*y)/(y-p1)
	
def funcionRacionalCuadratica(x,p0,p1,p2,p3):
	return (p0+p1*x+p2*x*x)/(x+p3)	

def funcionRacionalCubica(x,p0,p1,p2,p3,p4):
	return (p0+p1*x+p2*x*x+p3*x*x*x)/(x+p4)	
	
def funcionExponencialPolinomica(x,p0,p1,p2):
	return  p0+p1*(x**p2)
	
def funcionLinealDB(x,p0,p1):
	return  p0+p1*(x)	
	

def guardar_calibracion(tipoCanal,tipoCurva,parametros,dosis,transmitancias,funcionTaD,funcionDaT,nombreArchivo):
	f=open(nombreArchivo,'a')
	"""
	f.write("Calibracion"+'\n')
	f.write("Nombre: "+nombreArchivo+'\n')
	f.write("Tipo Canal: "+tipoCanal+'\n')
	f.write("Tipo Curva: "+tipoCurva+'\n')
	f.write("parametros: "+','.join(map(str,parametros))+'\n')
	f.write("Dosis Usadas: "+','.join(map(str,dosis))+'\n')
	f.write("Transmitancias: "+','.join(map(str,transmitancias))+'\n')
	f.close()
	"""
	dis={"Nombre":nombreArchivo,"TipoCanal":tipoCanal,"TipoCurva":tipoCurva,"Parametros":parametros,"Dosis":dosis,"Transmitancias":transmitancias,"funcionTaD":funcionTaD,"funcionDaT":funcionDaT}
	dill.settings['recurse'] = True
	#ser=dill.dumps(dis)
	dill.dump(dis, open(nombreArchivo, 'wb'))
	
def leer_Calibracion(nombreArchivo):
	f=open(nombreArchivo,'rb')
	return dill.load(f)
	

	

		
		

class CalibracionImagen:
	def __init__(self,promsR,promsG,promsB,dosis,tipoCanal,tipoCurva,corrLateral):
		self.T=[]
		self.TCeros=[]
		self.promsR=promsR[0]
		self.promsRCero=promsR[1]
		self.promsG=promsG[0]
		self.promsGCero=promsG[1]
		self.promsB=promsB[0]
		self.promsBCero=promsB[1]
		self.dosis=dosis
		self.tipoCanal=tipoCanal
		self.tipoCurva=tipoCurva
		self.corrLateral=corrLateral
		self.parametrosOptimos=[]
		self.Covarianza=[]
		def f():
			return 0
		self.funcionTaD=f
		self.funcionDaT=f
		
	def generar_calibracion(self,nombreArchivo):

		if self.tipoCanal!="Multicanal":
			print("aca")
			if self.tipoCanal=="Canal rojo":
				self.T=self.promsR
				self.TCeros=self.promsRCero
			elif self.tipoCanal=="Canal verde":
				self.T=self.promsG
				self.TCeros=self.promsGCero
			elif self.tipoCanal=="Canal azul":
				self.T=self.promsB
				self.TCeros=self.promsBCero
			elif self.tipoCanal=="Promedio RGB":
				for k in range(len(self.promsR)):
					self.T.append((self.promsR[k]+self.promsG[k]+self.promsB[k])/3.0)
					self.T.append((self.promsRCero[k]+self.promsGCero[k]+self.promsBCero[k])/3.0)	
					
			if not self.corrLateral:
				if self.tipoCurva=="Reciproca lineal":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionReciprocaLineal, self.dosis, self.T)
					def faux(D):
						return funcionReciprocaLineal(D,*self.parametrosOptimos)
					self.funcionCali=faux
				elif self.tipoCurva=="Racional lineal":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionRacionalLineal, self.dosis, self.T)
					print(self.parametrosOptimos)
					def faux(D):
						return funcionRacionalLineal(D,*self.parametrosOptimos)
					self.funcionDaT=faux
					def finv(T):
						return funcionInversaRacionalLineal(T,*self.parametrosOptimos)
					self.funcionTaD=finv
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
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionExponencialPolinomica, netOD, self.dosis)
					def faux(D):
						return funcionExponencialPolinomica(D,*self.parametrosOptimos)
					self.funcionCali=faux
				elif self.tipoCurva=="Lineal (Dosis bajas)":
					self.parametrosOptimos,self.pCovarianza=curve_fit(funcionLinealDB, self.dosis, self.T)
					def faux(D):
						return funcionLinealDB(D,*self.parametrosOptimos)
					self.funcionCali=faux
		guardar_calibracion(self.tipoCanal,self.tipoCurva,self.parametrosOptimos,self.dosis,self.T,self.funcionTaD,self.funcionDaT,nombreArchivo)	
				
				
				
					

			

		
		


