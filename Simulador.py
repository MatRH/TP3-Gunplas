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
from TP3 import Gunpla, Esqueleto, Parte, Arma, Piloto
from operator import itemgetter
from math import fabs

def armar_equipos(lista_pilotos, cantidad_equipos):
    '''Recibe una lista de pilotos de la cual elige para armar equipos y una
    cantidad de equipos a armar, divide a los pilotos equitativamente de manera
    que halla la misma cantidad de pilotos por equipo; si esto no fuera posible
    debido a que la cantidad de pilotos no fuera divisible por la cantidad de
    equipos, se le pedira al usuario que agregue la cantidad necesaria de pilotos
    para completar el equipo o en caso de que el usuario no ingrese nada se
    autocompletaran los equipos con un piloto al azar de la biblioteca de
    pilotos BOT.
    Devuelve una lista de listas, donde cada sub_lista representa un equipo,
    y Cada elemento es un piloto
    '''
    lista_equipos = []
    pilotos_bot = [Piloto(), Piloto()]
    pilotos = lista_pilotos[:]

    while (len(pilotos) % cantidad_equipos) != 0:
        pilotos.append(random.choice(pilotos_bot))

    cantidad_pilotos = len(pilotos)
    while pilotos:
        equipo = []
        for i in range(int((cantidad_pilotos / cantidad_equipos))):
            piloto = pilotos.pop(pilotos.index(random.choice(pilotos)))
            equipo.append(piloto)
        lista_equipos.append(equipo)
    return lista_equipos

def asignar_gunplas(lista_equipos):
    '''Recibe la lista de equipos y le asigna un gunpla a cada piloto.
    '''
    for equipo in lista_equipos:
        for piloto in equipo:
            gunpla = Gunpla()
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
    while len(lista_esqueletos) < cantidad:
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
            esqueleto_elegido = piloto.elegir_esqueleto(lista_esqueletos)
            piloto.get_gunpla()._set_esqueleto(esqueleto_elegido)

def generar_armas(cantidad, daño,hits,precision,peso,armadura,escudo,velocidad,energia):
    '''Recibe la cantidad de armas a generar, el daño,hits(cantidad de veces que puede atacar
    en el mismo turno),precision ,peso , armadura, energia, escudo y velocidad maximos.
     Devuelve la lista de armas generadas.
    '''
    lista_armas = []
    while len(lista_armas) < cantidad:
        arma                = Arma()
        arma.daño           = random.randint(1, daño)
        arma.hits           = random.randint(1, hits )
        arma.precision      = random.randint(0,precision )
        arma.peso           = random.randint(1,peso)
        arma.energia        = random.randint(-energia, energia)
        arma.armadura       = random.randint(-armadura , armadura)
        arma.escudo         = random.randint(-escudo , escudo)
        arma.velocidad      = random.randint(-velocidad, velocidad)
        arma.tipo_parte     = 'Arma'
        arma.tipo_municion  = random.choice(('FISICA', 'LASER', 'HADRON'))
        arma.tipo_arma      = random.choice(('MELEE', 'RANGO'))
        arma.clase          = "#generador de nombres"
        lista_armas.append(arma)
    return lista_armas

