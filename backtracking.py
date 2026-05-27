"""
PROYECTO: Problema de la Mochila (Knapsack Problem)
Archivo: backtracking.py
Descripción: Implementación de Backtracking con visualización de estados.
Complejidad temporal: O(2^n)
"""

def mochila_backtracking(pesos, valores, capacidad, callback=None):
    n = len(pesos)
    mejor_valor, mejor_comb = 0, []

    def explorar(i, peso_actual, valor_actual, seleccionados, nivel=0, camino=None):
        nonlocal mejor_valor, mejor_comb
        if camino is None:
            camino = []

        if callback:
            callback({
                'tipo': 'nodo',
                'nivel': nivel,
                'idx': i,
                'peso_actual': peso_actual,
                'valor_actual': valor_actual,
                'seleccionados': seleccionados.copy(),
                'camino': camino.copy()
            })

        if peso_actual > capacidad:
            if callback:
                callback({
                    'tipo': 'poda',
                    'nivel': nivel,
                    'idx': i,
                    'peso': peso_actual,
                    'capacidad': capacidad
                })
            return

        if i == n:
            if valor_actual > mejor_valor:
                mejor_valor, mejor_comb = valor_actual, seleccionados.copy()
                if callback:
                    callback({
                        'tipo': 'nueva_mejor',
                        'nivel': nivel,
                        'valor': valor_actual,
                        'seleccionados': seleccionados.copy(),
                        'peso': peso_actual
                    })
            return

        if callback:
            callback({
                'tipo': 'explora_rama',
                'nivel': nivel,
                'idx': i,
                'accion': 'izquierda',
                'texto': f'No incluir Obj{i+1}',
                'peso_actual': peso_actual,
                'valor_actual': valor_actual
            })
        explorar(i + 1, peso_actual, valor_actual, seleccionados.copy(), nivel + 1, camino + [('izq', i)])

        if callback:
            callback({
                'tipo': 'explora_rama',
                'nivel': nivel,
                'idx': i,
                'accion': 'derecha',
                'texto': f'Incluir Obj{i+1}',
                'peso_actual': peso_actual + pesos[i],
                'valor_actual': valor_actual + valores[i]
            })
        seleccionados.append(i)
        explorar(i + 1, peso_actual + pesos[i], valor_actual + valores[i], seleccionados, nivel + 1, camino + [('der', i)])
        seleccionados.pop()

    if callback:
        callback({'tipo': 'inicio', 'algoritmo': 'Backtracking', 'n_objetos': n, 'capacidad': capacidad})

    explorar(0, 0, 0, [])

    if callback:
        callback({
            'tipo': 'fin',
            'valor_total': mejor_valor,
            'seleccionados': mejor_comb,
            'combinaciones_exploradas': 2 ** n
        })

    return mejor_valor, mejor_comb