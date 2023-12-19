# Importación del módulo pygame y creación del vector 2D
import pygame as pg

vec = pg.math.Vector2

# Configuración de parámetros del juego
FPS = 60
FIELD_COLOR = (40, 40, 40)

# Ruta al archivo de fuente de texto para el juego
FONT_PATH = 'assetes/Good-Game.ttf'

# Intervalos de tiempo para las animaciones del juego
ANIM_TIME_INTERVAL = 150 
FAST_ANIM_TIME_INTERVAL = 15

# Tamaño de las celdas y dimensiones del campo de juego
TILE_SIZE = 40
FIELD_SIZE = FIELD_W, FIELD_H = 10, 20
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE

# Escalado de la ventana del juego y dimensiones resultantes
FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H

# Desplazamiento del grid en la ventana
GRID_OFFSET = vec((FIELD_SCALE_W - FIELD_W * TILE_SIZE) // 2, FIELD_SCALE_H - FIELD_H * TILE_SIZE)

# Posición inicial y próxima posición para el tetromino
INIT_POS_OFFSET = vec(FIELD_W // 2 - 1, 0)
NEXT_POS_OFFSET = vec(FIELD_W * 1.3, FIELD_H * 0.45)

# Direcciones de movimiento del tetromino
MOVE_DIRECTIONS = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)}

# Definición de las formas de los tetrominos y sus bloques relativos
TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)],
}