# Módulo de Algoritmos

Este directorio contiene las implementaciones de los tres algoritmos para resolver el problema de la mochila (Knapsack Problem), junto con utilidades para medir su rendimiento.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `greedy.py` | Algoritmo voraz (aproximado) |
| `dinamica.py` | Programación dinámica (óptimo) |
| `backtracking.py` | Backtracking exhaustivo (exacto) |
| `comparador.py` | Utilidades para medir tiempo y memoria |

---

## 1. Greedy (Algoritmo Voraz)

**Archivo**: `greedy.py`  
**Complejidad**: O(n log n)  
**Tipo**: Aproximado

### ¿Cómo funciona?

Imagina que tienes una mochila con capacidad limitada y varios objetos, cada uno con un peso y un valor. El algoritmo greedy toma decisiones "codiciosas" en cada paso: siempre elige el objeto que le da más valor por cada kilogramo de peso.

**Ejemplo intuitivo**: Si tienes 3 objetos:
- Objeto A: pesa 2 kg, vale 10 puntos → 5 puntos/kg
- Objeto B: pesa 3 kg, vale 12 puntos → 4 puntos/kg  
- Objeto C: pesa 4 kg, vale 8 puntos → 2 puntos/kg

El algoritmo primero calcula la "eficiencia" de cada objeto (valor/peso), los ordena de mayor a menor eficiencia, y luego los va metiendo en la mochila mientras quepan. En este caso, elegiría A primero, luego B, y si queda espacio, intentaría con C.

**Limitación**: Aunque es muy rápido, no siempre encuentra la mejor solución posible. A veces, elegir un objeto menos eficiente pero más pequeño permite meter otro objeto que en conjunto da más valor total.

### Explicación técnica

El algoritmo sigue estos pasos:

1. **Cálculo de ratios**: Para cada objeto `i`, calcula `ratio[i] = valores[i] / pesos[i]`
2. **Ordenamiento**: Ordena los objetos de mayor a menor ratio usando `sort()` con complejidad O(n log n)
3. **Selección greedy**: Itera por los objetos ordenados y los agrega a la mochila si caben:
   ```
   si peso_actual + peso[i] <= capacidad:
       seleccionar objeto i
       peso_actual += peso[i]
       valor_actual += valor[i]
   ```
4. **Descarte**: Si un objeto no cabe, se descarta y se continúa con el siguiente

**Pseudocódigo**:
```
funcion mochila_greedy(pesos, valores, capacidad):
    objetos = []
    para cada i en 0..n-1:
        ratio = valores[i] / pesos[i]
        objetos.agregar((i, pesos[i], valores[i], ratio))
    
    objetos.ordenar_por(ratio, descendente)
    
    peso_total = 0
    valor_total = 0
    seleccionados = []
    
    para cada (indice, peso, valor, _) en objetos:
        si peso_total + peso <= capacidad:
            seleccionados.agregar(indice)
            peso_total += peso
            valor_total += valor
    
    retornar valor_total, seleccionados
```

### Uso

```python
from src.greedy import mochila_greedy

valor, objetos = mochila_greedy(pesos, valores, capacidad, callback=None)
```

**Parámetros**:
- `pesos`: lista de pesos de los objetos (todos > 0)
- `valores`: lista de valores de los objetos (todos > 0)
- `capacidad`: capacidad máxima de la mochila (> 0)
- `callback`: función opcional para visualización de estados

**Retorna**:
- `valor`: valor total obtenido (no necesariamente óptimo)
- `objetos`: lista de índices de objetos seleccionados

---

## 2. Programación Dinámica

**Archivo**: `dinamica.py`  
**Complejidad**: O(n·W) donde W es la capacidad  
**Tipo**: Óptimo

### ¿Cómo funciona?

La programación dinámica resuelve problemas dividiéndolos en subproblemas más pequeños y guardando las soluciones para no recalcularlas. En el problema de la mochila, construimos una tabla donde cada celda responde a la pregunta: "¿Cuál es el máximo valor que puedo obtener usando los primeros `i` objetos con una capacidad de `w` kilogramos?"

**Ejemplo intuitivo**: Imagina que tienes una tabla con filas (objetos) y columnas (capacidades desde 0 hasta la capacidad máxima). Para cada celda, decides:
- ¿Incluyo este objeto o no?
- Si lo incluyo, ¿cuánto valor gano comparado con no incluirlo?

Vas llenando la tabla fila por fila, y al final, la celda inferior derecha contiene la respuesta óptima. Luego "reconstruyes" la solución recorriendo la tabla hacia atrás para ver qué objetos elegiste.

**Ventaja**: Siempre encuentra la solución óptima, a diferencia del greedy.

**Desventaja**: Usa mucha memoria (una tabla de tamaño n×W) y puede ser lento si la capacidad W es muy grande.

### Explicación técnica

El algoritmo construye una tabla DP de dimensiones `(n+1) × (W+1)`:

1. **Inicialización**: `dp[0][w] = 0` para todo `w` (con 0 objetos, el valor es 0)

