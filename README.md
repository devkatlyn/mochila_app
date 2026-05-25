# 🧠 Analizador del Problema de la Mochila (Knapsack Problem)

Una aplicación de escritorio interactiva construida en **Python** utilizando **CustomTkinter** que permite comparar de forma visual tres paradigmas clásicos de programación para resolver el problema de la mochila (*Knapsack Problem*).

El software calcula los objetos seleccionados para maximizar el valor dentro del límite de peso de la mochila, midiendo y graficando métricas de rendimiento en tiempo real.

---

## 🚀 Características

*   **Interfaz de Usuario Premium**: Diseño tipo Dashboard moderno con soporte completo para modo oscuro (Slate-Dark Theme).
*   **Paradigmas Comparados**:
    *   **Algoritmo Greedy (Voraz)**: Rápido y aproximado, de complejidad $O(n \log n)$.
    *   **Programación Dinámica**: Óptimo y preciso, de complejidad $O(n \cdot W)$.
    *   **Backtracking (Vuelta Atrás)**: Solución exhaustiva exacta, de complejidad $O(2^n)$.
*   **Consola de Resultados Coloreada**: Reportes interactivos con código de colores (verdes para éxitos, azules para datos clave, amarillos para advertencias).
*   **Métricas de Rendimiento Integradas**:
    *   Tiempo exacto de ejecución (segundos).
    *   Consumo de memoria RAM pico (KB).
    *   Complejidad algorítmica teórica.
*   **Visualización Directa**: Gráficas comparativas integradas en el panel principal (lado a lado) utilizando **Matplotlib** adaptado al modo oscuro de la aplicación.

---

## 🛠️ Tecnologías Utilizadas

*   **Lenguaje**: Python 3.x
*   **Interfaz Gráfica**: CustomTkinter
*   **Gráficos**: Matplotlib
*   **Medición**: `tracemalloc` (uso de memoria) y `time` (tiempos de ejecución)

---

## 💻 Instalación y Ejecución

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

### 1. Clonar o descargar el repositorio
Descarga este repositorio en tu computadora.

### 2. Crear y activar un entorno virtual (Opcional pero recomendado)
En la terminal del proyecto, ejecuta:
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar en Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Instalar Dependencias
Instala los paquetes necesarios de interfaz gráfica y visualización:
```powershell
pip install customtkinter matplotlib
```

### 4. Ejecutar la Aplicación
Inicia el programa con:
```powershell
python main.py
```

---

## 📊 Vista de la Aplicación

Al seleccionar **"Comparar todos"**, el panel derecho mostrará un reporte detallado del rendimiento de cada algoritmo junto a dos gráficos comparativos integrados en el dashboard:
1. **Tiempo de Ejecución** (segundos de procesador empleados).
2. **Uso de Memoria** (kilobytes acumulados).
