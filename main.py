from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tkinter import END

from greedy import mochila_greedy
from dinamica import mochila_dinamica
from backtracking import mochila_backtracking
from comparador import comparar_todo



# CONFIGURACIÓN GLOBAL


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# APP


class MochilaApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # WINDOW 
        self.title("Analizador del Problema de la Mochila")
        self.geometry("1200x720")
        self.minsize(1100, 650)
        self.configure(fg_color="#0f172a") # Slate 900

        # GRID 
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        
        # SIDEBAR
        

        self.sidebar = ctk.CTkFrame(
            self,
            width=320,
            corner_radius=15,
            fg_color="#1e293b" # Slate 800
        )

        self.sidebar.grid(row=0, column=0, sticky="nswe", padx=(15, 0), pady=15)

        # TITLE 

        self.title_label = ctk.CTkLabel(
            self.sidebar,
            text="ANALIZADOR DEL PROBLEMA\nDE LA MOCHILA",
            font=("Segoe UI", 18, "bold"),
            text_color="#3b82f6"
        )

        self.title_label.pack(pady=(30, 10))

        self.subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Comparación de paradigmas\nde programación",
            font=("Segoe UI", 12),
            text_color="#64748b"
        )

        self.subtitle.pack(pady=(0, 20))

        
        # INPUTS
       

        self.capacidad_label = ctk.CTkLabel(
            self.sidebar,
            text="Capacidad de la mochila",
            font=("Segoe UI", 12, "bold"),
            text_color="#cbd5e1"
        )
        self.capacidad_label.pack(anchor="w", padx=20)

        self.capacidad_entry = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Ej: 8",
            height=40,
            fg_color="#0f172a",
            border_color="#334155",
            text_color="#f8fafc",
            placeholder_text_color="#64748b",
            corner_radius=8
        )

        self.capacidad_entry.pack(fill="x", padx=20, pady=(5, 12))

        # ---------------- PESOS ----------------

        self.pesos_label = ctk.CTkLabel(
            self.sidebar,
            text="Pesos",
            font=("Segoe UI", 12, "bold"),
            text_color="#cbd5e1"
        )
        self.pesos_label.pack(anchor="w", padx=20)

        self.pesos_entry = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Ej: 2,3,4,5",
            height=40,
            fg_color="#0f172a",
            border_color="#334155",
            text_color="#f8fafc",
            placeholder_text_color="#64748b",
            corner_radius=8
        )

        self.pesos_entry.pack(fill="x", padx=20, pady=(5, 12))

        # ---------------- VALORES ----------------

        self.valores_label = ctk.CTkLabel(
            self.sidebar,
            text="Valores",
            font=("Segoe UI", 12, "bold"),
            text_color="#cbd5e1"
        )
        self.valores_label.pack(anchor="w", padx=20)

        self.valores_entry = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Ej: 3,4,5,6",
            height=40,
            fg_color="#0f172a",
            border_color="#334155",
            text_color="#f8fafc",
            placeholder_text_color="#64748b",
            corner_radius=8
        )

        self.valores_entry.pack(fill="x", padx=20, pady=(5, 20))

        
        # ALGORITMOS
        

        self.algoritmo_label = ctk.CTkLabel(
            self.sidebar,
            text="Selecciona un algoritmo",
            font=("Segoe UI", 14, "bold"),
            text_color="#f8fafc"
        )

        self.algoritmo_label.pack(anchor="w", padx=20, pady=(5, 10))

        self.algoritmo = ctk.StringVar(value="dinamica")

        self.greedy_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="Greedy (Voraz)",
            variable=self.algoritmo,
            value="greedy",
            font=("Segoe UI", 12),
            text_color="#cbd5e1",
            fg_color="#3b82f6",
            hover_color="#1d4ed8"
        )

        self.greedy_radio.pack(anchor="w", padx=20, pady=5)

        self.dp_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="Programación Dinámica",
            variable=self.algoritmo,
            value="dinamica",
            font=("Segoe UI", 12),
            text_color="#cbd5e1",
            fg_color="#3b82f6",
            hover_color="#1d4ed8"
        )

        self.dp_radio.pack(anchor="w", padx=20, pady=5)

        self.back_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="Backtracking",
            variable=self.algoritmo,
            value="backtracking",
            font=("Segoe UI", 12),
            text_color="#cbd5e1",
            fg_color="#3b82f6",
            hover_color="#1d4ed8"
        )

        self.back_radio.pack(anchor="w", padx=20, pady=5)

        self.compare_radio = ctk.CTkRadioButton(
            self.sidebar,
            text="Comparar todos",
            variable=self.algoritmo,
            value="comparar",
            font=("Segoe UI", 12),
            text_color="#cbd5e1",
            fg_color="#3b82f6",
            hover_color="#1d4ed8"
        )

        self.compare_radio.pack(anchor="w", padx=20, pady=5)

        
        # BUTTON
        

        self.run_button = ctk.CTkButton(
            self.sidebar,
            text="🚀 EJECUTAR",
            height=50,
            font=("Segoe UI", 16, "bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="#ffffff",
            corner_radius=10,
            command=self.ejecutar
        )

        self.run_button.pack(fill="x", padx=20, pady=(20, 10))

        
        # MAIN PANEL
        

        self.main_panel = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color="#1e293b" # Slate 800
        )

        self.main_panel.grid(row=0, column=1, sticky="nswe", padx=15, pady=15)

        self.main_panel.grid_rowconfigure(1, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)

        # ---------------- HEADER ----------------

        self.result_title = ctk.CTkLabel(
            self.main_panel,
            text="📊 RESULTADOS",
            font=("Segoe UI", 22, "bold"),
            text_color="#f8fafc"
        )

        self.result_title.grid(row=0, column=0, pady=(20, 10))

        # TEXTBOX
        

        self.output = ctk.CTkTextbox(
            self.main_panel,
            font=("Consolas", 14),
            corner_radius=12,
            fg_color="#0f172a",
            text_color="#f8fafc",
            border_color="#334155",
            border_width=1
        )

        self.output.grid(
            row=1,
            column=0,
            sticky="nswe",
            padx=20,
            pady=(0, 20)
        )

        # Configurar tags de color para el texto
        self.output.tag_config("header", foreground="#60a5fa")
        self.output.tag_config("negrita", foreground="#f8fafc")
        self.output.tag_config("accent", foreground="#38bdf8")
        self.output.tag_config("success", foreground="#34d399")
        self.output.tag_config("warning", foreground="#fbbf24")
        self.output.tag_config("muted", foreground="#64748b")

        
        # CONTENEDOR DE GRÁFICA
      

        self.graph_frame = ctk.CTkFrame(
            self.main_panel,
            fg_color="transparent"
        )

   
    # EJECUTAR
  

    def ejecutar(self):

        self.output.delete("1.0", END)

        # Ocultar la gráfica al iniciar una nueva ejecución
        if hasattr(self, 'graph_frame'):
            self.graph_frame.grid_forget()
            self.main_panel.grid_rowconfigure(2, weight=0)
            self.output.grid(row=1, column=0, sticky="nswe", padx=20, pady=(0, 20))

        try:

            capacidad = int(self.capacidad_entry.get())

            pesos = list(
                map(
                    int,
                    self.pesos_entry.get().split(",")
                )
            )

            valores = list(
                map(
                    int,
                    self.valores_entry.get().split(",")
                )
            )

            opcion = self.algoritmo.get()

            
            # GREEDY
            

            if opcion == "greedy":

                valor, objetos = mochila_greedy(
                    pesos,
                    valores,
                    capacidad
                )

                self.mostrar_resultado(
                    "GREEDY",
                    valor,
                    objetos,
                    pesos,
                    valores,
                    capacidad
                )

           
            # DINÁMICA
           

            elif opcion == "dinamica":

                valor, objetos = mochila_dinamica(
                    pesos,
                    valores,
                    capacidad
                )

                self.mostrar_resultado(
                    "PROGRAMACIÓN DINÁMICA",
                    valor,
                    objetos,
                    pesos,
                    valores,
                    capacidad
                )

         
            # BACKTRACKING
          

            elif opcion == "backtracking":

                valor, objetos = mochila_backtracking(
                    pesos,
                    valores,
                    capacidad
                )

                self.mostrar_resultado(
                    "BACKTRACKING",
                    valor,
                    objetos,
                    pesos,
                    valores,
                    capacidad
                )

           
            # COMPARAR TODOS
        

            elif opcion == "comparar":

                resultados = comparar_todo(
                    pesos,
                    valores,
                    capacidad
                )

                self.output.insert(
                    END,
                    "\n========= COMPARACIÓN DE PARADIGMAS =========\n\n",
                    "header"
                )

                for r in resultados:

                    self.output.insert(
                        END,
                        f"📊 {r['nombre']}\n",
                        "accent"
                    )

                    self.output.insert(
                        END,
                        "Valor obtenido: ",
                        "negrita"
                    )
                    self.output.insert(
                        END,
                        f"{r['valor']}\n",
                        "success"
                    )

                    self.output.insert(
                        END,
                        "Objetos seleccionados: ",
                        "negrita"
                    )
                    self.output.insert(
                        END,
                        f"{r['objetos']}\n"
                    )

                    self.output.insert(
                        END,
                        "Tiempo de ejecución: ",
                        "negrita"
                    )
                    self.output.insert(
                        END,
                        f"{r['tiempo']:.6f} segundos\n"
                    )

                    self.output.insert(
                        END,
                        "Uso de memoria: ",
                        "negrita"
                    )
                    self.output.insert(
                        END,
                        f"{r['memoria']:.2f} KB\n"
                    )

                    self.output.insert(
                        END,
                        "Complejidad algorítmica: ",
                        "negrita"
                    )
                    self.output.insert(
                        END,
                        f"{r['complejidad']}\n",
                        "warning"
                    )

                    self.output.insert(
                        END,
                        "------------------------------------------\n\n",
                        "muted"
                    )
                self.mostrar_grafica(resultados)

        except Exception as e:

            self.output.insert(
                END,
                f"\n❌ ERROR:\n{str(e)}"
            )

  
    # MOSTRAR RESULTADO
    

    def mostrar_resultado(
        self,
        titulo,
        valor,
        objetos,
        pesos,
        valores,
        capacidad
    ):
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
            self.output.insert(END, "✅ ", "success")
            self.output.insert(END, f"Objeto {i+1} → ", "success")
            self.output.insert(END, f"Peso: {pesos[i]} kg | Valor: {valores[i]}\n")
            peso_total += pesos[i]

        self.output.insert(END, "\n------------------------------------------------\n", "muted")
        
        self.output.insert(END, "Peso total utilizado: ", "negrita")
        self.output.insert(END, f"{peso_total} kg\n", "warning" if peso_total > capacidad else "success")
        
        self.output.insert(END, "Valor máximo obtenido: ", "negrita")
        self.output.insert(END, f"{valor}\n", "success")
        
        self.output.insert(END, "================================================\n", "muted")

    def mostrar_grafica(self, resultados):

        # Limpiar cualquier gráfica previa
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Acortar nombres para que no se superpongan en el eje X
        nombres = []
        for r in resultados:
            n = r["nombre"]
            if n == "PROGRAMACIÓN DINÁMICA":
                nombres.append("DINÁMICA")
            else:
                nombres.append(n)

        tiempos = [r["tiempo"] for r in resultados]
        memorias = [r["memoria"] for r in resultados]

        # Crear figura con 2 subplots (Tiempo y Memoria) lado a lado
        # Usamos facecolor='#2b2b2b' para integrarlo con el fondo oscuro de CustomTkinter
        fig = Figure(figsize=(10, 3.5), dpi=100, facecolor='#2b2b2b')
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # --- Gráfico de Tiempo ---
        colores_tiempo = ['#3b82f6', '#10b981', '#ef4444']  # Azul, Verde, Rojo
        bars1 = ax1.bar(nombres, tiempos, color=colores_tiempo[:len(nombres)], width=0.5, edgecolor='#475569', linewidth=1)
        ax1.set_title("Tiempo de Ejecución", color='#f8fafc', fontsize=12, fontweight='bold', pad=10)
        ax1.set_ylabel("Segundos", color='#cbd5e1', fontsize=10)
        ax1.set_facecolor('#2b2b2b')
        ax1.tick_params(colors='#94a3b8', labelsize=9)
        ax1.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax1.set_axisbelow(True)
        for spine in ax1.spines.values():
            spine.set_color('#475569')
            spine.set_alpha(0.5)
            
        # Añadir etiquetas de texto sobre las barras
        for bar in bars1:
            height = bar.get_height()
            ax1.annotate(f'{height:.6f}s',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', color='#cbd5e1', fontsize=8)

        # --- Gráfico de Memoria ---
        colores_memoria = ['#60a5fa', '#34d399', '#f87171']  # Tonos ligeramente más claros
        bars2 = ax2.bar(nombres, memorias, color=colores_memoria[:len(nombres)], width=0.5, edgecolor='#475569', linewidth=1)
        ax2.set_title("Uso de Memoria", color='#f8fafc', fontsize=12, fontweight='bold', pad=10)
        ax2.set_ylabel("KB", color='#cbd5e1', fontsize=10)
        ax2.set_facecolor('#2b2b2b')
        ax2.tick_params(colors='#94a3b8', labelsize=9)
        ax2.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        ax2.set_axisbelow(True)
        for spine in ax2.spines.values():
            spine.set_color('#475569')
            spine.set_alpha(0.5)

        # Añadir etiquetas de texto sobre las barras
        for bar in bars2:
            height = bar.get_height()
            ax2.annotate(f'{height:.2f} KB',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', color='#cbd5e1', fontsize=8)

        # Ajustar márgenes
        fig.tight_layout()

        # Dibujar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Configurar la visualización en el panel principal
        self.output.grid(row=1, column=0, sticky="nswe", padx=20, pady=(0, 10))
        self.graph_frame.grid(row=2, column=0, sticky="nswe", padx=20, pady=(0, 20))
        self.main_panel.grid_rowconfigure(2, weight=1)


# RUN APP


if __name__ == "__main__":

    app = MochilaApp()
    app.mainloop()
