"""
PROYECTO: Problema de la Mochila (Knapsack Problem)
Archivo: greedy.py
Descripción: Implementación del algoritmo Voraz (Greedy) con visualización de estados.
Complejidad temporal: O(n log n)
"""

def mochila_greedy(pesos, valores, capacidad, callback=None):
    n = len(valores)
    objetos = []

    if callback:
        callback({'tipo': 'inicio', 'algoritmo': 'Greedy', 'capacidad': capacidad, 'pesos': pesos, 'valores': valores})

    for i in range(n):
        if callback:
            callback({'tipo': 'calcula_ratio', 'idx': i, 'peso': pesos[i], 'valor': valores[i]})
        if pesos[i] == 0:
            if valores[i] > 0:
                if callback:
                    callback({'tipo': 'objeto_sin_peso', 'idx': i, 'valor': valores[i]})
            continue
        relacion = valores[i] / pesos[i]
        objetos.append((i, pesos[i], valores[i], relacion))
        if callback:
            callback({'tipo': 'ratio', 'idx': i, 'ratio': relacion})

    objetos.sort(key=lambda x: x[3], reverse=True)

    if callback:
        callback({'tipo': 'ordenado', 'orden': [o[0] for o in objetos]})

    peso_total, valor_total = 0, 0
    seleccionados = []
    descartados = []

    if callback:
        callback({'tipo': 'inicia_seleccion', 'capacidad': capacidad})

    for idx, (indice, peso, valor, _) in enumerate(objetos):
        if callback:
            callback({'tipo': 'evalua', 'idx': indice, 'peso': peso, 'valor': valor, 'peso_restante': capacidad - peso_total})

        if peso_total + peso <= capacidad:
            seleccionados.append(indice)
            peso_total += peso
            valor_total += valor
            if callback:
                callback({'tipo': 'selecciona', 'idx': indice, 'peso': peso, 'valor': valor, 'peso_total': peso_total, 'valor_total': valor_total, 'capacidad': capacidad})
        else:
            descartados.append(indice)
            if callback:
                callback({'tipo': 'descarta', 'idx': indice, 'peso': peso, 'razon': 'excede_capacidad'})

    if callback:
        callback({'tipo': 'fin', 'valor_total': valor_total, 'peso_total': peso_total, 'seleccionados': seleccionados})

    return valor_total, seleccionados