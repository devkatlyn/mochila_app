"""
PROYECTO: Problema de la Mochila (Knapsack Problem)
Archivo: backtracking.py
Descripción: Implementación de Backtracking para resolver el Problema de la
            Mochila. Explora todas las combinaciones posibles para encontrar
            la solución óptima.
Complejidad temporal: O(2^n)
"""

def mochila_backtracking(pesos, valores, capacidad):
    n = len(pesos)
    mejor_valor, mejor_comb = 0, []

    def explorar(i, peso_actual, valor_actual, seleccionados):
        nonlocal mejor_valor, mejor_comb
        if peso_actual > capacidad:  # Poda: superó capacidad
            return
        if i == n:  # Procesó todos los objetos
            if valor_actual > mejor_valor:  # Mejores solución encontrada
                mejor_valor, mejor_comb = valor_actual, seleccionados.copy()
            return

        explorar(i + 1, peso_actual, valor_actual, seleccionados)  # No tomar
        seleccionados.append(i)  # Intentar tomar objeto i
        explorar(i + 1, peso_actual + pesos[i], valor_actual + valores[i], seleccionados)
        seleccionados.pop()  # Backtrack: deshacer selección

    explorar(0, 0, 0, [])
    return mejor_valor, mejor_comb