def generar_partes(cantidad, peso, armadura, escudo, velocidad, energia, prob_armas, cant_max_armas):
    '''Recibe la cantidad de partes a generar, el peso , armadura, energia, escudo ,velocidad maximos,
    la probabilidad de que la parte contenga armas y la cantidad maxima de armas que puede tener una parte.
    Devuelve la lista de partes generadas.
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
        parte.tipo_parte         = "Nombre arma"#generador de nombres
        if random.randint(0,100) > prob_armas:
            cantidad_armas = random.randint(1,cant_max_armas)
            parte.armas.append(generar_armas(cantidad_armas,200,2,90,10,10,10,50,10)) #se pueden cambiar los valores para que genere armas distintas dentro de las partes
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
            partes_disponibles.pop(index(parte_elegida))
            partes_reservadas[numero_piloto] = parte_elegida #reserva la parte para el piloto

            for pila, parte in partes_disponibles.items():#devuelve las partes que nadie agarro
                pila.apilar(parte)
    return partes_reservadas

def elegir_partes(ronda, partes_reservadas):
    '''Recibe la ronda de pilotos y un diccionario de partes reservadas, donde
    el numero asignado previamente a cada piloto es la clave y el valor son
    las partes que este piloto reservó.
    Devuelve un diccionario donde las claves son el numero de piloto y los
    valores son las partes que eligió ese piloto'''
    partes_armar_gunplas = {}
    for numero_piloto, piloto in ronda:
        partes_utilizar = piloto.elegir_combinacion(partes_reservadas[numero_piloto])
        partes_armar_gunplas[numero_piloto] = partes_utilizar
    return partes_armar_gunplas

def equipar_gunplas(ronda, partes_armar_gunplas):
    '''Recibe la ronda de pilotos y un diccionario de partes para armar los
    Gunplas de cada piloto, donde las claves son el número de piloto y los
    valores son las partes que este piloto eligió'''
    for numero_piloto, piloto in ronda:
        lista_armas = []
        lista_partes = partes_armar_gunplas[numero_piloto][:]
        for parte in lista_partes:
            if parte.get_tipo_parte() == 'Arma':
                lista_armas.append(lista_partes.pop(lista_partes.index(parte)))
        piloto._set_partes(lista_partes)
        piloto._set_armas(lista_armas)

def armar_cola_turnos(ronda):
    '''Recibe la ronda de pilotos y los organiza según sus velocidades.
    Devuelve una cola de pilotos ordenados según velocidades decrecientes.
    '''
    cola_turnos = Cola()
    pilotos_velocidad = sorted(ronda, key= itemgetter(2).get_velocidad()) #itemgetter devuelve el segundo elemento de la tupla
    for numero_piloto, piloto in pilotos_velocidad:
        cola_turnos.encolar(piloto)
    return cola_turnos

def esta_activo(piloto):
    '''Recibe un piloto y evalua si este esta activo. Se considera activo cuando tiene energia mayor a 0.
        Devuelve True si esta activo, False si no lo esta.
    '''
    return (piloto.get_gunpla().get_energia() > 0)

def cantidad_equipos_activos(lista_equipos):
    '''Recibe la lista de equipos y devuelve la cantidad de equipos con al menos un Gunpla activo.
    '''
    equipos_activos = 0
    for equipo in lista_equipos:
        for piloto in equipo:
            if esta_activo(piloto):
                equipos_activos += 1
                break
    return equipos_activos

def generar_lista_oponentes(lista_equipos,piloto):
    '''Recibe una lista de equipos y un piloto y devuelve la lista de oponentes.
    '''
    lista_oponentes = []
    for equipo in lista_equipos:
        if piloto not in equipo:
            for oponente in equipo:
                lista_oponentes.append(oponente)
    return lista_oponentes

def calcular_daño(arma):
    '''Calcula el daño realizado por un arma.
    '''
    daño = 0
    for hits in range (arma.get_hits()):
        chance_hit = randint(0,100)
        if arma.get_precision() >= chance_hit:
            daño += arma.get_daño()
        if (arma.get_precision()/4) >= chance_hit:
            daño += arma.get_daño() * 1.5
        else:
            daño += 0

def reduccion_daño(arma, gunpla, daño):
    '''Recibe un arma a utilizar contra el Gunpla, un Gunpla y el daño ejercido
    por el arma, y calcula según el
    tipo de municion que utiliza el arma, la cantidad de daño reducido por las
    defensas del Gunpla y devuelve el valor del daño reducido'''
    municion = arma.get_tipo_municion()
    if municion == 'FISICA':
        daño_reducido = daño - gunpla.get_armadura()
    if municion == 'LASER':
        daño_reducido = daño - (daño * gunpla.get_escudo())
    else:#para cuando ejerce daño verdadero
        daño_reducido = daño
    return daño_reducido

def filtrar_armas_combinables(arma, gunpla):
    '''Recibe un arma utilizada por un Piloto y el Gunpla del piloto y devuelve
    una lista con las posibles armas de las que puede elegir ese piloto para
    volver a combinar su ataque'''
    tipo = arma.get_tipo()
    municion = arma.get_tipo_municion()
    clase = arma.get_clase()
    armas_adosadas = gunpla.get_armamento()
    armas_disponibles = []
    for arma in armas_adosadas:
        if arma.esta_lista():
            if arma.get_tipo() == tipo or arma.get_tipo_municion() == municion or arma.get_clase() == clase:
                armas_disponibles.append(arma)
    return armas_disponibles

def combate(atacante, defensor, arma, contraataque):
    '''Recibe el piloto atacante, el piloto defensor, el arma inicial con la
    que piloto comenzó el ataque y un valor booleano que representa si el
    ataque fue(True) o no (False) un contraataque.
    Devuelve el daño realizado por el atacante al defensor durante el combate
    '''
    daño = reduccion_daño(arma, defensor, calcular_daño(arma))
    defensor.get_gunpla()._aplicar_daño(daño)
    tipo_arma = arma.get_tipo()
    chance_combinar = randint(0,100)

    if contraataque: #contraataque es un booleano que indica si es o no un contraataque
        return

    if tipo_arma == 'MELEE' and chance_combinar > 40: #combina el arma con otra
        armas_disponibles = filtrar_armas_combinables(arma, atacante.get_gunpla())
        arma_combinada = atacante.elegir_arma(armas_disponibles)
        combate(atacante, defensor, arma_combinada, contraataque)

    if tipo_arma == 'RANGO' and chance_combinar > 25: #combina el arma con otra
        armas_disponibles = filtrar_armas_combinables(arma, atacante.get_gunpla())
        arma_combinacion = atacante.elegir_arma(oponente)
        combate(atacante, defensor, arma_combinada, contraataque)

    if tipo_arma == 'MELEE':
        defensor.elegir_arma(atacante)
        combate(defensor, combate, arma_defensor, True)

    if not contraataque:
        return daño

def ciclo_de_juego(lista_equipos,cola_turnos):
    '''
    '''
    indice_equipo = 0

    while cantidad_equipos_activos(lista_equipos) >= 2: #ciclo de juego
        piloto = cola_turnos.desencolar()
        if esta_activo(piloto):
            lista_oponentes = generar_lista_oponentes(piloto)
            indice_oponente = piloto.elegir_oponente(lista_oponentes)
            oponente = lista_oponentes[indice_oponente].get_gunpla
            arma_elegida    = piloto.elegir_arma(oponente)
            daño_aplicado = combate(piloto, lista_oponentes[indice_oponente], arma_elegida, False)

        if daño_aplicado == 0:
            cola_turnos.encolar(oponente) #es un turno extra

        if oponente.get_energia_restante() < 0  and abs(oponente.get_energia_restante()) > 5:
            cola_turnos.encolar(piloto) #es un turno extra

        cola_turnos.encolar(piloto)#se encola un turno para el piloto

    for equipo in lista_equipos: #devuelve el equipo y pilotos ganadores
        indice_equipo += 1
        for piloto in equipo:
            if piloto.get_gunpla().get_energia_restante() > 0:
                print ('Equipo ganador {}'.format(indice_equipo))
                pilotos_ganadores.append(piloto)

    for piloto in pilotos_ganadores:
        print ('Pilto ganador: {}'.format(piloto))
        print ('Con su Gunpla: {}'.format(piloto.get_gunpla()))

def main():
    lista_pilotos = [Piloto(), Piloto(), Piloto(), Piloto()]
    lista_equipos = armar_equipos(lista_pilotos, 2)
    asignar_gunplas(lista_equipos)   #asigna un Gunpla a cada Piloto
    lista_esqueletos = generar_esqueletos(10, 200, 200, 200, 4)
    asignar_esqueletos(lista_esqueletos, lista_equipos)
    lista_armas = generar_armas(20, 750 , 5 , 90 , 100 , 50 , 50 , 100 , 50)
    lista_partes = generar_partes(50, 200 , 200 , 200, 300, 200, 30 , 4)#los stats de las armas generadas dentro de las partes se cambian desde dentro de la funcion generar_partes
    lista_pilas = separar_en_pilas(lista_armas, lista_partes)
    ronda = armar_ronda(lista_equipos)
    partes_reservadas = reservar_partes(lista_pilas, ronda)
    partes_armar_gunplas = elegir_partes(ronda, partes_reservadas)
    equipar_gunplas(ronda, partes_armar_gunplas) #Le asigna al piloto de cada gunpla sus partes y armas
    cola_turnos = armar_cola_turnos(ronda)
    ciclo_de_juego(lista_equipos, cola_turnos)

main()
