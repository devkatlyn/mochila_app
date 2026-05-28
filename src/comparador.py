import timeit
import tracemalloc
from src.greedy import mochila_greedy
from src.dinamica import mochila_dinamica
from src.backtracking import mochila_backtracking


REPETICIONES_POR_ALGORITMO = {
    "GREEDY": 10000,
    "PROGRAMACIÓN DINÁMICA": 1000,
    "BACKTRACKING": 100,
}


def formatear_objetos(objetos):
    return ", ".join([f"Objeto {i+1}" for i in objetos])


def medir(nombre, func, pesos, valores, capacidad, complejidad):
    repeticiones = REPETICIONES_POR_ALGORITMO.get(nombre, 1000)

    # 1. Medir tiempo con timeit (7 repeticiones, toma la mejor)
    timer = timeit.Timer(lambda: func(pesos, valores, capacidad))
    tiempos = timer.repeat(repeat=7, number=repeticiones)
    mejor_tiempo = min(tiempos) / repeticiones

    # 2. Medir memoria por separado (sin interferir con el tiempo)
    tracemalloc.start()
    valor, objetos = func(pesos, valores, capacidad)
    _, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "nombre": nombre,
        "valor": valor,
        "objetos": formatear_objetos(objetos),
        "tiempo": mejor_tiempo,
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