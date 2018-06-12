'''
Ciclo de juego:
Cada jugador es un piloto que controlará un Gunpla.

1) Se separa a los pilotos en equipos que compiten entre sí;
    el equipo que logra ser el único con Gunplas activos es el ganador de la partida.

2) A cada piloto se le da para elegir un esqueleto de una lista de esqueletos disponibles.
    El mismo esqueleto puede ser elegido por más de un piloto.

3) Se generan partes y armas de forma aleatoria y se separan en distintas pilas según su tipo.
    Las partes se generan ya con sus respectivas armas.

4) Se dispone a los pilotos en una ronda, en orden aleatorio.

5)Mientras haya partes o armas para elegir:
    -A cada piloto se le ofrecen las partes en el tope de cada pila.
    -El piloto elige un arma o parte, quitándose la misma de la pila correspondiente.
    -Se pasa las pilas al siguiente piloto en la ronda.
    -Cada piloto equipa su Gunpla con algunas de las partes elegidas (las partes no utilizadas se descartan).

6) Se ordena a los pilotos según la velocidad de sus Gunpla y se los encola en la cola de turnos.

7) Mientras haya dos o más equipos con Gunplas activos:
    -Se le da el turno al siguiente piloto.
    -El piloto elige a quien atacar.
    -El piloto elige el arma con la que atacar.
    -El piloto ataca al Gunpla del enemigo con su Gunpla (aplicando el algoritmo de combinación de armas y cálculo de daño)
        *Si el daño fue nulo:
            -Se encola un turno extra del enemigo.
        *Si la energía restante del Gunpla enemigo es negativa y de valor absoluto mayor al 5% de la energía máxima del mismo:
            -Se encola un turno extra del jugador actual.
        *Si el arma elegida fue de tipo MELEE y el oponente no fue destruido:
            -El oponente contraataca:
                .elige un arma y la utiliza como un ataque normal.
                .No aplican reglas de turnos extra o combinación de armas.
8) Se encola un turno del jugador actual.
'''
'''
Reglas del juego:

Gunplas:
-Un Gunpla contiene obligatoriamente un esqueleto.
-Un Gunpla puede contener como máximo una parte de cada tipo.
-Un Gunpla puede equiparse adicionalmente armas hasta un máximo del número de slots de armas disponibles en el esqueleto (las armas disponibles en las partes no cuentan).

Esqueletos:
-Un esqueleto debe tener un valor de energía mayor a 0.
-Un esqueleto debe tener un valor de movilidad mayor o igual a 100.

Partes:
-Una parte puede tener una cantidad mayor o igual a 0 de armas adosadas.
-Las partes y armas pueden tener valores negativos de velocidad, armadura, escudo o energía.
-Las partes y las armas tienen pesos mayores o iguales a 0.

Armas:
-Las armas tienen uno de los 3 tipos de munición:
    FISICA: la reducción de daño se calcula según la fórmula de reducción de daño físico (ver la sección de fórmulas más adelante).
    LASER: la reducción de daño se calcula según la fórmula de reducción de daño láser.
    HADRON: no tiene reducción de daño.
-Las armas son de uno de los 2 tipos:
    MELEE: Luego de terminar el ataque, el oponente puede contraatacar con un arma.
    RANGO: Luego de terminar el ataque, el oponente no puede contraatacar.
-Las armas pueden combinar sus ataques si:
    Son del mismo tipo.
    Son de la misma clase.
    Tienen el mismo tipo de munición.
    No está descargada.
-Luego de usar un arma, se debe esperar Tiempo de recarga turnos para volver a usarla (Vuelva a estar cargada).
'''
import random
import TP3

def armar_equipos(lista_pilotos, cantidad_equipos):
    '''Recibe una lista de pilotos de la cual elige para armas equipos y una
     cantidad de equipos a armar, divide a los pilotos equitativamente de manera
     que halla la misma cantidad de pilotos por equipo; si esto no fuera posible
     debido a que la cantidad de pilotos no fuera divisible por la cantidad de
     equipos, se le pedira al usuario que agregue la cantidad necesaria de pilotos
     para completar el equipo o en caso de que el usuario no ingrese nada se
     autocompletaran los equipos con un piloto al azar de la biblioteca de
     pilotos BOT.
     Devuelve una lista de listas, donde cada sub_lista representa un equipo,
     y Cada elemento es un piloto'''

     lista_equipos              = []
     pilotos                    = lista_pilotos[:]

     for i in range(len(lista_pilotos) % cantidad_equipos):
         pilotos.append(random.choice(pilotos_bot))

     while pilotos:
         equipo = []
         for i in range(len(pilotos) / cantidad_equipos):
             piloto = pilotos.pop(random.choice(pilotos))
             equipo.append(piloto)
        lista_equipos.append(equipo)

    return lista_equipos

def asignar_gunplas(lista_equipos):
    '''Recibe la lista de equipos y le asigna un gunpla a cada piloto.
    '''
    for equipo in lista_equipos:
        for piloto in equipo:
            gunpla=Gunpla()
            piloto.set_gunpla(gunpla)


