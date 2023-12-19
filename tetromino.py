# Importación de módulos y clases necesarios
from settings import *
import random

# Clase que representa un bloque individual en el juego
class Block (pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True
        # Asigna un color al bloque según la forma del tetromino
        self.color = {
            'I': 'lightblue',
            'J': 'darkblue',
            'L': 'orange',
            'O': 'yellow',
            'S': 'green',
            'Z': 'red',
            'T': 'magenta',
        }[tetromino.shape]
        # Inicializa el bloque como una instancia de Sprite de Pygame
        super().__init__(tetromino.tetris.sprite_group)
        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        # Dibuja el bloque con un color específico y un borde redondeado
        pg.draw.rect(self.image, self.color, (1, 1, TILE_SIZE - 2, TILE_SIZE - 2), border_radius=8)
        self.rect = self.image.get_rect()
        
    def is_alive(self):
        # Elimina el bloque si ya no está vivo
        if not self.alive:
            self.kill() 
    
    def rotate(self, pivot_pos):
        # Realiza una rotación de 90 grados alrededor de un punto de pivote
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos
            
    def set_rect_pos(self):
        # Establece la posición del rectángulo en función de la posición actual o próxima del bloque
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * TILE_SIZE  
    def update(self):
        # Actualiza la posición del bloque en cada fotograma
        self.is_alive()
        self.set_rect_pos()
        
    def is_collide(self, pos):
        # Verifica si hay colisión con otros bloques o los límites del campo
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (y < 0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True
        

# Clase que representa un tetromino en el juego
class Tetromino:
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = TetrominoBag().get_next_tetromino()
        # Crea bloques para el tetromino según su forma
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        self.landing = False
        self.current = current
    
    def rotate (self):
        # Realiza una rotación del tetromino
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]
        
        # Verifica si la rotación causa colisión
        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]
    
    def is_collide(self, block_position):
        # Verifica si hay colisión con otros bloques del tetromino o bloques en el campo
        return any(map(Block.is_collide, self.blocks, block_position))
    
    def move(self, direction):
        # Mueve el tetromino en una dirección específica
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)
        
        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.landing = True
    
    def update (self):
        # Actualiza la posición del tetromino moviéndolo hacia abajo
        self.move(direction='down')

# Clase que maneja la bolsa de tetrominos para asegurar variedad en las piezas 
class TetrominoBag:
    def __init__(self):
        self.tetrominos = ['T', 'O', 'J', 'L', 'I', 'S', 'Z']
        self.shuffle()

    def shuffle(self):
        # Mezcla las piezas en la bolsa para mayor aleatoriedad
        random.shuffle(self.tetrominos)

    def get_next_tetromino(self):
        # Obtiene el siguiente tetromino de la bolsa, mezclándola si es necesario
        if len(self.tetrominos) == 0:
            self.shuffle()

        return self.tetrominos.pop()