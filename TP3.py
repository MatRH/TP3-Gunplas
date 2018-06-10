#Modelo de combate de Gunplas
'''
TP3 - Simulador de batallas de Gunplas
Introduccion
La empresa Banzai Mamco nos contrató para realizar un producto ultra secreto. En conmemoración del lanzamiento del New Gundam Breaker este 22 de Junio, la empresa quiere implementar una versión reducida del juego que pueda ayudar a atraer gente a comprar la versión completa del juego. En esta ocasión particular, intentan atraer puntualmente a programadores, asi que creyeron que sería una buena idea hacer un simulador de combates donde cada uno pudiese crear sus propias inteligencias artificiales y competir entre ellas.

El CEO de la empresa no quiere prestarnos ni una versión completa del juego (podrían regalarnos una, ¿no?) antes de la fecha de salida para evitar posibles filtraciones. Dijo que deberíamos conformarnos con lo que vemos en los trailers del juego:

Trailer 1
Trailer 2
En compensación nos ofreció auspiciar un torneo el mismo dia del lanzamiento, con premios para la mejores inteligencias artificiales creadas. De cualquier forma, aun no aclaró cuáles serían.

Consigna
El objetivo del trabajo práctico es implementar:

Un simulador de combates entre modelos Gundam (Gunpla)
Una o más inteligencias artificiales que utilicen el simulador
Reglas del juego
Un Gunpla contiene obligatoriamente un esqueleto.
Un Gunpla puede contener como máximo una parte de cada tipo.
Un Gunpla puede equiparse adicionalmente armas hasta un máximo del número de slots de armas disponibles en el esqueleto (las armas disponibles en las partes no cuentan).
Un esqueleto debe tener un valor de energía mayor a 0.
Un esqueleto debe tener un valor de movilidad mayor o igual a 100.
Una parte puede tener una cantidad mayor o igual a 0 de armas adosadas.
Las partes y armas pueden tener valores negativos de velocidad, armadura, escudo o energía.
Las partes y las armas tienen pesos mayores o iguales a 0.
Las armas tienen uno de los 3 tipos de munición:
FISICA: la reducción de daño se calcula según la fórmula de reducción de daño físico (ver la sección de fórmulas más adelante).
LASER: la reducción de daño se calcula según la fórmula de reducción de daño láser.
HADRON: no tiene reducción de daño.
Las armas son de uno de los 2 tipos:
MELEE: Luego de terminar el ataque, el oponente puede contraatacar con un arma.
RANGO: Luego de terminar el ataque, el oponente no puede contraatacar.
Las armas pueden combinar sus ataques si:
Son del mismo tipo.
Son de la misma clase.
Tienen el mismo tipo de munición.
No está descargada.
Luego de usar un arma, se debe esperar Tiempo de recarga turnos para volver a usarla (Vuelva a estar cargada).
Ciclo de juego
Cada jugador es un piloto que controlará un Gunpla. Se separa a los pilotos en equipos que compiten entre sí; el equipo que logra ser el único con Gunplas activos es el ganador de la partida.

A cada piloto se le da para elegir un esqueleto de una lista de esqueletos disponibles. El mismo esqueleto puede ser elegido por más de un piloto.
Se generan partes y armas de forma aleatoria y se separan en distintas pilas según su tipo.
Las partes se generan ya con sus respectivas armas.
Se dispone a los pilotos en una ronda, en orden aleatorio.
Mientras haya partes o armas para elegir:
A cada piloto se le ofrecen las partes en el tope de cada pila.
El piloto elige un arma o parte, quitándose la misma de la pila correspondiente.
Se pasa las pilas al siguiente piloto en la ronda.
Cada piloto equipa su Gunpla con algunas de las partes elegidas (las partes no utilizadas se descartan).
Se ordena a los pilotos según la velocidad de sus Gunpla y se los encola en la cola de turnos.
Mientras haya dos o más equipos con Gunplas activos:
Se le da el turno al siguiente piloto.
El piloto elige a quien atacar.
El piloto elige el arma con la que atacar.
El piloto ataca al Gunpla del enemigo con su Gunpla (aplicando el algoritmo de combinación de armas y cálculo de daño explicado más adelante).
Si el daño fue nulo:
Se encola un turno extra del enemigo.
Si la energía restante del Gunpla enemigo es negativa y de valor absoluto mayor al 5% de la energía máxima del mismo:
Se encola un turno extra del jugador actual.
Si el arma elegida fue de tipo MELEE y el oponente no fue destruido:
El oponente contraataca: elige un arma y la utiliza como un ataque normal. No aplican reglas de turnos extra o combinación de armas.
Se encola un turno del jugador actual.'''

