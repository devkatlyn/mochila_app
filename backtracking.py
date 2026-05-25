"""
-------------------------------------------------------
PROYECTO: Problema de la Mochila (Knapsack Problem)
-------------------------------------------------------

Archivo:
backtracking.py

Descripción:
Este archivo contiene la implementación del algoritmo
Backtracking para resolver el Problema de la Mochila.

El algoritmo explora todas las combinaciones posibles
de objetos para encontrar la solución óptima sin
superar la capacidad máxima de la mochila.

Paradigma utilizado:
Backtracking / Fuerza Bruta

Complejidad temporal:
O(2^n)
"""

def mochila_backtracking(pesos, valores, capacidad):

    n = len(pesos)

    mejor_valor = 0
    mejor_comb = []

    def explorar(i, peso_actual, valor_actual, seleccionados):

        nonlocal mejor_valor, mejor_comb

        # Si ya superó capacidad, se descarta
        if peso_actual > capacidad:
            return

        # Si llegamos al final de los objetos
        if i == n:

            if valor_actual > mejor_valor:
                mejor_valor = valor_actual
                mejor_comb = seleccionados.copy()

            return

        # Caso 1: NO tomar el objeto i
        explorar(
            i + 1,
            peso_actual,
            valor_actual,
            seleccionados
        )

        # Caso 2: SÍ tomar el objeto i
        seleccionados.append(i)

        explorar(
            i + 1,
            peso_actual + pesos[i],
            valor_actual + valores[i],
            seleccionados
        )

        seleccionados.pop()

    explorar(0, 0, 0, [])

    return mejor_valor, mejor_comb