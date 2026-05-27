# Analizador del Problema de la Mochila

Aplicación de escritorio en **Python** con **CustomTkinter** para comparar tres algoritmos clásicos del Knapsack Problem.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Tkinter](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)

## Algoritmos Comparados

| Algoritmo | Complejidad | Tipo |
|-----------|-------------|------|
| Greedy | O(n log n) | Aproximado |
| Programación Dinámica | O(n·W) | Óptimo |
| Backtracking | O(2^n) | Exacto |

## Instalación

```bash
pip install customtkinter matplotlib
python main.py
```

## Uso

1. Ingresar capacidad de la mochila
2. Ingresar pesos separados por coma (ej: `2,3,4,5`)
3. Ingresar valores separados por coma (ej: `3,4,5,6`)
4. Seleccionar algoritmo o "Comparar todos"
5. Click en **EJECUTAR**

## Estructura

```
├── main.py           # GUI (CustomTkinter + Matplotlib)
├── greedy.py         # Algoritmo voraz
├── dinamica.py       # Programación dinámica
├── backtracking.py   # Backtracking exhaustivo
├── comparador.py      # Métricas de rendimiento
└── requirements.txt  # Dependencias
```

## Métricas

- Tiempo de ejecución (segundos)
- Uso de memoria pico (KB)
- Complejidad algorítmica teórica
