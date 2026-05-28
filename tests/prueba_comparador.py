import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.comparador import comparar_todo

pesos = [2, 3, 4, 5]
valores = [3, 4, 5, 6]
capacidad = 8

comparar_todo(pesos, valores, capacidad)