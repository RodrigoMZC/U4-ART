# Proyecto: Red Neuronal ART

Este repositorio contiene una implementación didáctica de una red neuronal ART (Adaptive Resonance Theory) sencilla, con una interfaz gráfica en Tkinter para dibujar o cargar imágenes y clasificar/aprender patrones binarios.

**Características principales**
- Implementación básica de una red ART (clasificación y aprendizaje ).
- Interfaz gráfica con Tkinter para pintar un grid o cargar imágenes.
- Visualización del prototipo aprendido por la red.
- Parámetros configurables en `config.py`.

## Estructura del proyecto
- `main.py`: Punto de entrada de la aplicación. Inicializa la ventana Tkinter y lanza la app.
- `gui.py`: Implementa la clase `NeuralApp` con toda la interfaz (canvas de dibujo, controles y lógica de interacción).
- `art.py`: Implementación de la red ART (`ARTNetwork`) con métodos de predicción, creación/actualización de categorías y obtención de prototipos.
- `config.py`: Parámetros del proyecto (tamaño del grid, tamaño de celda, parámetros ART como `rho`, `beta`, número máximo de categorías, y umbral de imagen).
- `requirements.txt`: Dependencias necesarias (`numpy`, `Pillow`, `tkinter`).

## Requisitos
- Python 3.8+ (o compatible con `tkinter` y `Pillow`).
- Dependencias listadas en `requirements.txt`.

## Instalación
1. Crear y activar un entorno virtual (opcional, recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

Nota: En macOS `tkinter` normalmente viene con la instalación del sistema o con la instalación de Python desde python.org. Si falta, instale la versión de Python que incluya `tkinter`.

## Uso
1. Ejecutar la aplicación:

```bash
python main.py
```

2. Interfaz:
- En el panel izquierdo puedes dibujar en el grid con el mouse. Se puede arrastrar para pintar.
- `Limpiar` borra la entrada actual.
- `Cargar Imagen` permite seleccionar una imagen (`.png`, `.jpg`) que se redimensiona al tamaño del grid y se umbraliza.
- Ajusta el control `Vigilancia (Rho)` para cambiar la sensibilidad de la red (1.0 = muy estricto, 0.0 = muy flexible).
- Presiona `PROCESAR ->` para que la red ART intente reconocer o aprender el patrón.

3. Salida:
- La etiqueta mostrará si el patrón fue reconocido, aprendido como nuevo o si la memoria está llena.
- El panel derecho muestra el prototipo (patrón) asociado a la categoría encontrada.

## Configuración y parámetros
Editar `config.py` para cambiar parámetros:
- `GRID_ROWS`, `GRID_COLS`: dimensión del grid de entrada/salida.
- `CELL_SIZE`: tamaño visual (píxeles) de cada celda en el canvas.
- `MAX_CATEGORIES`: número máximo de categorías (memoria de la red).
- `DEFAULT_RHO`: valor inicial de vigilancia (rho).
- `BETA`: parámetro de elección (usado en la implementación si se decide extender).
- `IMAGE_THRESHOLD`: umbral para binarizar imágenes cargadas.

## Detalles de la implementación
- `ARTNetwork` en `art.py` contiene:
  - Pesos bottom-up (`W_bu`) y top-down (`W_td`).
  - `predict(input_vector)`: intenta clasificar o crear una nueva categoría.
  - `_create_category` y `_update_weights` para aprendizaje.
  - `get_prototype(idx)` para recuperar el prototipo top-down.

La representación de entrada es un vector binario (0/1) con tamaño `GRID_ROWS * GRID_COLS`.