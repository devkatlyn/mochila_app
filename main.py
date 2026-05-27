from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tkinter import END

from greedy import mochila_greedy
from dinamica import mochila_dinamica
from backtracking import mochila_backtracking
from comparador import comparar_todo

ctk.set_appearance_mode("dark")  # Tema oscuro
ctk.set_default_color_theme("blue")


class MochilaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Analizador del Problema de la Mochila")
        self.geometry("1200x720")
        self.minsize(1100, 650)
        self.configure(fg_color="#0f172a")  # Slate 900

        self.grid_columnconfigure(0, weight=1)  # Sidebar
        self.grid_columnconfigure(1, weight=2)  # Main panel
        self.grid_rowconfigure(0, weight=1)

        self._crear_sidebar()
        self._crear_main_panel()

    def _crear_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=15, fg_color="#1e293b")  # Slate 800
        self.sidebar.grid(row=0, column=0, sticky="nswe", padx=(15, 0), pady=15)

        self.title_label = ctk.CTkLabel(self.sidebar, text="ANALIZADOR DEL PROBLEMA\nDE LA MOCHILA", font=("Segoe UI", 18, "bold"), text_color="#3b82f6")
        self.title_label.pack(pady=(30, 10))

        self.subtitle = ctk.CTkLabel(self.sidebar, text="Comparación de paradigmas\nde programación", font=("Segoe UI", 12), text_color="#64748b")
        self.subtitle.pack(pady=(0, 20))

        # Capacidad
        self.capacidad_label = ctk.CTkLabel(self.sidebar, text="Capacidad de la mochila", font=("Segoe UI", 12, "bold"), text_color="#cbd5e1")
        self.capacidad_label.pack(anchor="w", padx=20)
        self.capacidad_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 8", height=40, fg_color="#0f172a", border_color="#334155", text_color="#f8fafc", placeholder_text_color="#64748b", corner_radius=8)
        self.capacidad_entry.pack(fill="x", padx=20, pady=(5, 12))

        # Pesos
        self.pesos_label = ctk.CTkLabel(self.sidebar, text="Pesos", font=("Segoe UI", 12, "bold"), text_color="#cbd5e1")
        self.pesos_label.pack(anchor="w", padx=20)
        self.pesos_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 2,3,4,5", height=40, fg_color="#0f172a", border_color="#334155", text_color="#f8fafc", placeholder_text_color="#64748b", corner_radius=8)
        self.pesos_entry.pack(fill="x", padx=20, pady=(5, 12))

        # Valores
        self.valores_label = ctk.CTkLabel(self.sidebar, text="Valores", font=("Segoe UI", 12, "bold"), text_color="#cbd5e1")
        self.valores_label.pack(anchor="w", padx=20)
        self.valores_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 3,4,5,6", height=40, fg_color="#0f172a", border_color="#334155", text_color="#f8fafc", placeholder_text_color="#64748b", corner_radius=8)
        self.valores_entry.pack(fill="x", padx=20, pady=(5, 20))

        # Selección de algoritmo
        self.algoritmo_label = ctk.CTkLabel(self.sidebar, text="Selecciona un algoritmo", font=("Segoe UI", 14, "bold"), text_color="#f8fafc")
        self.algoritmo_label.pack(anchor="w", padx=20, pady=(5, 10))
        self.algoritmo = ctk.StringVar(value="dinamica")

        self.greedy_radio = ctk.CTkRadioButton(self.sidebar, text="Greedy (Voraz)", variable=self.algoritmo, value="greedy", font=("Segoe UI", 12), text_color="#cbd5e1", fg_color="#3b82f6", hover_color="#1d4ed8")
        self.greedy_radio.pack(anchor="w", padx=20, pady=5)

        self.dp_radio = ctk.CTkRadioButton(self.sidebar, text="Programación Dinámica", variable=self.algoritmo, value="dinamica", font=("Segoe UI", 12), text_color="#cbd5e1", fg_color="#3b82f6", hover_color="#1d4ed8")
        self.dp_radio.pack(anchor="w", padx=20, pady=5)

        self.back_radio = ctk.CTkRadioButton(self.sidebar, text="Backtracking", variable=self.algoritmo, value="backtracking", font=("Segoe UI", 12), text_color="#cbd5e1", fg_color="#3b82f6", hover_color="#1d4ed8")
        self.back_radio.pack(anchor="w", padx=20, pady=5)

        self.compare_radio = ctk.CTkRadioButton(self.sidebar, text="Comparar todos", variable=self.algoritmo, value="comparar", font=("Segoe UI", 12), text_color="#cbd5e1", fg_color="#3b82f6", hover_color="#1d4ed8")
        self.compare_radio.pack(anchor="w", padx=20, pady=5)

        # Botón ejecutar
        self.run_button = ctk.CTkButton(self.sidebar, text="EJECUTAR", height=50, font=("Segoe UI", 16, "bold"), fg_color="#3b82f6", hover_color="#2563eb", text_color="#ffffff", corner_radius=10, command=self.ejecutar)
        self.run_button.pack(fill="x", padx=20, pady=(20, 10))

    def _crear_main_panel(self):
        self.main_panel = ctk.CTkFrame(self, corner_radius=15, fg_color="#1e293b")  # Slate 800
        self.main_panel.grid(row=0, column=1, sticky="nswe", padx=15, pady=15)
        self.main_panel.grid_rowconfigure(1, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)

        self.result_title = ctk.CTkLabel(self.main_panel, text="RESULTADOS", font=("Segoe UI", 22, "bold"), text_color="#f8fafc")
        self.result_title.grid(row=0, column=0, pady=(20, 10))

        self.output = ctk.CTkTextbox(self.main_panel, font=("Consolas", 14), corner_radius=12, fg_color="#0f172a", text_color="#f8fafc", border_color="#334155", border_width=1)
        self.output.grid(row=1, column=0, sticky="nswe", padx=20, pady=(0, 20))
        self.output.tag_config("header", foreground="#60a5fa")
        self.output.tag_config("negrita", foreground="#f8fafc")
        self.output.tag_config("accent", foreground="#38bdf8")
        self.output.tag_config("success", foreground="#34d399")
        self.output.tag_config("warning", foreground="#fbbf24")
        self.output.tag_config("muted", foreground="#64748b")

        self.graph_frame = ctk.CTkFrame(self.main_panel, fg_color="transparent")

    def ejecutar(self):
        self.output.delete("1.0", END)
        if hasattr(self, 'graph_frame'):
            self.graph_frame.grid_forget()
            self.main_panel.grid_rowconfigure(2, weight=0)
            self.output.grid(row=1, column=0, sticky="nswe", padx=20, pady=(0, 20))

        try:
            capacidad = int(self.capacidad_entry.get())
            if capacidad <= 0:
                raise ValueError("La capacidad debe ser un número positivo.")

            pesos_raw = self.pesos_entry.get().split(",")
            valores_raw = self.valores_entry.get().split(",")

            if len(pesos_raw) != len(valores_raw):
                raise ValueError("La cantidad de pesos y valores debe ser igual.")

            pesos, valores = [], []
            for p in pesos_raw:
                val = int(p.strip())
                if val < 0:
                    raise ValueError("Los pesos no pueden ser negativos.")
                pesos.append(val)

            for v in valores_raw:
                val = int(v.strip())
                if val < 0:
                    raise ValueError("Los valores no pueden ser negativos.")
                valores.append(val)

            opcion = self.algoritmo.get()

            if opcion == "greedy":
                valor, objetos = mochila_greedy(pesos, valores, capacidad)
                self.mostrar_resultado("GREEDY", valor, objetos, pesos, valores, capacidad)
            elif opcion == "dinamica":
                valor, objetos = mochila_dinamica(pesos, valores, capacidad)
                self.mostrar_resultado("PROGRAMACIÓN DINÁMICA", valor, objetos, pesos, valores, capacidad)
            elif opcion == "backtracking":
                valor, objetos = mochila_backtracking(pesos, valores, capacidad)
                self.mostrar_resultado("BACKTRACKING", valor, objetos, pesos, valores, capacidad)
            elif opcion == "comparar":
                resultados = comparar_todo(pesos, valores, capacidad)
                self._mostrar_comparacion(resultados)
                self.mostrar_grafica(resultados)

        except Exception as e:
            self.output.insert(END, f"\nERROR: {str(e)}")

    def _mostrar_comparacion(self, resultados):
        self.output.insert(END, "\n========= COMPARACIÓN DE PARADIGMAS =========\n\n", "header")
        for r in resultados:
            self.output.insert(END, f"{r['nombre']}\n", "accent")
            self.output.insert(END, "Valor obtenido: ", "negrita")
            self.output.insert(END, f"{r['valor']}\n", "success")
            self.output.insert(END, "Objetos seleccionados: ", "negrita")
            self.output.insert(END, f"{r['objetos']}\n")
            self.output.insert(END, "Tiempo de ejecución: ", "negrita")
            self.output.insert(END, f"{r['tiempo']:.6f} segundos\n")
            self.output.insert(END, "Uso de memoria: ", "negrita")
            self.output.insert(END, f"{r['memoria']:.2f} KB\n")
            self.output.insert(END, "Complejidad algorítmica: ", "negrita")
            self.output.insert(END, f"{r['complejidad']}\n", "warning")
            self.output.insert(END, "------------------------------------------\n\n", "muted")

    def mostrar_resultado(self, titulo, valor, objetos, pesos, valores, capacidad):
        self.output.insert(END, f"\n========== {titulo} ==========\n\n", "header")
        self.output.insert(END, "Capacidad máxima: ", "negrita")
        self.output.insert(END, f"{capacidad} kg\n\n", "accent")
        self.output.insert(END, "Objetos disponibles:\n\n", "negrita")

        for i in range(len(pesos)):
            self.output.insert(END, f"Objeto {i+1} → ", "muted")
            self.output.insert(END, f"Peso: {pesos[i]} kg | Valor: {valores[i]}\n")

        self.output.insert(END, "\nObjetos seleccionados:\n\n", "negrita")
        peso_total = 0
        for i in objetos:
            self.output.insert(END, "Objeto {i+1} → ", "success")
            self.output.insert(END, f"Peso: {pesos[i]} kg | Valor: {valores[i]}\n")
            peso_total += pesos[i]

        self.output.insert(END, "\n------------------------------------------------\n", "muted")
        self.output.insert(END, "Peso total utilizado: ", "negrita")
        self.output.insert(END, f"{peso_total} kg\n", "warning" if peso_total > capacidad else "success")
        self.output.insert(END, "Valor máximo obtenido: ", "negrita")
        self.output.insert(END, f"{valor}\n", "success")
        self.output.insert(END, "================================================\n", "muted")

    def mostrar_grafica(self, resultados):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        nombres = [r["nombre"] if r["nombre"] != "PROGRAMACIÓN DINÁMICA" else "DINÁMICA" for r in resultados]
        tiempos = [r["tiempo"] for r in resultados]
        memorias = [r["memoria"] for r in resultados]

        fig = Figure(figsize=(10, 3.5), dpi=100, facecolor='#2b2b2b')
        ax1, ax2 = fig.add_subplot(121), fig.add_subplot(122)

        colores = ['#3b82f6', '#10b981', '#ef4444']
        bars1 = ax1.bar(nombres, tiempos, color=colores[:len(nombres)], width=0.5, edgecolor='#475569', linewidth=1)
        ax1.set_title("Tiempo de Ejecución", color='#f8fafc', fontsize=12, fontweight='bold', pad=10)
        ax1.set_ylabel("Segundos", color='#cbd5e1', fontsize=10)
        ax1.set_facecolor('#2b2b2b')
        ax1.tick_params(colors='#94a3b8', labelsize=9)
        ax1.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax1.set_axisbelow(True)
        for spine in ax1.spines.values():
            spine.set_color('#475569')
            spine.set_alpha(0.5)
        for bar in bars1:  # Etiquetas sobre barras
            ax1.annotate(f'{bar.get_height():.6f}s', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', color='#cbd5e1', fontsize=8)

        colores_mem = ['#60a5fa', '#34d399', '#f87171']
        bars2 = ax2.bar(nombres, memorias, color=colores_mem[:len(nombres)], width=0.5, edgecolor='#475569', linewidth=1)
        ax2.set_title("Uso de Memoria", color='#f8fafc', fontsize=12, fontweight='bold', pad=10)
        ax2.set_ylabel("KB", color='#cbd5e1', fontsize=10)
        ax2.set_facecolor('#2b2b2b')
        ax2.tick_params(colors='#94a3b8', labelsize=9)
        ax2.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax2.set_axisbelow(True)
        for spine in ax2.spines.values():
            spine.set_color('#475569')
            spine.set_alpha(0.5)
        for bar in bars2:  # Etiquetas sobre barras
            ax2.annotate(f'{bar.get_height():.2f} KB', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', color='#cbd5e1', fontsize=8)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.output.grid(row=1, column=0, sticky="nswe", padx=20, pady=(0, 10))
        self.graph_frame.grid(row=2, column=0, sticky="nswe", padx=20, pady=(0, 20))
        self.main_panel.grid_rowconfigure(2, weight=1)


if __name__ == "__main__":
    app = MochilaApp()
    app.mainloop()