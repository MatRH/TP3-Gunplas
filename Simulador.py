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
    '''
    lista_esqueletos = []
    while len(esqueletos) < cantidad:
        esqueleto = Esqueleto()
        esqueleto.velocidad = random.randint(-velocidad_max, velocidad_max)
        esqueleto.energia = random.randint(0, energia_max)
        esqueleto.movilidad = random.randint(100, movilidad_max)
        esqueleto.slots = random.randint(0, slots_max)
        lista_esqueletos.append(esqueleto)
