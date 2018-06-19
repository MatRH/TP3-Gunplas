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
        esqueleto_capacidad  = lista_esqueletos[0]
        esqueleto_promedio   = lista_esqueletos[0]
        for esqueleto in lista_esqueletos:
        	if esqueleto.get_energia() > esqueleto_energetico.get_energia():
        		esqueleto_energetico     = esqueleto        		
			if esqueleto.get_energia()   == esqueleto_energetico.get_energia():
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
        partes           = partes_disponibles.values()
        parte_energetica = tipo_parte[0]
        parte_escudo     = tipo_parte[0]
        parte_promedio   = tipo_parte[0]
        for parte in tipos_partes:
            if parte.get_energia() > parte_energetica.get_energia():
                parte_energetica = parte
            if parte.get_energia() == parte_energetica.get_energia():
                if parte.get_escudo() > parte_escudo.get_escudo():
                    parte_energetica = parte
            if parte.get_escudo() > parte_escudo.get_escudo():
                parte_escudo = parte
            if parte.get_escudo() == parte_escudo.get_escudo():
                if parte.get_energia() > parte_escudo.get_energia():
                    parte_escudo = parte
            if parte.get_energia() * parte.get_escudo() > parte_promedio.get_energia() * parte_promedio.get_escudo():
                parte_promedio = parte
        if parte_energetica == parte_escudo:
            return parte_energetica
        else:
            return parte_promedio

    def elegir_arma(lista_armas,oponente):
        '''Devuelve el arma con la cual se decide atacar al oponente.
        '''
        armas_oponente      = oponente.get_armamento()
        arma_elegida        = lista_armas[0]
        armas_rango         = []
        armas_melee         = []
        arma_oponente_melee = None
        arma_elegida_rango  = armas_rango[0]
        arma_elegida_melee  = armas_melee[0]

        for arma in lista_armas:
            if arma.get_tipo() == "RANGO" and arma.esta_lista():
                armas_rango.append(arma)
            if arma.get_tipo() == "MELEE" and arma.esta_lista():
                armas_melee.append(arma)
            
        for arma_oponente in armas_oponente:
                if arma_oponente.get_tipo() == "MELEE":
                    arma_oponente_melee = True
                    break
                else:
                    arma_oponente_melee = False

        if arma_oponente_melee:
            for arma_rango in armas_rango: 
                if arma_rango.get_daño() * arma_rango.get_hits() > arma_elegida_rango.get_daño() * arma_elegida_rango.get_hits():
                    arma_elegida = arma_rango
                if arma_rango.get_daño() * arma_rango.get_hits() == arma_elegida_rango.get_daño() * arma_elegida_rango.get_hits():
                    if arma_rango.get_daño() > arma_elegida.get_daño():
                        arma_elegida = arma_rango
                    if arma_rango.get_daño() == arma_elegida_rango.get_daño():
                        if arma_rango.get_hits() >= arma_elegida_rango.get_hits():
                            arma_elegida = arma_rango
                if arma_rango.get_daño() * arma_rango.get_hits() < arma_elegida_rango.get_daño() * arma_elegida_rango.get_hits():
                    arma_elegida = arma_elegida_rango
        else:
            for arma_melee in armas_melee:
                if arma_melee.get_daño() * arma_melee.get_hits() > arma_elegida_melee.get_daño() * arma_elegida_melee.get_hits():
                    arma_elegida = arma_melee
                if arma_melee.get_daño() * arma_melee.get_hits() == arma_elegida_melee.get_daño() * arma_elegida_melee.get_hits():
                    if arma_melee.get_daño() > arma_elegida_melee.get_daño():
                        arma_elegida = arma_melee
                    if arma_melee.get_daño() == arma_elegida_melee.get_daño():
                        if arma_melee.get_hits() >= arma_elegida_melee.get_hits():
                            arma_elegida = arma_melee
                if arma_melee.get_daño() * arma_melee.get_hits() < arma_elegida_melee.get_daño() * arma_elegida_melee.get_hits():
                    arma_elegida = arma_elegida_melee
        return arma_elegida


    def elegir_combinacion(partes_reservadas):
        '''Dada una lista con partes previamente reservadas, devuelve una lista
        con las partes a utilizar para construir el Gunpla. Este método se
        utiliza para elegir las partes que se van a utilizar en el modelo, de
        entre las que se reservaron previamente para cada piloto.'''
        partes_utilizar = []
        while len(partes_utilizar) < 5:
            parte = partes_reservadas[0]

            if parte not in partes_utilizar:
                partes_utilizar.append(parte)
        return partes_utilizar
