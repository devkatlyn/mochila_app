"""
PROYECTO: Problema de la Mochila (Knapsack Problem)
Archivo: backtracking.py
Descripción: Implementación de Backtracking con visualización de estados.
Complejidad temporal: O(2^n)
"""

def mochila_backtracking(pesos, valores, capacidad, callback=None, max_estados=500):
    n = len(pesos)
    mejor_valor, mejor_comb = 0, []
    estados_generados = 0
    truncado = False

    def explorar(i, peso_actual, valor_actual, seleccionados, nivel=0, camino=None):
        nonlocal mejor_valor, mejor_comb, estados_generados, truncado
        if camino is None:
            camino = []

        if callback:
            if estados_generados < max_estados:
                callback({
                    'tipo': 'nodo',
                    'nivel': nivel,
                    'idx': i,
                    'peso_actual': peso_actual,
                    'valor_actual': valor_actual,
                    'seleccionados': seleccionados.copy(),
                    'camino': camino.copy()
                })
                estados_generados += 1
            else:
                truncado = True

        if peso_actual > capacidad:
            if callback and estados_generados < max_estados:
                callback({
                    'tipo': 'poda',
                    'nivel': nivel,
                    'idx': i,
                    'peso': peso_actual,
                    'capacidad': capacidad
                })
                estados_generados += 1
            return

        if i == n:
            if valor_actual > mejor_valor:
                mejor_valor, mejor_comb = valor_actual, seleccionados.copy()
                if callback and estados_generados < max_estados:
                    callback({
                        'tipo': 'nueva_mejor',
                        'nivel': nivel,
                        'valor': valor_actual,
                        'seleccionados': seleccionados.copy(),
                        'peso': peso_actual
                    })
                    estados_generados += 1
            return

        if callback and estados_generados < max_estados:
            callback({
                'tipo': 'explora_rama',
                'nivel': nivel,
                'idx': i,
                'accion': 'izquierda',
                'texto': f'No incluir Obj{i+1}',
                'peso_actual': peso_actual,
                'valor_actual': valor_actual
            })
            estados_generados += 1
        explorar(i + 1, peso_actual, valor_actual, seleccionados.copy(), nivel + 1, camino + [('izq', i)])

        if callback and estados_generados < max_estados:
            callback({
                'tipo': 'explora_rama',
                'nivel': nivel,
                'idx': i,
                'accion': 'derecha',
                'texto': f'Incluir Obj{i+1}',
                'peso_actual': peso_actual + pesos[i],
                'valor_actual': valor_actual + valores[i]
            })
            estados_generados += 1
        seleccionados.append(i)
        explorar(i + 1, peso_actual + pesos[i], valor_actual + valores[i], seleccionados, nivel + 1, camino + [('der', i)])
        seleccionados.pop()

    if callback:
        callback({'tipo': 'inicio', 'algoritmo': 'Backtracking', 'n_objetos': n, 'capacidad': capacidad})
        estados_generados += 1

    if capacidad <= 0:
        if callback:
            callback({
                'tipo': 'fin',
                'valor_total': 0,
                'seleccionados': [],
                'combinaciones_exploradas': 0,
                'truncado': False
            })
        return 0, []

    explorar(0, 0, 0, [])

    if callback:
        callback({
            'tipo': 'fin',
            'valor_total': mejor_valor,
            'seleccionados': mejor_comb,
            'combinaciones_exploradas': 2 ** n,
            'truncado': truncado
        })

    return mejor_valor, mejor_comb
