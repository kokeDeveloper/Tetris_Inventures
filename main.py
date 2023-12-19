# Importaciones necesarias
from settings import *
from tetris import Tetris, Text
import sys
import pygame.mixer as mixer


# Clase que representa el juego
class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.load_music()
        
    def set_timer(self):
        # Configuración de eventos temporizados
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def update(self):
        # Actualiza el juego y limita la velocidad de fotogramas
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        # Dibuja el campo de juego, tetrominos y texto
        self.screen.fill(color=FIELD_COLOR)
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()

    def check_events(self):
        # Maneja eventos del teclado y de cierre de la ventana
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
                if event.key == pg.K_SPACE:  
                    self.tetris.hard_drop()   
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True
    
    def load_music(self):
        # Inicializa y carga la música de fondo
        mixer.init()

        bg_music_path = 'Tetris_original_theme.mp3'
        mixer.music.load(bg_music_path)

        mixer.music.play(-1)  # El argumento -1 significa reproducir en bucle

    def run(self):
        # Bucle principal del juego
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()

# Otros módulos y clases tienen sus propios comentarios para facilitar la comprensión del código.
# Puedes consultar el código completo para ver los comentarios en cada sección.
