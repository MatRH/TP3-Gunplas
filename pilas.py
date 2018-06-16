class Pila():
	'''Representa una pila.
	'''
	def __init__(self):
		self.datos = []

	def apilar(self,dato):
		'''Metodo para apilar datos a la pila.
		'''
		return self.datos.append(dato)

	def desapilar(self,dato):
		'''Metodo para desapilar datos de la pila.
		'''
		return self.datos.pop(dato)

	def esta_vacia(self):
		'''Metodo para verificar si una pila esta vacia.
		'''
		return len(self.datos)==0


class _Nodo():
	'''Representa un Nodo.
	'''
	def __init__(self, dato=None, prox=None, ant= None, ult=None):
		self.dato = dato
		self.prox = prox
		self.ant  = ant
		self.ult  = ult

	def append(self,elemento):
		nuevo = _Nodo(elemento, None, self.ult)
		if not self.prim:
			self.prim = nuevo
		else:
			self.ult.prox = nuevo
		self.ult = nuevo
			self.ult.prox 

class Cola():
	'''Representa una cola.
	'''
	def __init__(self):
		self.prim = None
		self.ult  = None

	def encolar(self,dato):
		'''Metodo para encolar un dato a la cola.
		'''
		if not self.prim:
			self.prim = nodo
			self.ult  =	nodo
		else:
			self.ult.prox = nodo
			self.prox	  = nodo

	def desencolar(self):
		'''Metodo para desencolar un dato de la cola.
		'''
		dato 	  = self.prim
		self.prim = self.prox
		if not self.prim:
			self.ult = None
		return dato