2. **Llenado de la tabla**: Para cada objeto `i` (de 1 a n) y cada capacidad `w` (de 0 a W):
   ```
   si pesos[i-1] <= w:
       dp[i][w] = max(
           dp[i-1][w],                           # no incluir objeto i
           valores[i-1] + dp[i-1][w - pesos[i-1]] # incluir objeto i
       )
   sino:
       dp[i][w] = dp[i-1][w]  # no cabe, copiar valor anterior
   ```

3. **Reconstrucción**: Empezando desde `dp[n][W]`, recorremos hacia atrás:
   ```
   w = W
   para i desde n hasta 1:
       si dp[i][w] != dp[i-1][w]:
           objeto i fue seleccionado
           w = w - pesos[i-1]
   ```

**Pseudocódigo**:
```
funcion mochila_dinamica(pesos, valores, capacidad):
    n = longitud(valores)
    dp = matriz de (n+1) filas × (capacidad+1) columnas, inicializada en 0
    
    para i desde 1 hasta n:
        para w desde 0 hasta capacidad:
            si pesos[i-1] <= w:
                dp[i][w] = max(
                    dp[i-1][w],
                    valores[i-1] + dp[i-1][w - pesos[i-1]]
                )
            sino:
                dp[i][w] = dp[i-1][w]
    
    # Reconstrucción
    objetos = []
    w = capacidad
    para i desde n hasta 1:
        si dp[i][w] != dp[i-1][w]:
            objetos.agregar(i-1)
            w = w - pesos[i-1]
    
    retornar dp[n][capacidad], objetos.invertir()
```

### Uso

```python
from src.dinamica import mochila_dinamica

valor, objetos = mochila_dinamica(pesos, valores, capacidad, callback=None)
```

**Parámetros**:
- `pesos`: lista de pesos de los objetos (todos > 0)
- `valores`: lista de valores de los objetos (todos > 0)
- `capacidad`: capacidad máxima de la mochila (> 0)
- `callback`: función opcional para visualización de estados

**Retorna**:
- `valor`: valor total óptimo (garantizado)
- `objetos`: lista de índices de objetos seleccionados

---

## 3. Backtracking

**Archivo**: `backtracking.py`  
**Complejidad**: O(2^n)  
**Tipo**: Exacto

### ¿Cómo funciona?

El backtracking explora sistemáticamente todas las combinaciones posibles de objetos (incluir o no incluir cada uno) y se queda con la mejor solución encontrada. Es como probar todas las posibilidades, pero con una optimización: si en algún momento te das cuenta de que una combinación ya excede la capacidad de la mochila, "podas" esa rama y no sigas explorando por ahí.

**Ejemplo intuitivo**: Imagina un árbol de decisiones donde en cada nivel decides si incluyes o no un objeto:
- Nivel 0: ¿Incluyo el objeto 1? (sí/no)
- Nivel 1: ¿Incluyo el objeto 2? (sí/no)
- Nivel 2: ¿Incluyo el objeto 3? (sí/no)
- ...

Cada camino desde la raíz hasta una hoja representa una combinación de objetos. El algoritmo recorre todo el árbol, pero cuando el peso acumulado supera la capacidad, deja de explorar esa rama (poda). Al final, compara todas las soluciones válidas y se queda con la de mayor valor.

**Ventaja**: Siempre encuentra la solución óptima (es exhaustivo).

**Desventaja**: Es muy lento para muchos objetos. Con 20 objetos, hay más de 1 millón de combinaciones posibles.

### Explicación técnica

El algoritmo usa recursión para explorar un árbol binario de decisiones:

1. **Función recursiva `explorar(i, peso_actual, valor_actual, seleccionados)`**:
   - `i`: índice del objeto actual a decidir
   - `peso_actual`: peso acumulado de los objetos seleccionados
   - `valor_actual`: valor acumulado de los objetos seleccionados
   - `seleccionados`: lista de índices de objetos incluidos hasta ahora

2. **Casos base**:
   - **Poda**: Si `peso_actual > capacidad`, esta rama es inválida → retornar
   - **Hoja**: Si `i == n`, hemos decidido sobre todos los objetos:
     - Si `valor_actual > mejor_valor`, actualizar la mejor solución

3. **Ramas recursivas**:
   - **No incluir objeto i**: `explorar(i+1, peso_actual, valor_actual, seleccionados)`
   - **Incluir objeto i**: 
     ```
     seleccionados.agregar(i)
     explorar(i+1, peso_actual + pesos[i], valor_actual + valores[i], seleccionados)
     seleccionados.quitar_ultimo()  # backtrack
     ```

**Pseudocódigo**:
```
funcion mochila_backtracking(pesos, valores, capacidad):
    n = longitud(pesos)
    mejor_valor = 0
    mejor_comb = []
    
    funcion explorar(i, peso_actual, valor_actual, seleccionados):
        si peso_actual > capacidad:
            retornar  # poda
        
        si i == n:
            si valor_actual > mejor_valor:
                mejor_valor = valor_actual
                mejor_comb = seleccionados.copiar()
            retornar
        
        # Rama izquierda: no incluir objeto i
        explorar(i+1, peso_actual, valor_actual, seleccionados)
        
        # Rama derecha: incluir objeto i
        seleccionados.agregar(i)
        explorar(i+1, peso_actual + pesos[i], valor_actual + valores[i], seleccionados)
        seleccionados.quitar_ultimo()  # backtrack
    
    explorar(0, 0, 0, [])
    retornar mejor_valor, mejor_comb
```