class Gunpla():
    """Representa un Gunpla. Un Gunpla está copuesto por un Esqueleto,
     un conjunto de partes y un conjunto de armas"""
    def __init__(self):
        self.partes    = [] #lista de partes adosadas al Gunpla
        self.esqueleto = None #referencia a una instancia de la clase Esqueleto
        self.movilidad = 0 #Siendo base la movilidad del esqueleto, peso el peso del Gunpla y velocidad la velocidad del Gunpla: movilidad = (base - peso / 2 + velocidad * 3) / base movilidad = (base - peso / 2 + velocidad * 3) / base
        self.armas     = [] #lista de armas adosadas al Gunpla

    def get_peso(self):
        '''Devuelve el peso total del Gunpla.
        Un Gunpla pesa lo que pesa la sumatoria de sus partes y armas'''
        peso = 0
        for parte in self.partes:
            peso += parte.get_peso()
        for arma in self.armamento:
            peso += arma.get_peso()
        return peso

    def get_armadura(self):
        '''Devuelve la armadura total del Gunpla.
        Un Gunpla tiene tanta armadura como la sumatoria de la armadura de sus
        partes y armas'''
        armadura = 0
        for parte in self.partes:
            armadura += parte.get_armadura()
        for arma in self.armamento:
            armadura += arma.get_armadura()
        return armadura

    def get_escudo(self):
        '''Devuelve el escudo total del Gunpla.
        Un Gunpla tiene tanto escudo como la sumatoria del escudo de sus
        partes y armas'''
        escudo = 0
        for parte in self.partes:
            escudo += parte.get_escudo()
        for arma in self.armamento:
            escudo += arma.get_escudo()
        return escudo

    def get_velocidad(self):
        '''Devuelve la velocidad total del Gunpla.
        Un Gunpla tiene tanta velocidad como la sumatoria de las velocidades
        de sus partes y esqueleto'''
        velocidad = self.esqueleto.get_velocidad()
        for parte in self.partes:
            velocidad += parte.get_velocidad()
        return velocidad

    def get_energia(self):
        '''Devuelve la energía total del Gunpla.
        Un Gunpla tiene tanta energía como la sumatoria de la energía de sus
        partes, armas y esqueleto'''
        energia = self.esqueleto.get_energia()
        for parte in self.partes:
            energia += parte.get_energia()
        for arma in self.armamento:
            energia += arma.get_energia()
        return energia

    def get_energia_restante(self):
        '''Devuelve la energía que le resta al Gunpla'''
        return ''''''

    def get_movilidad(self):
        '''Devuelve la movilidad de un Gunpla.
        Se calcula según la fórmula descripta en la seccion de fórmulas'''
        return self.movilidad

    def get_armamento(self):
        '''Devuelve una lista con todas las armas adosadas al Gunpla
        (Se incluyen las armas disponibles en las partes)'''
        armas_disponibles = []
        for parte in self.partes:
            armas_disponibles.append(parte.get_armamento())
        for arma in self.armas:
            armas_disponibles.append(arma)
        return armas_disponibles


class Esqueleto():
    """Representa el esqueleto interno de un Gunpla"""
    def __init__(self):
        self.velocidad = velocidad      #valor fijo
        self.energia   = energia        #valor fijo
        self.movilidad = movilidad      #valor fijo
        self.slots     = slots          #valor fijo

    def get_velocidad(self):
        '''Devuelve la velocidad del esqueleto'''
        return self.velocidad

    def get_energia(self):
        '''Devuelve la energia del esqueleto'''
        return self.energia

    def get_movilidad(self):
        '''Devuelve la movilidad del esqueleto'''
        return self.movilidad

    def get_cantidad_slots(self):
        '''Devuelve la cantidad de slots (ranuras) para armas que
        tiene el esqueleto.'''
        return self.slots

