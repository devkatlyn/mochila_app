"""
PROYECTO: Problema de la Mochila (Knapsack Problem)
Archivo: dinamica.py
Descripción: Implementación del algoritmo de Programación Dinámica para resolver
            el Problema de la Mochila. Busca maximizar el valor sin superar
            la capacidad usando tabla de subproblemas.
Complejidad temporal: O(n * W)
"""

def mochila_dinamica(pesos, valores, capacidad):
    n = len(valores)
    dp = [[0 for x in range(capacidad + 1)] for x in range(n + 1)]  # Tabla DP

    for i in range(1, n + 1):  # Llenar tabla iterativamente
        for w in range(capacidad + 1):
            if pesos[i - 1] <= w:  # Objeto cabe: elegir mejor opción
                dp[i][w] = max(valores[i - 1] + dp[i - 1][w - pesos[i - 1]], dp[i - 1][w])
            else:  # Objeto no cabe
                dp[i][w] = dp[i - 1][w]

    objetos = []  # Reconstruir objetos seleccionados
    w = capacidad
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:  # Este objeto fue seleccionado
            objetos.append(i - 1)
            w -= pesos[i - 1]

    return dp[n][capacidad], objetos[::-1]  # Invertir para orden original