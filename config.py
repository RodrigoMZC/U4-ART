# --- DIMENSIONES DEL GRID ---
GRID_ROWS = 50
GRID_COLS = 50

# Tamaño visual de cada cuadrito en la pantalla (en píxeles)
CELL_SIZE = 20 

# --- PARÁMETROS DE LA RED NEURONAL (ART-1) ---
MAX_CATEGORIES = 10   # Cuántos patrones distintos puede aprender como máximo
DEFAULT_RHO = 0.5     # Vigilancia inicial (0.0 a 1.0)
BETA = 1.0            # Parámetro de elección (estándar es 1.0)

# --- PROCESAMIENTO DE IMAGEN ---
# Umbral para decidir si un gris es blanco o negro (0 a 255)
# Si la imagen sale muy negra, aumenta esto. Si sale muy blanca, bájalo.
IMAGE_THRESHOLD = 128