import numpy as np
from PIL import Image
import SimpleITK as sitk

class ImagenCalibracion:
	def __init__(self,rutaImagen,nombre,numeroPuntos):
		self.ruta=ruta
		self.nombre=nombre
		self.numeroPuntos=numeroPuntos
		self.imOriginal=Image.open(ruta)
		self.imArreglo=np.array(self.imOriginal)

	

class FuncionCalibracion:
	def __init__(self,tipo)		

