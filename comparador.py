"""
-------------------------------------------------------
PROYECTO: Problema de la Mochila (Knapsack Problem)
-------------------------------------------------------

Archivo:
comparador.py

Descripción:
Este archivo contiene las funciones encargadas de
medir y comparar el rendimiento de los algoritmos
implementados.

Se analizan aspectos como:
- Tiempo de ejecución
- Uso de memoria
- Complejidad algorítmica
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

    inicio = time.time()
    valor, objetos = func(pesos, valores, capacidad)
    fin = time.time()

    memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
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

    resultados = []

    resultados.append(
        medir(
            "GREEDY",
            mochila_greedy,
            pesos,
            valores,
            capacidad,
            "O(n log n)"
        )
    )

    resultados.append(
        medir(
            "PROGRAMACIÓN DINÁMICA",
            mochila_dinamica,
            pesos,
            valores,
            capacidad,
            "O(n·W)"
        )
    )

    resultados.append(
        medir(
            "BACKTRACKING",
            mochila_backtracking,
            pesos,
            valores,
            capacidad,
            "O(2^n)"
        )
    )

    return resultados
def obtener_metricas(resultados):

    nombres = []
    tiempos = []
    memorias = []

    for r in resultados:

        nombres.append(r["nombre"])
        tiempos.append(r["tiempo"])
        memorias.append(r["memoria"])

    return nombres, tiempos, memorias