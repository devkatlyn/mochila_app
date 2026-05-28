from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tkinter import Canvas, END
import math

from src.greedy import mochila_greedy
from src.dinamica import mochila_dinamica
from src.backtracking import mochila_backtracking
from src.comparador import comparar_todo

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

VELOCIDAD_GREEDY = 40  # ms entre frames
VELOCIDAD_BACKTRACKING = 50
MAX_NODOS_POR_NIVEL = 30
COLORES = {
    'bg': '#0f172a',
    'panel': '#1e293b',
    'texto': '#f8fafc',
    'muted': '#64748b',
    'azul': '#3b82f6',
    'verde': '#34d399',
    'rojo': '#ef4444',
    'amarillo': '#fbbf24',
    'cyan': '#38bdf8',
    'naranja': '#f97316',
}


class Visualizador:
    def __init__(self, canvas):
        self.canvas = canvas
        self.estados = []
        self.animando = False
        self.objetos_rects = []
        self.objetos_labels = []
        self.seleccionados_rects = []
        self.descartados_rects = []
        self.dp_celdas = {}
        self.bt_nodos = {}
        self.bt_lineas = []
        self.capacidad_bar = None
        self.titulo_id = None
        self.info_id = None
        self.estado_id = None
        self.leyenda_ids = []
        self.sel_y = 0
        self.desc_y = 0
        self.tipo_algoritmo = 'greedy'
        self.velocidad = VELOCIDAD_GREEDY

    def limpiar(self):
        self.canvas.delete("all")
        self.estados = []
        self.animando = False
        self.objetos_rects = []
        self.objetos_labels = []
        self.seleccionados_rects = []
        self.descartados_rects = []
        self.dp_celdas = {}
        self.bt_nodos = {}
        self.bt_lineas = []
        self.capacidad_bar = None
        self.titulo_id = None
        self.info_id = None
        self.estado_id = None
        self.leyenda_ids = []
        self.sel_y = 0
        self.desc_y = 0
        self.tipo_algoritmo = 'greedy'
        self.velocidad = VELOCIDAD_GREEDY

    def agregar_estado(self, estado):
        self.estados.append(estado)

    def iniciar_animacion(self):
        if not self.estados:
            return
        self.animando = True
        self._indice = 0
        self._animar_siguiente()

    def _animar_siguiente(self):
        if not self.animando or self._indice >= len(self.estados):
            self.animando = False
            return
        estado = self.estados[self._indice]
        self._indice += 1
        self._procesar_estado(estado)
        self.canvas.after(self.velocidad, self._animar_siguiente)

    def _procesar_estado(self, estado):
        tipo = estado.get('tipo', '')

        if tipo == 'inicio':
            self._dibujar_inicio(estado)
        elif tipo == 'calcula_ratio':
            self._resaltar_objeto(estado['idx'], COLORES['amarillo'])
        elif tipo == 'ratio':
            self._actualizar_ratio(estado['idx'], estado['ratio'])
        elif tipo == 'ordenado':
            self._animar_ordenamiento(estado['orden'])
        elif tipo == 'evalua':
            self._resaltar_objeto(estado['idx'], COLORES['cyan'])
            self._actualizar_info(f"Evaluando Objeto {estado['idx']+1} (peso={estado['peso']}, valor={estado['valor']})")
        elif tipo == 'selecciona':
            self._marcar_seleccionado(estado['idx'])
            self._actualizar_barra(estado['peso_total'], estado.get('capacidad', 0))
            self._actualizar_info(f"Objeto {estado['idx']+1} SELECCIONADO (peso={estado['peso']}, valor={estado['valor']})")
        elif tipo == 'descarta':
            self._marcar_descartado(estado['idx'])
            self._actualizar_info(f"Objeto {estado['idx']+1} DESCARTADO ({estado['razon']})")
        elif tipo == 'fin':
            self._dibujar_fin(estado)
        elif tipo == 'celda':
            self._resaltar_celda(estado['fila'], estado['col'], estado['valor'], estado.get('actualizada', False))
        elif tipo == 'inicia_fila':
            self._actualizar_info(f"Fila {estado['fila']}: Objeto {estado['objeto']+1} (peso={estado['peso']}, valor={estado['valor']})")
        elif tipo == 'inicia_reconstruccion':
            self._actualizar_info("Reconstruyendo solucion...")
        elif tipo == 'reconstruye':
            self._resaltar_celda_reconstruida()
        elif tipo == 'nodo':
            self._dibujar_nodo_bt(estado)
        elif tipo == 'poda':
            self._marcar_poda(estado)
        elif tipo == 'explora_rama':
            self._dibujar_rama_bt(estado)
        elif tipo == 'nueva_mejor':
            self._marcar_mejor_solucion(estado)
        elif tipo == 'inicia_seleccion':
            self._actualizar_info("Iniciando seleccion de objetos...")

    def _dibujar_inicio(self, estado):
        w = self.canvas.winfo_width()
        algoritmo = estado.get('algoritmo', '')
        self.tipo_algoritmo = algoritmo.lower()
        if self.tipo_algoritmo == 'backtracking':
            self.velocidad = VELOCIDAD_BACKTRACKING
        else:
            self.velocidad = VELOCIDAD_GREEDY

        self.canvas.create_text(w // 2, 20, text=f"{algoritmo.upper()}",
                                font=("Segoe UI", 16, "bold"), fill=COLORES['azul'], tags="titulo")
        self.info_id = self.canvas.create_text(w // 2, 50, text="Iniciando...",
                                                font=("Consolas", 11), fill=COLORES['texto'], tags="info")

        if algoritmo == 'Greedy':
            self._init_greedy(estado)
        elif algoritmo == 'Dinámica':
            self._init_dinamica(estado)
        elif algoritmo == 'Backtracking':
            self._init_backtracking(estado)

    def _actualizar_info(self, texto):
        if self.info_id:
            self.canvas.itemconfig(self.info_id, text=texto)

    def _init_greedy(self, estado):
        w = self.canvas.winfo_width()
        pesos = estado.get('pesos', [])
        valores = estado.get('valores', [])
        capacidad = estado.get('capacidad', 0)
        n = len(pesos)
        if n == 0:
            return

        obj_w = min(90, (w - 80) // n - 8)
        obj_h = 65
        start_x = (w - (obj_w + 8) * n) // 2
        y = 85

        self.objetos_rects = []
        self.objetos_labels = []

        for i in range(n):
            x = start_x + i * (obj_w + 8)
            rect = self.canvas.create_rectangle(x, y, x + obj_w, y + obj_h,
                                                 fill=COLORES['panel'], outline=COLORES['muted'], width=2,
                                                 tags=f"obj_{i}")
            self.objetos_rects.append(rect)

            self.canvas.create_text(x + obj_w // 2, y + 15, text=f"Obj {i+1}",
                                     font=("Segoe UI", 9, "bold"), fill=COLORES['texto'], tags=f"obj_label_{i}")
            self.canvas.create_text(x + obj_w // 2, y + 32, text=f"P:{pesos[i]}  V:{valores[i]}",
                                     font=("Consolas", 8), fill=COLORES['muted'], tags=f"obj_info_{i}")
            ratio_text = self.canvas.create_text(x + obj_w // 2, y + 50, text="",
                                                   font=("Consolas", 8), fill=COLORES['amarillo'], tags=f"obj_ratio_{i}")
            self.objetos_labels.append(ratio_text)

        bar_y = y + obj_h + 25
        self.canvas.create_text(40, bar_y + 10, text="Cap:", font=("Segoe UI", 9, "bold"),
                                 fill=COLORES['texto'], anchor="w")
        self.capacidad_bar_bg = self.canvas.create_rectangle(85, bar_y + 2, w - 40, bar_y + 18,
                                                              fill=COLORES['bg'], outline=COLORES['muted'], width=1)
        self.capacidad_bar = self.canvas.create_rectangle(85, bar_y + 2, 85, bar_y + 18,
                                                           fill=COLORES['verde'], outline="")
        self.capacidad_text = self.canvas.create_text(w // 2, bar_y + 10, text=f"0 / {capacidad} kg",
                                                       font=("Consolas", 8), fill=COLORES['texto'])

        self.sel_y = bar_y + 40
        self.canvas.create_text(40, self.sel_y, text="Seleccionados:", font=("Segoe UI", 9, "bold"),
                                 fill=COLORES['verde'], anchor="w", tags="sel_label")

        self.desc_y = self.sel_y + 30
        self.canvas.create_text(40, self.desc_y, text="Descartados:", font=("Segoe UI", 9, "bold"),
                                 fill=COLORES['rojo'], anchor="w", tags="desc_label")

    def _resaltar_objeto(self, idx, color):
        if idx < len(self.objetos_rects):
            self.canvas.itemconfig(self.objetos_rects[idx], outline=color, width=3)

    def _actualizar_ratio(self, idx, ratio):
        if idx < len(self.objetos_labels):
            self.canvas.itemconfig(self.objetos_labels[idx], text=f"R:{ratio:.2f}")

    def _animar_ordenamiento(self, orden):
        pass

    def _marcar_seleccionado(self, idx):
        if idx < len(self.objetos_rects):
            self.canvas.itemconfig(self.objetos_rects[idx], fill='#1a3a2a', outline=COLORES['verde'], width=3)

    def _marcar_descartado(self, idx):
        if idx < len(self.objetos_rects):
            self.canvas.itemconfig(self.objetos_rects[idx], fill='#3a1a1a', outline=COLORES['rojo'], width=3)
            rect = self.objetos_rects[idx]
            coords = self.canvas.coords(rect)
            if len(coords) == 4:
                x1, y1, x2, y2 = coords
                self.canvas.create_line(x1, y1, x2, y2, fill=COLORES['rojo'], width=2, tags="desc_line")
                self.canvas.create_line(x1, y2, x2, y1, fill=COLORES['rojo'], width=2, tags="desc_line")

    def _actualizar_barra(self, peso_actual, capacidad):
        if capacidad <= 0:
            return
        w = self.canvas.winfo_width()
        bar_width = (w - 130) * (peso_actual / capacidad)
        self.canvas.coords(self.capacidad_bar, 85, self.canvas.coords(self.capacidad_bar)[1],
                           85 + bar_width, self.canvas.coords(self.capacidad_bar)[3])
        color = COLORES['verde'] if peso_actual <= capacidad else COLORES['rojo']
        self.canvas.itemconfig(self.capacidad_bar, fill=color)
        self.canvas.itemconfig(self.capacidad_text, text=f"{peso_actual} / {capacidad} kg")

    def _dibujar_fin(self, estado):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        valor = estado.get('valor_total', 0)
        peso = estado.get('peso_total', 0)
        seleccionados = estado.get('seleccionados', [])

        self._actualizar_info(f"FINALIZADO - Valor: {valor} | Peso: {peso}")

        if self.tipo_algoritmo == 'greedy':
            y = self.desc_y + 30
        else:
            y = h - 80

        x = 40
        for idx in seleccionados:
            self.canvas.create_rectangle(x, y, x + 55, y + 22, fill=COLORES['verde'],
                                          outline=COLORES['texto'], width=1, tags="sel_item")
            self.canvas.create_text(x + 27, y + 11, text=f"Obj{idx+1}",
                                     font=("Segoe UI", 8, "bold"), fill=COLORES['texto'], tags="sel_item")
            x += 62

        self.canvas.create_text(w // 2, y + 40, text=f"VALOR MAXIMO: {valor}",
                                 font=("Segoe UI", 13, "bold"), fill=COLORES['amarillo'], tags="resultado")

    def _init_dinamica(self, estado):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        n = estado.get('n', 0)
        W = estado.get('W', 0)
        pesos = estado.get('pesos', [])
        valores = estado.get('valores', [])

        if n == 0 or W == 0:
            return

        cell_w = min(45, (w - 120) // (W + 1))
        cell_h = min(30, (h - 200) // (n + 1))
        start_x = 80
        start_y = 90

        self.dp_celdas = {}
        self.dp_cell_w = cell_w
        self.dp_cell_h = cell_h
        self.dp_start_x = start_x
        self.dp_start_y = start_y

        for j in range(W + 1):
            x = start_x + j * cell_w
            self.canvas.create_text(x + cell_w // 2, start_y - 15, text=str(j),
                                     font=("Consolas", 8), fill=COLORES['muted'])
        for i in range(n + 1):
            y = start_y + i * cell_h
            label = f"Obj{i}" if i > 0 else "0"
            self.canvas.create_text(start_x - 25, y + cell_h // 2, text=label,
                                     font=("Consolas", 8), fill=COLORES['muted'])

        for i in range(n + 1):
            for j in range(W + 1):
                x = start_x + j * cell_w
                y = start_y + i * cell_h
                rect = self.canvas.create_rectangle(x, y, x + cell_w, y + cell_h,
                                                     fill=COLORES['bg'], outline=COLORES['muted'], width=1)
                text = self.canvas.create_text(x + cell_w // 2, y + cell_h // 2, text="0",
                                                font=("Consolas", 8), fill=COLORES['texto'])
                self.dp_celdas[(i, j)] = (rect, text)

        self.canvas.create_text(w // 2, start_y + (n + 1) * cell_h + 30, text="Reconstruyendo...",
                                 font=("Segoe UI", 10), fill=COLORES['cyan'], tags="reconstruccion", state="hidden")

    def _resaltar_celda(self, fila, col, valor, actualizada):
        if (fila, col) in self.dp_celdas:
            rect, text = self.dp_celdas[(fila, col)]
            color = COLORES['amarillo'] if actualizada else COLORES['panel']
            self.canvas.itemconfig(rect, fill=color, outline=COLORES['azul'], width=2)
            self.canvas.itemconfig(text, text=str(valor))

    def _resaltar_celda_reconstruida(self):
        for (fila, col), (rect, text) in self.dp_celdas.items():
            current_fill = self.canvas.itemcget(rect, "fill")
            if current_fill == COLORES['amarillo']:
                self.canvas.itemconfig(rect, fill=COLORES['panel'], outline=COLORES['muted'], width=1)

    def _init_backtracking(self, estado):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        n = estado.get('n_objetos', 0)

        self.bt_node_r = 16
        self.bt_v_gap = 50
        self.bt_start_x = w // 2
        self.bt_start_y = 80
        self.bt_nodos = {}
        self.bt_lineas = []
        self.bt_nivel_count = {}
        self.bt_canvas_w = w
        self.bt_canvas_h = h

        raiz = self.canvas.create_oval(
            self.bt_start_x - self.bt_node_r, self.bt_start_y - self.bt_node_r,
            self.bt_start_x + self.bt_node_r, self.bt_start_y + self.bt_node_r,
            fill=COLORES['azul'], outline=COLORES['texto'], width=2, tags="bt_raiz"
        )
        raiz_text = self.canvas.create_text(self.bt_start_x, self.bt_start_y, text="R",
                                             font=("Segoe UI", 9, "bold"), fill=COLORES['texto'])
        self.bt_nodos[(0, 0)] = (raiz, raiz_text, self.bt_start_x, self.bt_start_y)

        self.canvas.create_text(w // 2, h - 30, text="Verde=Seleccionado  Rojo=Podado  Dorado=Mejor",
                                 font=("Segoe UI", 9), fill=COLORES['muted'])

    def _dibujar_nodo_bt(self, estado):
        nivel = estado['nivel']
        idx = estado['idx']

        if nivel not in self.bt_nivel_count:
            self.bt_nivel_count[nivel] = 0
        count = self.bt_nivel_count[nivel]
        self.bt_nivel_count[nivel] += 1

        if count >= MAX_NODOS_POR_NIVEL:
            return

        total_at_level = min(2 ** nivel, MAX_NODOS_POR_NIVEL)
        margin = 30
        spread = (self.bt_canvas_w - 2 * margin) / (total_at_level + 1)
        x = margin + (count + 0.5) * spread
        y = self.bt_start_y + nivel * self.bt_v_gap

        r = self.bt_node_r
        rect = self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                         fill=COLORES['panel'], outline=COLORES['muted'], width=2)
        text = self.canvas.create_text(x, y, text=f"{idx+1}",
                                         font=("Segoe UI", 8, "bold"), fill=COLORES['texto'])
        self.bt_nodos[(nivel, count)] = (rect, text, x, y)

        if nivel > 0:
            padre_nivel = nivel - 1
            padre_idx = count // 2
            if (padre_nivel, padre_idx) in self.bt_nodos:
                _, _, px, py = self.bt_nodos[(padre_nivel, padre_idx)]
                linea = self.canvas.create_line(px, py + self.bt_node_r, x, y - r,
                                                 fill=COLORES['muted'], width=2, tags="bt_linea")
                self.bt_lineas.append(linea)

    def _dibujar_rama_bt(self, estado):
        nivel = estado['nivel']
        count = self.bt_nivel_count.get(nivel, 0) - 1
        if count < MAX_NODOS_POR_NIVEL and (nivel, count) in self.bt_nodos:
            rect, text, x, y = self.bt_nodos[(nivel, count)]
            self.canvas.itemconfig(rect, outline=COLORES['amarillo'], width=3)

    def _marcar_poda(self, estado):
        nivel = estado['nivel']
        count = self.bt_nivel_count.get(nivel, 0) - 1
        if count < MAX_NODOS_POR_NIVEL and (nivel, count) in self.bt_nodos:
            rect, text, x, y = self.bt_nodos[(nivel, count)]
            self.canvas.itemconfig(rect, fill='#3a1a1a', outline=COLORES['rojo'], width=3)
            self.canvas.create_line(x - 8, y - 8, x + 8, y + 8,
                                     fill=COLORES['rojo'], width=2, tags="poda_x")
            self.canvas.create_line(x - 8, y + 8, x + 8, y - 8,
                                     fill=COLORES['rojo'], width=2, tags="poda_x")

    def _marcar_mejor_solucion(self, estado):
        nivel = estado['nivel']
        valor = estado['valor']
        for key, (rect, text, x, y) in self.bt_nodos.items():
            if key[0] == nivel:
                self.canvas.itemconfig(rect, fill='#3a3a1a', outline=COLORES['amarillo'], width=3)
                self.canvas.create_text(x, y - 22, text=f"★ {valor}",
                                         font=("Segoe UI", 8, "bold"), fill=COLORES['amarillo'], tags="mejor")
                break


class MochilaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Analizador del Problema de la Mochila")
        self.geometry("1200x720")
        self.minsize(1100, 650)
        self.configure(fg_color=COLORES['bg'])

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self._crear_sidebar()
        self._crear_main_panel()

    def _crear_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=15, fg_color=COLORES['panel'])
        self.sidebar.grid(row=0, column=0, sticky="nswe", padx=(15, 0), pady=15)

        self.title_label = ctk.CTkLabel(self.sidebar, text="ANALIZADOR DEL PROBLEMA\nDE LA MOCHILA",
                                         font=("Segoe UI", 18, "bold"), text_color=COLORES['azul'])
        self.title_label.pack(pady=(30, 10))

        self.subtitle = ctk.CTkLabel(self.sidebar, text="Comparacion de paradigmas\nde programacion",
                                      font=("Segoe UI", 12), text_color=COLORES['muted'])
        self.subtitle.pack(pady=(0, 20))

        self.capacidad_label = ctk.CTkLabel(self.sidebar, text="Capacidad de la mochila",
                                             font=("Segoe UI", 12, "bold"), text_color="#cbd5e1")
        self.capacidad_label.pack(anchor="w", padx=20)
        self.capacidad_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 8", height=40,
                                             fg_color=COLORES['bg'], border_color="#334155",
                                             text_color="#f8fafc", placeholder_text_color=COLORES['muted'],
                                             corner_radius=8)
        self.capacidad_entry.pack(fill="x", padx=20, pady=(5, 12))

        self.pesos_label = ctk.CTkLabel(self.sidebar, text="Pesos",
                                         font=("Segoe UI", 12, "bold"), text_color="#cbd5e1")
        self.pesos_label.pack(anchor="w", padx=20)
        self.pesos_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 2,3,4,5", height=40,
                                         fg_color=COLORES['bg'], border_color="#334155",
                                         text_color="#f8fafc", placeholder_text_color=COLORES['muted'],
                                         corner_radius=8)
        self.pesos_entry.pack(fill="x", padx=20, pady=(5, 12))

        self.valores_label = ctk.CTkLabel(self.sidebar, text="Valores",
                                           font=("Segoe UI", 12, "bold"), text_color="#cbd5e1")
        self.valores_label.pack(anchor="w", padx=20)
        self.valores_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 3,4,5,6", height=40,
                                           fg_color=COLORES['bg'], border_color="#334155",
                                           text_color="#f8fafc", placeholder_text_color=COLORES['muted'],
                                           corner_radius=8)
        self.valores_entry.pack(fill="x", padx=20, pady=(5, 20))

        self.algoritmo_label = ctk.CTkLabel(self.sidebar, text="Selecciona un algoritmo",
                                             font=("Segoe UI", 14, "bold"), text_color="#f8fafc")
        self.algoritmo_label.pack(anchor="w", padx=20, pady=(5, 10))
        self.algoritmo = ctk.StringVar(value="dinamica")

        self.greedy_radio = ctk.CTkRadioButton(self.sidebar, text="Greedy (Voraz)",
                                                 variable=self.algoritmo, value="greedy",
                                                 font=("Segoe UI", 12), text_color="#cbd5e1",
                                                 fg_color=COLORES['azul'], hover_color="#1d4ed8")
        self.greedy_radio.pack(anchor="w", padx=20, pady=5)

        self.dp_radio = ctk.CTkRadioButton(self.sidebar, text="Programacion Dinamica",
                                             variable=self.algoritmo, value="dinamica",
                                             font=("Segoe UI", 12), text_color="#cbd5e1",
                                             fg_color=COLORES['azul'], hover_color="#1d4ed8")
        self.dp_radio.pack(anchor="w", padx=20, pady=5)

        self.back_radio = ctk.CTkRadioButton(self.sidebar, text="Backtracking",
                                               variable=self.algoritmo, value="backtracking",
                                               font=("Segoe UI", 12), text_color="#cbd5e1",
                                               fg_color=COLORES['azul'], hover_color="#1d4ed8")
        self.back_radio.pack(anchor="w", padx=20, pady=5)

        self.compare_radio = ctk.CTkRadioButton(self.sidebar, text="Comparar todos",
                                                  variable=self.algoritmo, value="comparar",
                                                  font=("Segoe UI", 12), text_color="#cbd5e1",
                                                  fg_color=COLORES['azul'], hover_color="#1d4ed8")
        self.compare_radio.pack(anchor="w", padx=20, pady=5)

        self.run_button = ctk.CTkButton(self.sidebar, text="EJECUTAR", height=50,
                                         font=("Segoe UI", 16, "bold"),
                                         fg_color=COLORES['azul'], hover_color="#2563eb",
                                         text_color="#ffffff", corner_radius=10, command=self.ejecutar)
        self.run_button.pack(fill="x", padx=20, pady=(20, 10))

    def _crear_main_panel(self):
        self.main_panel = ctk.CTkFrame(self, corner_radius=15, fg_color=COLORES['panel'])
        self.main_panel.grid(row=0, column=1, sticky="nswe", padx=15, pady=15)
        self.main_panel.grid_rowconfigure(1, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)

        self.result_title = ctk.CTkLabel(self.main_panel, text="VISUALIZACION",
                                          font=("Segoe UI", 20, "bold"), text_color="#f8fafc")
        self.result_title.grid(row=0, column=0, pady=(15, 5))

        self.canvas = Canvas(self.main_panel, bg=COLORES['bg'], highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nswe", padx=15, pady=(0, 15))

        self.visualizador = Visualizador(self.canvas)

        self.output = ctk.CTkTextbox(self.main_panel, font=("Consolas", 12), corner_radius=12,
                                      fg_color=COLORES['bg'], text_color="#f8fafc",
                                      border_color="#334155", border_width=1, height=200)
        self.output.tag_config("header", foreground=COLORES['azul'])
        self.output.tag_config("negrita", foreground="#f8fafc")
        self.output.tag_config("accent", foreground=COLORES['cyan'])
        self.output.tag_config("success", foreground=COLORES['verde'])
        self.output.tag_config("warning", foreground=COLORES['amarillo'])
        self.output.tag_config("muted", foreground=COLORES['muted'])
        self.output.grid(row=2, column=0, sticky="nswe", padx=15, pady=(0, 15))

        self.graph_frame = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        self._ultimo_estado_truncado = False

    def _callback(self, estado):
        self.visualizador.agregar_estado(estado)
        if estado.get('tipo') == 'fin' and estado.get('truncado'):
            self._ultimo_estado_truncado = True

    def ejecutar(self):
        self.canvas.delete("all")
        self.output.delete("1.0", END)
        self.visualizador.limpiar()

        if hasattr(self, 'graph_frame'):
            self.graph_frame.grid_forget()
            self.main_panel.grid_rowconfigure(3, weight=0)

        try:
            capacidad = int(self.capacidad_entry.get())
            if capacidad <= 0:
                raise ValueError("La capacidad debe ser positiva.")

            pesos_raw = self.pesos_entry.get().split(",")
            valores_raw = self.valores_entry.get().split(",")

            if len(pesos_raw) != len(valores_raw):
                raise ValueError("La cantidad de pesos y valores debe ser igual.")

            pesos, valores = [], []
            for p in pesos_raw:
                val = int(p.strip())
                if val <= 0:
                    raise ValueError("Los pesos deben ser positivos (mayores a 0).")
                pesos.append(val)

            for v in valores_raw:
                val = int(v.strip())
                if val <= 0:
                    raise ValueError("Los valores deben ser positivos (mayores a 0).")
                valores.append(val)

            opcion = self.algoritmo.get()

            if opcion == "greedy":
                valor, objetos = mochila_greedy(pesos, valores, capacidad, callback=self._callback)
                self.visualizador.iniciar_animacion()
                self._mostrar_resultado_texto("GREEDY", valor, objetos, pesos, valores, capacidad)
            elif opcion == "dinamica":
                valor, objetos = mochila_dinamica(pesos, valores, capacidad, callback=self._callback)
                self.visualizador.iniciar_animacion()
                self._mostrar_resultado_texto("PROGRAMACION DINAMICA", valor, objetos, pesos, valores, capacidad)
            elif opcion == "backtracking":
                self._ultimo_estado_truncado = False
                valor, objetos = mochila_backtracking(pesos, valores, capacidad, callback=self._callback)
                self.visualizador.iniciar_animacion()
                self._mostrar_resultado_texto("BACKTRACKING", valor, objetos, pesos, valores, capacidad, self._ultimo_estado_truncado)
            elif opcion == "comparar":
                resultados = comparar_todo(pesos, valores, capacidad)
                self._mostrar_comparacion(resultados)
                self._mostrar_grafica(resultados)

        except Exception as e:
            self.output.insert(END, f"\nERROR: {str(e)}")

    def _mostrar_resultado_texto(self, titulo, valor, objetos, pesos, valores, capacidad, truncado=False):
        self.output.insert(END, f"\n{titulo}\n", "header")
        self.output.insert(END, f"Valor maximo: {valor}\n", "success")
        self.output.insert(END, f"Objetos seleccionados: ", "negrita")
        self.output.insert(END, f"{[f'Obj{i+1}' for i in objetos]}\n", "accent")
        peso_total = sum(pesos[i] for i in objetos)
        self.output.insert(END, f"Peso total: {peso_total}/{capacidad} kg\n", "success")
        if truncado:
            self.output.insert(END, "\nAVISO: La visualizacion fue truncada (limite de 500 estados).\n", "warning")
            self.output.insert(END, "El resultado es correcto, pero no se muestran todos los nodos explorados.\n", "muted")

    def _mostrar_comparacion(self, resultados):
        self.output.insert(END, "\nCOMPARACION DE PARADIGMAS\n\n", "header")
        for r in resultados:
            self.output.insert(END, f"{r['nombre']}\n", "accent")
            self.output.insert(END, f"  Valor: {r['valor']} | Objetos: {r['objetos']}\n", "success")
            self.output.insert(END, f"  Tiempo: {r['tiempo']:.6f}s | Memoria: {r['memoria']:.2f} KB\n")
            self.output.insert(END, f"  Complejidad: {r['complejidad']}\n\n", "warning")

    def _mostrar_grafica(self, resultados):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        nombres = [r["nombre"] if r["nombre"] != "PROGRAMACIÓN DINÁMICA" else "DINAMICA" for r in resultados]
        tiempos = [r["tiempo"] for r in resultados]
        memorias = [r["memoria"] for r in resultados]

        fig = Figure(figsize=(10, 3.5), dpi=100, facecolor='#2b2b2b')
        ax1, ax2 = fig.add_subplot(121), fig.add_subplot(122)

        colores = [COLORES['azul'], COLORES['verde'], COLORES['rojo']]
        bars1 = ax1.bar(nombres, tiempos, color=colores[:len(nombres)], width=0.5,
                         edgecolor='#475569', linewidth=1)
        ax1.set_title("Tiempo de Ejecucion", color='#f8fafc', fontsize=12, fontweight='bold', pad=10)
        ax1.set_ylabel("Segundos", color='#cbd5e1', fontsize=10)
        ax1.set_facecolor('#2b2b2b')
        ax1.tick_params(colors='#94a3b8', labelsize=9)
        ax1.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax1.set_axisbelow(True)
        for spine in ax1.spines.values():
            spine.set_color('#475569')
            spine.set_alpha(0.5)
        for bar in bars1:
            ax1.annotate(f'{bar.get_height():.6f}s',
                          xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                          xytext=(0, 3), textcoords="offset points",
                          ha='center', va='bottom', color='#cbd5e1', fontsize=8)

        colores_mem = ['#60a5fa', '#34d399', '#f87171']
        bars2 = ax2.bar(nombres, memorias, color=colores_mem[:len(nombres)], width=0.5,
                          edgecolor='#475569', linewidth=1)
        ax2.set_title("Uso de Memoria", color='#f8fafc', fontsize=12, fontweight='bold', pad=10)
        ax2.set_ylabel("KB", color='#cbd5e1', fontsize=10)
        ax2.set_facecolor('#2b2b2b')
        ax2.tick_params(colors='#94a3b8', labelsize=9)
        ax2.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax2.set_axisbelow(True)
        for spine in ax2.spines.values():
            spine.set_color('#475569')
            spine.set_alpha(0.5)
        for bar in bars2:
            ax2.annotate(f'{bar.get_height():.2f} KB',
                          xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                          xytext=(0, 3), textcoords="offset points",
                          ha='center', va='bottom', color='#cbd5e1', fontsize=8)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.output.grid(row=2, column=0, sticky="nswe", padx=15, pady=(0, 5))
        self.graph_frame.grid(row=3, column=0, sticky="nswe", padx=15, pady=(0, 15))
        self.main_panel.grid_rowconfigure(3, weight=0)


if __name__ == "__main__":
    app = MochilaApp()
    app.mainloop()