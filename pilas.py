class Pila():
	def __init__(self):
		self.datos = []

	def apilar(self,dato):
		return self.datos.append(dato)

	def desapilar(self,dato):
		return self.datos.pop(dato)

	def esta_vacia(self):
		return len(self.datos)==0