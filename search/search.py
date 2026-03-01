# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontera=util.Queue()
    visitadas=set()
    estado_inicial=problem.getStartState()
    frontera.push((estado_inicial,[]))
    while not frontera.isEmpty():
        estado_actual,ruta_actual=frontera.pop()
        if problem.isGoalState(estado_actual):
            return ruta_actual
        if estado_actual not in visitadas:
            visitadas.add(estado_actual)
            sucesores=problem.getSuccessors(estado_actual)
            for siguiente_estado,accion,costo in sucesores:
                if siguiente_estado not in visitadas:
                    nueva_ruta=ruta_actual+[accion]
                    frontera.push((siguiente_estado,nueva_ruta))
    return []




def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()



import datetime
import csv
import atexit
import sys

def obtener_laberinto_terminal():
    """
    @brief Obtiene el nombre del laberinto desde los argumentos de la terminal.
    @return str Nombre del laberinto o "Desconocido" si no se encuentra.
    """
    palabras = sys.argv
    for i, palabra in enumerate(palabras):
        # añadimos 'or palabra == "-l"' para que detecte la abreviatura
        if palabra == "--layout" or palabra == "-l":
            if i + 1 < len(palabras):
                return palabras[i + 1]
        elif palabra.startswith("--layout="):
            return palabra.split("=", 1)[1]

    return "Desconocido"


def exploracion():
    """
    @brief Funcion de exploración del laberinto
    @return function getAction devuelve la funcion que determina la accion de Pacman en cada estado
    """
    pasos = 0
    atexit.register(lambda: guardar_registro(pasos, visitadas, tiempo_inicio, laberinto))
    laberinto = obtener_laberinto_terminal()
    tiempo_inicio = datetime.datetime.now()
    historial = []
    visitadas = set()

    def getAction(estado):
        """
        @brief Determina la accion a realizar en cada estado del juego
        @param estado es el estado actual del juego
        @return str devuelve la accion seleccionada
        """
        nonlocal pasos
        pasos += 1
        #gaurdamos la posicion actual
        posicion_actual = estado.getPacmanPosition()
        #la insertamos en visiatadas, evidentemente, ya que estamos en ella
        visitadas.add(posicion_actual)
        #pedimos que acciones puede hacer el pacman en esa posicion: p.e acciones_legales=['North', 'East', 'Stop']
        acciones_legales = estado.getLegalPacmanActions()
        #aqui intentamos a acceder a la primera accion legal posible ->
        accion_elegida = seleccionarAccion(posicion_actual, acciones_legales)
        #si encontramo suna nueva, pues genial, guardamos la que tenmos y devolvemos la nueva, si no pues devolvemos la contraria
        if accion_elegida:
            historial.append(accion_elegida)
            return accion_elegida

        return casillaContraria(acciones_legales)

    def seleccionarAccion(posicion_actual, acciones_legales):
        """
        @brief Selecciona la mejor accion disponible para explorar nuevas areas
        @param posicion_actual posicion actual del Pacman
        @param acciones_legales lista de acciones legales disponibles
        @return str devuelve la accion seleccionada o una lista vacaa si no hay sitios inexplorados
        """
        #si tenemos por ejemplo ['North', 'East', 'Stop'] no se mira oeste, basicamente esta funcion hace que vayamos en orden
        acciones_en_orden = [Directions.WEST,Directions.NORTH, Directions.EAST, Directions.SOUTH]
        for accion in acciones_en_orden:
            if accion in acciones_legales:
                siguiente_posicion = movimientos(posicion_actual, accion)
                if siguiente_posicion not in visitadas:
                    return accion
        return []

    """
            @brief Retrocede cuando no hay movimientos inexplorados disponibles
            @param acciones_legales es una lista de acciones legales en la posicion actual
            @return str devuelve la accion contraria o STOP si no hay opciones
     """
    def casillaContraria(acciones_legales):

        if historial:
            ultima_accion = historial.pop()
            accion_contraria = movimientos(None, ultima_accion, contraria=True)
            if accion_contraria in acciones_legales:
                return accion_contraria
        return Directions.STOP

    def movimientos(posicion, accion, contraria=False):
        """
        @brief Calcula la nueva posicion o devuelve la accion opuesta si es necesario
        @param posicion es la posicion actual
        @param accion es la accion elegida
        @param contraria es un bool que indica si se debe obtener la accion opuesta
        @return tuple devuelve una nueva posicion (x, y) o una accion contraria si se especifica
        """
        listaMovimientos = {
            Directions.NORTH: (0, 1),
            Directions.EAST: (1, 0),
            Directions.SOUTH: (0, -1),
            Directions.WEST: (-1, 0),
        }

        opuestas = {
            Directions.NORTH: Directions.SOUTH,
            Directions.SOUTH: Directions.NORTH,
            Directions.EAST: Directions.WEST,
            Directions.WEST: Directions.EAST,
        }
        if contraria:
            return opuestas.get(accion, Directions.STOP)
        dx, dy = listaMovimientos.get(accion, (0, 0))
        return posicion[0] + dx, posicion[1] + dy

    def guardar_registro(pasos, visitadas, tiempo_inicio, laberinto):
        """
        @brief Guarda los datos de la exploracion en un archivo CSV
        @param pasos es el total de pasos dados
        @param visitadas es el conjunto de casillas exploradas
        @param tiempo_inicio es el iempo al empezar la exploracion
        @param laberinto es el nombre del laberinto elegido
        """
        tiempo_fin = datetime.datetime.now()
        tiempo_transcurrido = (tiempo_fin - tiempo_inicio).total_seconds()
        casillas_exploradas = len(visitadas)
        ratio_repeticion = pasos / casillas_exploradas if casillas_exploradas > 0 else 0

        archivo = "r.csv"
        encabezados = ["Laberinto", "Total de pasos", "Numero de casillas exploradas", "Ratio de repetición", "Coste acumulado"]

        try:
            with open(archivo, "r", encoding="utf-8") as file:
                tiene_datos = bool(file.readline())
        except FileNotFoundError:
            tiene_datos = False

        with open(archivo, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not tiene_datos:
                writer.writerow(encabezados)
            writer.writerow([laberinto, pasos, casillas_exploradas, ratio_repeticion, tiempo_transcurrido])

    return getAction
#prueba
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
exp = exploracion
#python pacman.py -l trickySearch -p AgenteExplorador