### Uso

```python
from src.backtracking import mochila_backtracking

valor, objetos = mochila_backtracking(pesos, valores, capacidad, callback=None, max_estados=500)
```

**Parámetros**:
- `pesos`: lista de pesos de los objetos (todos > 0)
- `valores`: lista de valores de los objetos (todos > 0)
- `capacidad`: capacidad máxima de la mochila (> 0)
- `callback`: función opcional para visualización de estados
- `max_estados`: límite de estados visuales generados (default: 500)

**Retorna**:
- `valor`: valor total óptimo (garantizado)
- `objetos`: lista de índices de objetos seleccionados

**Nota**: Para n > 15 objetos, la visualización se trunca automáticamente a 500 estados para evitar congelar la interfaz.

---

## Comparador

**Archivo**: `comparador.py`

Mide y compara el rendimiento de los tres algoritmos en términos de tiempo de ejecución y uso de memoria.

### ¿Cómo funciona?

El comparador ejecuta cada algoritmo con los mismos datos de entrada y mide:
- **Tiempo de ejecución**: usando `time.perf_counter()` para alta precisión
- **Memoria pico**: usando `tracemalloc` para rastrear asignaciones de memoria

Luego devuelve una lista con las métricas de cada algoritmo para facilitar la comparación.

### Uso

```python
from src.comparador import comparar_todo

resultados = comparar_todo(pesos, valores, capacidad)
```

**Retorna**: lista de diccionarios con métricas:
```python
[
    {
        "nombre": "GREEDY",
        "valor": 10,
        "objetos": "Objeto 1, Objeto 2",
        "tiempo": 0.000123,      # segundos
        "memoria": 0.45,         # KB
        "complejidad": "O(n log n)"
    },
    {
        "nombre": "PROGRAMACIÓN DINÁMICA",
        "valor": 10,
        "objetos": "Objeto 2, Objeto 4",
        "tiempo": 0.000456,
        "memoria": 1.23,
        "complejidad": "O(n·W)"
    },
    {
        "nombre": "BACKTRACKING",
        "valor": 10,
        "objetos": "Objeto 2, Objeto 4",
        "tiempo": 0.000789,
        "memoria": 0.89,
        "complejidad": "O(2^n)"
    }
]
```

---

## Validación de Entradas

Todos los algoritmos validan internamente:
- `capacidad > 0`: si no, retornan `(0, [])` inmediatamente
- `pesos > 0`: validado en la GUI antes de llamar a los algoritmos
- `valores > 0`: validado en la GUI antes de llamar a los algoritmos

Si se llaman directamente sin pasar por la GUI, los algoritmos se protegen contra capacidades inválidas, pero asumen que los pesos y valores son positivos.

---

## Callbacks

Los callbacks son funciones opcionales que reciben un diccionario con el estado actual del algoritmo. Se usan para visualización en tiempo real en la GUI.

### Ejemplo de callback

```python
def mi_callback(estado):
    print(estado)

mochila_greedy([2, 3], [4, 5], 8, callback=mi_callback)
```

### Tipos de estados

| Tipo | Algoritmo | Descripción |
|------|-----------|-------------|
| `inicio` | Todos | Algoritmo iniciado con parámetros |
| `calcula_ratio` | Greedy | Calculando ratio valor/peso para objeto i |
| `ratio` | Greedy | Ratio calculado para objeto i |
| `ordenado` | Greedy | Objetos ordenados por ratio |
| `inicia_seleccion` | Greedy | Iniciando fase de selección |
| `evalua` | Greedy | Evaluando si incluir objeto i |
| `selecciona` | Greedy | Objeto i seleccionado |
| `descarta` | Greedy | Objeto i descartado (no cabe) |
| `inicia_fila` | Dinámica | Iniciando fila i de la tabla DP |
| `celda` | Dinámica | Celda (i, w) de la tabla DP actualizada |
| `inicia_reconstruccion` | Dinámica | Iniciando reconstrucción de solución |
| `reconstruye` | Dinámica | Objeto i identificado como parte de la solución |
| `nodo` | Backtracking | Nodo del árbol de decisión explorado |
| `poda` | Backtracking | Rama podada (excede capacidad) |
| `explora_rama` | Backtracking | Explorando rama izquierda/derecha |
| `nueva_mejor` | Backtracking | Nueva mejor solución encontrada |
| `fin` | Todos | Algoritmo finalizado con resultado |

---

## Uso desde la GUI

La GUI (`main.py`) importa estos módulos automáticamente:

```python
from src.greedy import mochila_greedy
from src.dinamica import mochila_dinamica
from src.backtracking import mochila_backtracking
from src.comparador import comparar_todo
```

No es necesario importarlos manualmente al ejecutar la aplicación.
