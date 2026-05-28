"""
PROYECTO: Problema de la Mochila (Knapsack Problem)
Archivo: comparador.py
Descripción: Funciones para medir y comparar el rendimiento de los algoritmos.
            Analiza tiempo de ejecución, uso de memoria y complejidad.
"""

import time
import tracemalloc
from greedy import mochila_greedy
from dinamica import mochila_dinamica
from backtracking import mochila_backtracking


def formatear_objetos(objetos):
    return ", ".join([f"Objeto {i+1}" for i in objetos])


def medir(nombre, func, pesos, valores, capacidad, complejidad):
    tracemalloc.start()
    inicio = time.perf_counter()
    valor, objetos = func(pesos, valores, capacidad)
    fin = time.perf_counter()
    _, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "nombre": nombre,
        "valor": valor,
        "objetos": formatear_objetos(objetos),
        "tiempo": fin - inicio,
        "memoria": memoria_pico / 1024,
        "complejidad": complejidad
    }


def comparar_todo(pesos, valores, capacidad):
    resultados = [
        medir("GREEDY", mochila_greedy, pesos, valores, capacidad, "O(n log n)"),
        medir("PROGRAMACIÓN DINÁMICA", mochila_dinamica, pesos, valores, capacidad, "O(n·W)"),
        medir("BACKTRACKING", mochila_backtracking, pesos, valores, capacidad, "O(2^n)")
    ]
    return resultados