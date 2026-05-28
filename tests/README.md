# Pruebas

Este directorio contiene scripts de prueba independientes para validar el funcionamiento de cada algoritmo del problema de la mochila.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `prueba_greedy.py` | Prueba del algoritmo voraz |
| `prueba_dinamica.py` | Prueba de programación dinámica |
| `prueba_backtracking.py` | Prueba de backtracking |
| `prueba_comparador.py` | Prueba del comparador de algoritmos |

## Datos de Prueba

Todos los scripts usan el mismo conjunto de datos para facilitar la comparación:

```python
pesos = [2, 3, 4, 5]
valores = [3, 4, 5, 6]
capacidad = 8
```

## Ejecución

Desde la raíz del proyecto:

```bash
python tests/prueba_greedy.py
python tests/prueba_dinamica.py
python tests/prueba_backtracking.py
python tests/prueba_comparador.py
```

## Resultados Esperados

### Greedy
```
Valor máximo obtenido: 7
Objetos seleccionados: Objeto 1, Objeto 2
Peso total utilizado: 5 kg
```

**Nota**: Greedy no garantiza la solución óptima. Selecciona objetos por ratio valor/peso.

---

### Programación Dinámica
```
Valor máximo obtenido: 10
Objetos seleccionados: Objeto 2, Objeto 4
Peso total utilizado: 8 kg
```

**Nota**: DP garantiza la solución óptima.

---

### Backtracking
```
Valor máximo obtenido: 10
Objetos seleccionados: Objeto 2, Objeto 4
Peso total utilizado: 8 kg
```

**Nota**: Backtracking garantiza la solución óptima (igual que DP).

---

### Comparador

El comparador ejecuta los tres algoritmos y muestra:
- Valor obtenido por cada algoritmo
- Tiempo de ejecución (segundos)
- Uso de memoria (KB)
- Complejidad teórica

**Ejemplo de salida**:
```
GREEDY
  Valor: 7 | Objetos: Objeto 1, Objeto 2
  Tiempo: 0.000045s | Memoria: 0.12 KB
  Complejidad: O(n log n)

PROGRAMACIÓN DINÁMICA
  Valor: 10 | Objetos: Objeto 2, Objeto 4
  Tiempo: 0.000234s | Memoria: 1.05 KB
  Complejidad: O(n·W)

BACKTRACKING
  Valor: 10 | Objetos: Objeto 2, Objeto 4
  Tiempo: 0.000156s | Memoria: 0.89 KB
  Complejidad: O(2^n)
```

---

## Validación

Las pruebas validan:
- **Correctitud**: el algoritmo retorna el valor y objetos esperados
- **Consistencia**: DP y Backtracking deben dar el mismo resultado (óptimo)
- **Rendimiento**: el comparador mide tiempo y memoria para análisis comparativo

---

## Notas

- Los scripts son independientes y no requieren la GUI
- Cada prueba imprime resultados en consola de forma legible
- No hay dependencias externas más allá de los módulos del proyecto
- Los resultados pueden variar ligeramente en tiempo de ejecución según el sistema

---

## Agregar Nuevas Pruebas

Para agregar una nueva prueba:

1. Crear un archivo `prueba_<nombre>.py` en este directorio
2. Importar el módulo correspondiente:
   ```python
   from src.greedy import mochila_greedy
   ```
3. Definir datos de prueba y ejecutar el algoritmo
4. Imprimir resultados de forma clara
5. Ejecutar desde la raíz: `python tests/prueba_<nombre>.py`
