import TP3

class Piloto():
    '''Inteligencia artificial para controlar un Gunpla.'''
    def __init__(self):
        '''Crea un piloto y no recibe ningun parámetro'''
        self.gunpla = Gunpla #Gunpla asociado al piloto

    def set_gunpla(self, gunpla):
        '''Asigna un Gunpla a un piloto'''
        self.gunpla = gunpla

    def get_gunpla(self):
        '''Devuelve el Gunpla asociado al piloto'''
        return self.gunpla

    def elegir_esqueleto(self, lista_esqueletos):
        '''Dada una lista de esqueletos, devuelve el índice del esqueleto a utilizar'''
        esqueleto_mobilidad = lista_esqueletos[0]
        esqueleto_capacidad = lista_esqueletos[0]
        esqueleto_elegido	= lista_esqueletos[0]

        for esqueleto in lista_esqueletos:
        	if esqueleto.get_cantidad_slots() * esqueleto.get_mobilidad() > esqueleto_elegido.get_cantidad_slots() * esqueleto_elegido.get_mobilidad():
        		esqueleto_elegido = esqueleto
        	if esqueleto.get_cantidad_slots() * esqueleto.get_mobilidad() == esqueleto_elegido.get_cantidad_slots() * esqueleto_elegido.get_mobilidad():
        		if esqueleto.get_velocidad() > esqueleto_elegido.get_velocidad():
        			esqueleto_elegido = esqueleto
        		if esqueleto.get_velocidad() == esqueleto_elegido.get_velocidad():
        				






    def elegir_parte(self, partes_disponibles):
        '''Dado un diccionario: {tipo_parte:parte}, devuelve el tipo de parte
        que quiere elegir. Este metodo se utiliza para ir eligiendo de a una las
        partes que se van a reservar para cada piloto, de entre las cuales va a
        poder elegir para armar su modelo'''
        for tipo, parte in partes_disponibles.items():
            return parte
        
    def elegir_combinacion(self, partes_reservadas):
        '''Dada una lista con partes previamente reservadas, devuelve una lista
        con las partes a utilizar para construir el Gunpla. Este método se
        utiliza para elegir las partes que se van a utilizar en el modelo, de
        entre las que se reservaron previamente para cada piloto.'''
        partes_utilizar = []
        while len(partes_utilizar) < 5:
            parte = random.choice(partes_reservadas)
            if parte not in partes_utilizar:
                partes_utilizar.append(parte)
        return partes_utilizar

    def elegir_oponente(self,lista_oponentes):
        '''Dada una lista de oponentes,devuelve el indice del gunpla al cual se decide atacar.
        '''
        return index(random.choice(lista_oponentes))
        
    def elegir_arma(self,oponente):
        '''Devuelve el arma con la cual se decide atacar al oponente.
        '''

        return random.choice(self.gunpla().get_armamento())
