import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import config
from PIL import Image, ImageOps
from art import ARTNetwork

class NeuralApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Red Neuronal ART")
        
        self.rows = config.GRID_ROWS
        self.cols = config.GRID_COLS
        self.cell_size = config.CELL_SIZE
        
        # Inicializar Red ART
        self.art = ARTNetwork(n=self.rows*self.cols, m=config.MAX_CATEGORIES, rho=config.DEFAULT_RHO, beta=config.BETA)
        
        # Variables de interfaz
        self.input_grid = np.zeros(self.rows * self.cols)
        self.rho_var = tk.DoubleVar(value=config.DEFAULT_RHO)
        
        self.setup_ui()

    def setup_ui(self):
        # Frame Principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=20, pady=20)
        
        # --- Lado Izquierdo: Entrada ---
        left_panel = tk.Frame(main_frame)
        left_panel.grid(row=0, column=0, padx=20)
        
        tk.Label(left_panel, text="Entrada", font=("Arial", 12, "bold")).pack()
        self.canvas_in = tk.Canvas(left_panel, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas_in.pack(pady=5)
        self.canvas_in.bind("<ButtonPress-1>", self.start_paint)
        self.canvas_in.bind("<B1-Motion>", self.paint_move)
        self.draw_grid(self.canvas_in)
        
        btn_frame = tk.Frame(left_panel)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Limpiar", command=self.clear_input, bg="#ffcccc").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cargar Imagen", command=self.load_image).pack(side=tk.LEFT, padx=5)

        # --- Centro: Controles ---
        ctrl_panel = tk.Frame(main_frame)
        ctrl_panel.grid(row=0, column=1, padx=20)
        
        tk.Label(ctrl_panel, text="Vigilancia (Rho)").pack()
        tk.Scale(ctrl_panel, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.rho_var, length=150).pack()
        tk.Label(ctrl_panel, text="(1.0 = Estricto / 0.0 = Flexible)", font=("Arial", 8)).pack(pady=5)
        
        tk.Button(ctrl_panel, text="PROCESAR ->", font=("Arial", 10, "bold"), command=self.process_network, bg="#ccffcc", height=2, width=15).pack(pady=20)

        # --- Lado Derecho: Salida ---
        right_panel = tk.Frame(main_frame)
        right_panel.grid(row=0, column=2, padx=20)
        
        tk.Label(right_panel, text="Memoria de la Red (Salida)", font=("Arial", 12, "bold")).pack()
        self.canvas_out = tk.Canvas(right_panel, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg="#f0f0f0", highlightthickness=1, highlightbackground="black")
        self.canvas_out.pack(pady=5)
        self.draw_grid(self.canvas_out, is_output=True)
        
        self.lbl_result = tk.Label(right_panel, text="Esperando entrada...", fg="blue")
        self.lbl_result.pack()

    def draw_grid(self, canvas, is_output=False):
        canvas.delete("grid_line")
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                fill = "white"
                tags = (f"cell_{r}_{c}", "grid_line")
                canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="gray", tags=tags)

    def paint_cell(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= col < self.cols and 0 <= row < self.rows:
            idx = row * self.cols + col
            self.input_grid[idx] = 1
            self.canvas_in.itemconfig(f"cell_{row}_{col}", fill="black")

    def start_paint(self, event):
        """Se ejecuta al hacer el primer clic. Decide si pintamos o borramos."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= col < self.cols and 0 <= row < self.rows:
            idx = row * self.cols + col
            current_val = self.input_grid[idx]
            
            # LÓGICA INTELIGENTE:
            # Si el pixel actual es 0 (blanco), activamos modo PINTAR (1)
            # Si el pixel actual es 1 (negro), activamos modo BORRAR (0)
            if current_val == 0:
                self.current_paint_mode = 1
            else:
                self.current_paint_mode = 0
            
            # Aplicar inmediatamente al pixel clickeado
            self.update_cell(row, col, self.current_paint_mode)

    def paint_move(self, event):
        """Se ejecuta al arrastrar el mouse. Usa el modo decidido en start_paint."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= col < self.cols and 0 <= row < self.rows:
            # Aplicar el mismo modo (pintar o borrar) a los cuadros por donde pase el mouse
            self.update_cell(row, col, self.current_paint_mode)
    def update_cell(self, row, col, val):
        """Función auxiliar para actualizar visual y lógicamente una celda"""
        idx = row * self.cols + col
        # 1. Actualizar lógica (matriz numpy)
        self.input_grid[idx] = val
        
        # 2. Actualizar visual (canvas)
        # Usamos colores definidos en config
        color = "black" if val == 1 else "white"
        self.canvas_in.itemconfig(f"cell_{row}_{col}", fill=color)
        
    def clear_input(self):
        self.input_grid = np.zeros(self.rows * self.cols)
        for r in range(self.rows):
            for c in range(self.cols):
                self.canvas_in.itemconfig(f"cell_{r}_{c}", fill="white")
        self.lbl_result.config(text="Limpio")

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if not file_path:
            return
        try:
            img = Image.open(file_path).convert('L')
            img = img.resize((self.cols, self.rows), Image.Resampling.NEAREST)
            threshold = 128
            img = img.point(lambda p: 255 if p > threshold else 0)
            img = ImageOps.invert(img)
            
            data = np.array(img)
            self.clear_input()
            
            for r in range(self.rows):
                for c in range(self.cols):
                    if data[r, c] > 128:
                        self.input_grid[r * self.cols + c] = 1
                        self.canvas_in.itemconfig(f"cell_{r}_{c}", fill="black")
                    else:
                        self.input_grid[r * self.cols + c] = 0
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

    def process_network(self):
        self.art.rho = self.rho_var.get()
        if np.sum(self.input_grid) == 0:
            self.lbl_result.config(text="Dibuja algo primero")
            return

        category_idx, message, pattern_to_draw = self.art.predict(self.input_grid)
        self.lbl_result.config(text=message)
        
        if category_idx != -1 and pattern_to_draw is not None:
            # Dibujamos el patrón que nos devolvió predict (el original antes de aprender)
            self.draw_output_pattern(pattern_to_draw)

        #prototype = self.art.get_prototype(category_idx)
        #self.draw_output_pattern(prototype)

    def draw_output_pattern(self, pattern):
        for r in range(self.rows):
            for c in range(self.cols):
                idx = r * self.cols + c
                color = "#af1379" if pattern[idx] >= 0.9 else "#fefefe"
                self.canvas_out.itemconfig(f"cell_{r}_{c}", fill=color)