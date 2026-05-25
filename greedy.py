"""
-------------------------------------------------------
PROYECTO: Problema de la Mochila (Knapsack Problem)
-------------------------------------------------------

Archivo:
greedy.py

Descripción:
Este archivo contiene la implementación del algoritmo
Voraz (Greedy) para resolver el Problema de la Mochila.

El algoritmo selecciona los objetos según la mejor
relación valor/peso para intentar maximizar el valor
total sin superar la capacidad de la mochila.

Paradigma utilizado:
Algoritmo Voraz (Greedy)

Complejidad temporal:
O(n log n)
"""

def mochila_greedy(pesos, valores, capacidad):

    n = len(valores)

    # Crear lista de objetos
    objetos = []

    for i in range(n):

        relacion = valores[i] / pesos[i]

        objetos.append(
            (i, pesos[i], valores[i], relacion)
        )

    # Ordenar por mejor relación valor/peso
    objetos.sort(key=lambda x: x[3], reverse=True)

    peso_total = 0
    valor_total = 0

    seleccionados = []

    for objeto in objetos:

        indice, peso, valor, _ = objeto

        if peso_total + peso <= capacidad:

            seleccionados.append(indice)

            peso_total += peso
            valor_total += valor

    return valor_total, seleccionados