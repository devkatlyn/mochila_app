"""
-------------------------------------------------------
PROYECTO: Problema de la Mochila (Knapsack Problem)
-------------------------------------------------------

Archivo:
dinamica.py

Descripción:
Este archivo contiene la implementación del algoritmo
de Programación Dinámica para resolver el Problema
de la Mochila.

El algoritmo busca maximizar el valor total de los
objetos seleccionados sin superar la capacidad máxima
de la mochila.

Paradigma utilizado:
Programación Dinámica

Complejidad temporal:
O(n * W)
-------------------------------------------------------
"""
def mochila_dinamica(pesos, valores, capacidad):
    
    n = len(valores)

    # Crear tabla
    dp = [[0 for x in range(capacidad + 1)] for x in range(n + 1)]

    # Llenar tabla
    for i in range(1, n + 1):
        for w in range(capacidad + 1):

            if pesos[i - 1] <= w:
                dp[i][w] = max(
                    valores[i - 1] + dp[i - 1][w - pesos[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruir objetos seleccionados
    objetos = []
    w = capacidad

    for i in range(n, 0, -1):

        if dp[i][w] != dp[i - 1][w]:
            objetos.append(i - 1)
            w -= pesos[i - 1]

    objetos.reverse()

    return dp[n][capacidad], objetos
