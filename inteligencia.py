from TP3 import Gunpla, Esqueleto, Parte, Arma, Piloto
from math import fabs

def calcular_dps_arma(arma):
    '''Recibe un objeto arma y devuelve el dps (daño por turno) que puede
    causar un arma en promedio'''
    hits = arma.get_hits()
    dmg  = arma.get_daño()
    cd   = arma.get_tiempo_recarga()
    dps = (hits * dmg)/cd
    return dps

def nivel_amenaza(gunpla):
    '''Recibe un gunpla y estudia sus partes y armas y devuelve un valor
    que representa el nivel de amenaza que presenta ese gunpla en el turno
    proximo'''
    dps = 0
    hp = gunpla.get_energia()
    for arma in gunpla.get_armamento():
        if arma.esta_lista() or arma.get_tiempo_recarga() < 2:
            dps += calcular_dps_arma(arma)
    return energia * dps

def calcular_handicap(parte):
    '''Recibe una parte y devuelve un valor que representa cuanto reducira los
    atributos del gunpla si se la equipa'''
    atributos = [parte.get_energia(), parte.get_escudo(), parte.get_armadura(), parte.get_velocidad()]
    peso = parte.get_peso()
    handicap = fabs(peso)
    for atributo in atributos:
        if atributo < 0:
            handicap *= fabs(atributo)
    return handicap

def buscar_mejor_arma(lista_armas):
    '''Recibe una lista de armas y  devuelve la mejor arma para ese
    gunpla'''
    mejor_arma = lista_armas[0]
    for arma in lista_armas:
        dps_mejor = calcular_dps_arma(mejor_arma)
        dps_arma = calcular_dps_arma(arma)
        if arma.tipo_municion() == 'HADRON' and dps_arma > dps_mejor/2:
            mejor_arma = arma
        if dps_arma > dps_mejor and calcular_handicap(arma) <= calcular_handicap(mejor_arma) :
            mejor_arma = arma
        if dps_arma > dps_mejor*3/4 and calcular_handicap(arma) <= calcular_handicap(mejor_arma):
            mejor_arma = arma
    return mejor_arma


class Piloto(): #Ninja
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

    def elegir_esqueleto(self, lista_esqueletos):
        '''Dada una lista de esqueletos, devuelve el índice del esqueleto a utilizar'''
        return random.choice(lista_esqueletos)

    def elegir_parte(self, partes_disponibles):
        '''Dado un diccionario: {tipo_parte:parte}, devuelve el tipo de parte
        que quiere elegir. Este metodo se utiliza para ir eligiendo de a una las
        partes que se van a reservar para cada piloto, de entre las cuales va a
        poder elegir para armar su modelo'''
        armas_disponibles = []
        partes = []
        for tipo, parte in partes_disponibles.items():
            if tipo = 'Arma':
                armas_disponibles.append(arma)
            else:
                



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
        return index(random.choice(lista_oponentes))#para la IA deberia utilizar un contador para devolver la posicion correcta

    def elegir_arma(self,oponente):
        '''Devuelve el arma con la cual se decide atacar al oponente.
        '''
        return random.choice(self.gunpla().get_armamento())
