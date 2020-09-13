import numpy as np
from PIL import Image
import SimpleITK as sitk

class Calibracion:
	def __init__(self,dosis,tipoCanal,tipoCurva):
		self.dosis=dosis
		self.tipoCanal=tipoCanal
		self.tipoCurva=tipoCurva
		self.parametros=[]


class CalibracionImagen:
	def __init__(self,imagen,esquinasSecciones,dosis,tipoCanal,tipoCurva,filtrar,corrLateral,corrBackground):
		self.imagen=imagen
		self.esquinasSecciones=esquinasSecciones
		self.dosis=dosis
		self.tipoCanal=tipoCanal
		self.tipoCurva=tipoCurva
		self.filtrar=filtrar
		self.corrLateral=corrLateral
		self.corrBackground=self.corrBackground
		
	def generar_calibracion(nombreArchivo):
		
		


