import TP3

class Bot_tanque(Piloto):
	'''Inteligencia artificial para controlar un Gunpla.'''
    def __init(self):
        '''Crea un piloto y no recibe ningun parámetro'''
        self.gunpla = Gunpla #Gunpla asociado al piloto

    def set_gunpla(self, gunpla):
        '''Asigna un Gunpla a un piloto'''
        self.gunpla = gunpla

    def get_gunpla(self):
        '''Devuelve el Gunpla asociado al piloto'''
        return self.gunpla

    def elegir_esqueleto(lista_esqueletos):
        '''Dada una lista de esqueletos, devuelve el índice del esqueleto a utilizar'''
        esqueleto_energetico = lista_esqueletos[0]
        esqueleto_capacidad = lista_esqueletos[0]
        esqueleto_promedio = lista_esqueletos[0]
        for esqueleto in lista_esqueletos:
        	if esqueleto.get_energia() > esqueleto_energetico.get_energia():
        		esqueleto_energetico = esqueleto        		
			if esqueleto.get_energia() == esqueleto_energetico.get_energia():
				if esqueleto.get_slots() > esqueleto_energetico.get_slots():
					esqueleto_energetico = esqueleto

        	if esqueleto.get_slots() > esqueleto_capacidad.get_slots():
        		esqueleto_capacidad = esqueleto
        	if esqueleto.get_slots() == esqueleto_capacidad.get_slots():
				if esqueleto.get_energia() > esqueleto_capacidad.get_energia():
					esqueleto_capacidad = esqueleto

        	if (esqueleto.get_slots())*(esqueleto.get_energia()) > (esqueleto_promedio.get_slots())*(esqueleto_promedio.get_energia()):
        		esqueleto_promedio = esqueleto

 		if esqueleto_capacidad == esqueleto_energetico:       
        	return esqueleto_energetico
        else:
        	return esqueleto_promedio

        		


    def elegir_parte(partes_disponibles):
        '''Dado un diccionario: {tipo_parte:parte}, devuelve el tipo de parte
        que quiere elegir. Este metodo se utiliza para ir eligiendo de a una las
        partes que se van a reservar para cada piloto, de entre las cuales va a
        poder elegir para armar su modelo'''
        return random.choice(partes_disponibles.keys())

    def elegir_combinacion(partes_reservadas):
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
