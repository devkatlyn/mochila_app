import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.dinamica import mochila_dinamica

pesos = [2, 3, 4, 5]
valores = [3, 4, 5, 6]
capacidad = 8

valor_maximo, objetos = mochila_dinamica(
    pesos,
    valores,
    capacidad
)

print("\nRESULTADOS \n")

print(f"Capacidad máxima de la mochila: {capacidad} kg\n")

print("Objetos disponibles:\n")

for i in range(len(pesos)):
    print(
        f"Objeto {i + 1}: "
        f"Peso = {pesos[i]} kg | "
        f"Valor = {valores[i]}"
    )

print("\nObjetos seleccionados:\n")

peso_total = 0

for i in objetos:

    print(
        f"Objeto {i + 1}: "
        f"Peso = {pesos[i]} kg | "
        f"Valor = {valores[i]}"
    )

    peso_total += pesos[i]

print("\n-----------------------------\n")

print(f"Peso total utilizado: {peso_total} kg")
print(f"Valor máximo obtenido: {valor_maximo}")

