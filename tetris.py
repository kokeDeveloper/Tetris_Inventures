# Importación de módulos y clases necesarios
from settings import *
import math
from tetromino import Tetromino
import pygame.freetype as ft

# Clase que maneja la representación del texto en el juego
class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)
    
    def draw(self):
        # Renderiza diferentes textos en la pantalla con posiciones y tamaños específicos
        self.font.render_to(self.app.screen, (WIN_W * 0.597, WIN_H * 0.02),
                            text='TETRIS', fgcolor = 'white',
                            size = TILE_SIZE * 2.65)
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.22),
                            text='next', fgcolor = 'orange',
                            size = TILE_SIZE * 2.4)
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.67),
                            text='score', fgcolor = 'white',
                            size = TILE_SIZE * 2.4)
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.8),
                            text=f'{self.app.tetris.score}', fgcolor = 'white',
                            size = TILE_SIZE * 2.8)
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.55),
                            text='Level', fgcolor = 'white',
                            size = TILE_SIZE * 1)
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.6),
                            text=f'{self.app.tetris.level}', fgcolor = 'white',
                            size = TILE_SIZE * 1)

# Clase principal que gestiona el estado del juego        
class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current = False)
        self.speed_up = False
        self.level = 1
        self.lines_to_next_level = 10
        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
        self.completed_lines_count = 0
        
    def get_score(self):
        # Actualiza la puntuación del juego basándose en las líneas completadas
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0
    
    def up_level(self):
        # Aumenta el nivel del juego si se completan suficientes líneas
        if self.completed_lines_count >= self.lines_to_next_level:
            self.level += 1
            self.lines_to_next_level += 10
            print("Subiendo de nivel...")
    
    def check_full_lines(self):
        # Verifica si hay líneas completas en el campo y las elimina
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, - 1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]
                
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)
            
            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                print(f"Línea completa en la fila {y}!")
                self.completed_lines_count += 1
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False 
                    self.field_array[row][x] = 0
                    
                self.full_lines += 1
    
    def put_tetromino_blocks_in_array(self):
        # Coloca los bloques del tetromino actual en la matriz del campo de juego
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block
    
    def get_field_array(self):
        # Inicializa una matriz vacía para representar el campo de juego
        return [[0 for x in range (FIELD_W)] for y in range (FIELD_H)]
    
    def is_game_over(self):
        # Verifica si el juego ha terminado al alcanzar la parte superior del campo
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True
    
    def hard_drop(self):
        # Hace que el tetromino caiga rápidamente hasta llegar al fondo
        while not self.tetromino.landing:
            self.tetromino.move(direction='down')
        self.check_tetromino_landing()
    
    def check_tetromino_landing(self):
        # Verifica si el tetromino ha aterrizado y realiza las acciones correspondientes
        if self.tetromino.landing:
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)
    
    def control(self, pressed_key):
        # Maneja las acciones del jugador en función de las teclas presionadas
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True
    
    def draw_grid(self):
        # Dibuja la cuadrícula del campo de juego
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black',
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
    
    def update(self):
        # Actualiza el juego en cada fotograma
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
            self.up_level()
        self.sprite_group.update()

    def draw(self):
        # Dibuja la cuadrícula y los tetrominos en la pantall
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)