def generar_esqueletos(cantidad, velocidad_max, energia_max, movilidad_max, slots_max):
    '''Recibe una cantidad de esqueletos a generar, un valor maximo para Cada
    uno de los atributos correspondiente al esqueleto, velocidad, energia, movilidad
    y slots. el valor maximo para la energia debe ser mayor a cero y el de la
    movilidad mayor a 100.
    Genera la cantidad introducida de esqueletos con atributos que varian
    entre:
    - velocidad max ingresada <= velocidad <= + velocidad max ingresada
    0   <= energia <= energia maxima ingresada
    100 <= movilidad <= movilidad maxima ingresada
    0 <= slots <= slots maximos ingresados
    y los devuelve en una lista
    '''
    lista_esqueletos = []
    while len(esqueletos) < cantidad:
        esqueleto = Esqueleto()
        esqueleto.velocidad = random.randint(-velocidad_max, velocidad_max)
        esqueleto.energia = random.randint(0, energia_max)
        esqueleto.movilidad = random.randint(100, movilidad_max)
        esqueleto.slots = random.randint(0, slots_max)
        lista_esqueletos.append(esqueleto)
    return lista_esqueletos


def asignar_esqueletos(lista_esqueletos,lista_equipos):
    '''Recibe una lista de esqueletos y una lista de equipos la cual es una lista de listas,
    donde cada sublista es un equipo y cada elemento de la lista es un Piloto. Cada Piloto 
    elige un esqueleto, y se le asigna a su Gunpla.
    '''
    for equipo in lista_equipos:
        for piloto in equipo:
            esqueleto_elegido = piloto.elegir_esqueleto()
            piloto.get_gunpla()._set.esqueleto(esqueleto_elegido)

def generar_armas(cantidad, daño,hits,precision,peso,armadura,escudo,velocidad,energia):
    '''Recibe la cantidad de armas a generar, el daño,hits(cantidad de veces que puede atacar
    en el mismo turno),precision ,peso , armadura, energia, escudo y velocidad maximos.
     Devuelve la lista de armas generadas.
    '''
    lista_armas = []
    while len(armas) < cantidad:
        arma                = Arma()
        arma.daño           = random.randint(1, daño)
        arma.hits           = random.randint(1, hits )
        arma.precision      = random.randint(0,precision )
        arma.peso_base      = random.randint(1,peso)
        arma.energia_base   = random.randint(-energia, energia)
        arma.armadura_base  = random.randint(-armadura , armadura)
        arma.escudo_base    = random.randint(-escudo , escudo)
        arma.velocidad_base = random.randint(-velocidad, velocidad)
        arma.tipo_parte     = 'Arma'
        arma.tipo_municion  = random.choice(('FISICA', 'LASER', 'HADRON'))
        arma.tipo_arma      = random.choice(('MELEE', 'RANGO'))
        arma.clase          = #generador de nombres
        lista_armas.append(arma)
    return lista_armas

def generar_partes(cantidad, peso, armadura, escudo, velocidad, energia, prob_armas, cant_max_armas):
    '''Recibe la cantidad de partes a generar, el peso , armadura, energia, escudo ,velocidad maximos, 
    la probabilidad de que la parte contenga armas y la cantidad maxima de armas que puede tener una parte.
    Devuelve la lista de armas generadas.
    '''
    lista_partes = []
    while len(lista_partes) < cantidad:
        parte = Parte()
        parte.peso_base          = random.randint(1, peso)
        parte.armadura_base      = random.randint(-armadura , armadura)
        parte.escudo_base        = random.randint(-escudo, escudo)
        parte.velocidad_base     = random.randint(-velocidad, velocidad)
        parte.energia_base       = random.randint(-energia, energia)
        parte.armas              = []
        parte.tipo_parte         = #generador de nombres
        if random.randint(0,100) > prob_armas:
            cantidad_armas = random.randint(1,cant_max_armas)
            parte.armas.append(generar_armas(cantidad_armas, daño,hits,precision, peso ,armadura,escudo,velocidad,energia))
    return lista_partes

def separar_en_pilas(lista_armas,lista_partes):
    '''Recibe las listas de armas y partes y las apila en pilas distintas segun su tipo. 
    Devuelve una lista de pilas
    '''
    lista_pilas = []
    pila_melee = Pila()
    pila_rango = Pila()
    for arma in lista_armas:
        if arma.get_tipo == 'MELEE':
            pila_melee.apilar(arma)

        else:
            pila_rango.apilar(arma)
    lista_pilas.append(pila_melee)
    lista_pilas.append(pila_rango)

    for parte in lista_partes:
        tipo = str(parte.get_tipo_parte())
        if tipo not in lista_pilas:
            tipo = Pila()
            lista_pilas.append(tipo)
        tipo.apilar(parte)
    return lista_pilas

def armar_ronda(lista_equipos):
    '''Recibe la lista de equipos, la desordenada y devuelve una ronda con los pilotos desordenados.
    '''
    ronda=[]
    numero_piloto = 0
    for equipo in lista_equipos:
        for piloto in equipo:
            numero_piloto += 1
            ronda.append((numero_piloto, piloto))
    random.shuffle(ronda)
    return ronda

def reservar_partes(lista_pilas, ronda):
    '''Recibe una lista de pilas disponibles para los gunplas y la ronda de pilotos
    y reserva las partes que elige cada piloto siguiendo la ronda de turnos.
    '''
    partes_disponibles = {}
    partes_reservadas = {}
    
    while lista_pilas:
        for numero_piloto, piloto in ronda:
            for pila in lista_pilas:
                parte_disponible = pila.desapilar()
                partes_disponibles[pila] = parte_disponible
            parte_elegida = piloto.elegir_parte(partes_disponibles) #el piloto elige la parte
            partes_disponibles.pop(parte_elegida)
            partes_reservadas[numero_piloto] = parte_elegida #reserva la parte para el piloto

            for pila, parte in partes_disponibles.items():#devuelve las partes que nadie agarro
                pila.apilar(parte)
    return partes_reservadas









