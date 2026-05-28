"""
PROYECTO: Problema de la Mochila (Knapsack Problem)
Archivo: dinamica.py
Descripción: Implementación de Programación Dinámica con visualización de estados.
Complejidad temporal: O(n * W)
"""

def mochila_dinamica(pesos, valores, capacidad, callback=None):
    n = len(valores)

    if callback:
        callback({'tipo': 'inicio', 'algoritmo': 'Dinámica', 'n': n, 'W': capacidad, 'pesos': pesos, 'valores': valores})

    if capacidad <= 0:
        if callback:
            callback({'tipo': 'fin', 'valor_total': 0, 'seleccionados': []})
        return 0, []

    dp = [[0 for x in range(capacidad + 1)] for x in range(n + 1)]

    for i in range(1, n + 1):
        if callback:
            callback({'tipo': 'inicia_fila', 'fila': i, 'objeto': i-1, 'peso': pesos[i-1], 'valor': valores[i-1]})
        for w in range(capacidad + 1):
            if pesos[i - 1] <= w:
                anterior = dp[i - 1][w]
                con_objeto = valores[i - 1] + dp[i - 1][w - pesos[i - 1]]
                dp[i][w] = max(con_objeto, anterior)
                if callback:
                    callback({
                        'tipo': 'celda',
                        'fila': i, 'col': w,
                        'valor': dp[i][w],
                        'anterior': anterior,
                        'con_objeto': con_objeto,
                        'actualizada': dp[i][w] != anterior
                    })
            else:
                dp[i][w] = dp[i - 1][w]
                if callback:
                    callback({'tipo': 'celda', 'fila': i, 'col': w, 'valor': dp[i][w], 'anterior': dp[i-1][w], 'actualizada': False})

    objetos = []
    w = capacidad

    if callback:
        callback({'tipo': 'inicia_reconstruccion'})

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            objetos.append(i - 1)
            if callback:
                callback({'tipo': 'reconstruye', 'idx': i-1, 'peso': pesos[i-1], 'valor': valores[i-1], 'w_restante': w})
            w -= pesos[i - 1]

    if callback:
        callback({'tipo': 'fin', 'valor_total': dp[n][capacidad], 'seleccionados': objetos[::-1]})

    return dp[n][capacidad], objetos[::-1]