class Parte():
    """Representa una parte de un Gunpla"""
    def __init__(self):
        self.peso       = peso
        self.armadura   = armadura
        self.escudo     = escudo
        self.velocidad  = velocidad
        self.energia    = energia
        self.armamento  = armamento
        self.tipo_parte = tipo

    def get_peso(self):
        '''Devuelve el peso total de la parte.
        Una parte pesa lo que pesa la sumatoria de sus armas más el peso
        base de la parte'''
        return self.peso

    def get_armadura(self):
        '''Devuelve la armadura total de la parte.
        Una parte tiene tanta armadura como la sumatoria de la armadura de
        sus armas más la armadura base de la parte'''
        return self.armadura

    def get_escudo(self):
        '''Devuelve el escudo total de la parte.
        Una parte tiene tanto escudo como la sumatoria del escudo de sus armas
        más el escudo base de la parte'''
        return self.escudo

    def get_velocidad(self):
        '''Devuelve la velocidad total de la parte.
        Un Gunpla tiene tanta velocidad como la sumatoria de las velocidades
        de sus partes y esqueleto'''
        return self.velocidad

    def get_energia(self):
        '''Devuelve la energía total de la parte.
        La parte tiene tanta energía como la sumatoria de la energía de
        sus armas más la energía base de la parte'''
        return self.eneriga

    def get_armamento(self):
        '''Devuelve una lista con todas las armas adosadas a la parte'''
        return self.armamento

    def get_tipo_parte(self):
        '''Devuelve una cadena que representa el tipo de parte'''
        return self.tipo_parte

class Arma():
    """Representa un arma"""
    def __init__(self):
        self.peso           = peso
        self.armadura       = armadura
        self.escudo         = escudo
        self.velocidad      = velocidad
        self.energia        = energia
        self.tipo_municion  = tipo_municion
        self.tipo_arma      = tipo_arma
        self.clase          = clase
        self.daño           = daño
        self.hits           = hits
        self.precision      = precision
        self.tiempo_recarga = tiempo_recarga
        self.disponible     = lista
        self.tipo_parte     = 'Arma'

    def get_peso(self):
        '''Devuelve el peso del arma. Es un valor fijo'''
        return self.peso

    def get_armadura(self):
        '''Devuelve la armadura del arma. Es un valor fijo'''
        return self.armadura

    def get_escudo(self):
        '''Devuelve la armadura del arma. Es un valor fijo'''
        return self.escudo

    def get_velocidad(self):
        '''Devuelve la velocidad del arma. Es un valor fijo'''
        return self.velocidad

    def get_energia(self):
        '''Devuelve la energía del arma. Es un valor fijo'''
        return self.energia

    def get_tipo_municion(self):
        '''Devuelve el tipo de munición del arma: "FISICA"|"LASER"|"HADRON"'''
        return self.tipo_municion

    def get_tipo(self):
        '''Devuelve el tipo del arma: "MELEE"|"RANGO"'''
        return self.tipo_arma

    def get_clase(self):
        '''Devuelve la clase del arma, la cual es un string. Ejemplo "GN Blade"'''
        return self.clase

    def get_daño(self):
        '''Devuelve el daño de un ataque del arma. Es un valor fijo'''
        return self.daño

    def get_hits(self):
        '''Devuelve la cantidad de veces que puede atacar un arma en un turno.
        Es un valor fijo'''
        return self.hits

    def get_precision(self):
        '''Devuelve la precisión del arma'''
        return self.precision

    def get_tiempo_recarga(self):
        '''Devuelve la cantidad de turnos que tarda un arma en estar lista'''
        return self.tiempo_recarga

    def esta_lista(self):
        '''Devuelve si el arma es capaz de ser utilizada en este turno o no'''
        return self.disponible

    def get_tipo_parte(self):
        '''Devuelve el tipo de parte de un arma. Siempre es "Arma"'''
        return self.tipo_parte

'''Fórmulas
Movilidad
Siendo base la movilidad del esqueleto, peso el peso del Gunpla y velocidad la velocidad del Gunpla:

movilidad = (base - peso / 2 + velocidad * 3) / base
La movilidad tiene un límite superior de 1 e inferior de 0.

Reducción de daño físico
Siendo daño el daño recibido y armadura la armadura del Gunpla:

daño reducido = daño - armadura
El daño reducido tiene un límite inferior de 0.

Reducción de daño láser
Siendo daño el daño recibido y escudo el escudo del Gunpla:

daño reducido = daño - daño * escudo
El daño reducido no tiene límite. Si es negativo, implica que aumenta la energía del Gunpla.

Algoritmo de cálculo de daño
Atacante:

Se usa Hit veces el arma. Cada uso genera Daño con un Precisión% de probabilidad (sino, el daño es 0).
Con un (25 * Precisión)% de probabilidad el daño se multiplica por 1,5.
Con una probabilidad, puede combinar su ataque con el de otra arma combinable, aplicando el mismo algoritmo del atacante de forma recursiva:
Si el arma es MELEE, la probabilidad es del 40%.
Si el arma es RANGO, la probabilidad es del 25%.
Si es un contraataque, la probabilidad es siempre nula.
Defensor:

Con un (80 * Movilidad)% de probabilidad, evade el daño completamente.
Reduce el daño según el tipo.
Absorbe el daño restante.'''
