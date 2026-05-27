"""
PROYECTO: Problema de la Mochila (Knapsack Problem)
Archivo: greedy.py
Descripción: Implementación del algoritmo Voraz (Greedy) para resolver el
            Problema de la Mochila. Selecciona objetos según la mejor relación
            valor/peso para maximizar el valor sin superar la capacidad.
Complejidad temporal: O(n log n)
"""

def mochila_greedy(pesos, valores, capacidad):
    n = len(valores)
    objetos = []

    for i in range(n):
        if pesos[i] == 0:  # Objeto sin peso: incluir si tiene valor
            if valores[i] > 0:
                seleccionados.append(i)
                valor_total += valores[i]
            continue
        relacion = valores[i] / pesos[i]  # Relación valor/peso
        objetos.append((i, pesos[i], valores[i], relacion))

    objetos.sort(key=lambda x: x[3], reverse=True)  # Ordenar por mejor relación

    peso_total, valor_total, seleccionados = 0, 0, []

    for indice, peso, valor, _ in objetos:
        if peso_total + peso <= capacidad:  # Cabe en la mochila
            seleccionados.append(indice)
            peso_total += peso
            valor_total += valor

    return valor_total, seleccionados