import pygame
from gl import Renderer, ModelObj
import shaders
from pygame.locals import *
from pygame import mixer
from menu import *

class Game(object):
    def __init__(self, width = 500, height = 500):
        pygame.init()
        self.running, self.playing, self.isPaused = True, False, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.width, self.height = width, height
        self.deltaTime = 0.0
        self.display = pygame.Surface((self.width, self.height))
        self.window = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
        self.glwindow = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.OPENGL)
        self.font = pygame.font.Font("res/fonts/BOOne.ttf", 25)
        self.clock = pygame.time.Clock()
        self.main_menu = MainMenu(self)
        self.credits = CreditsMenu(self)
        self.options = OptionsMenu(self)
        self.instructions = InstructionsMenu(self)
        self.pause = PauseMenu(self)
        self.curr_menu = self.main_menu

        pygame.display.set_caption("OpenGL Renderer")

        # Create renderer
        self.rend = Renderer(self.glwindow)
        self.rend.setShaders(shaders.vertex_shader, shaders.fragment_shader)

        face = ModelObj('res/obj/model.obj', 'res/textures/model.bmp')
        pyr = ModelObj('res/obj/triangular.obj', 'res/textures/pyramid.bmp')
        homer = ModelObj('res/obj/homer.obj', 'res/textures/homer.bmp')
        weir = ModelObj('res/obj/coin.obj', 'res/textures/coin.jpg')

        face.position.z = -5
        pyr.position.z = -5
        homer.position.z = -5
        weir.position.z = -5

        self.rend.activeModel = face

        self.rend.scene.append(face)
        self.rend.scene.append(pyr)
        self.rend.scene.append(homer)
        self.rend.scene.append(weir)

        # Background music
        mixer.music.load('res/sfx/backgroundMusic.wav')
        mixer.music.play(-1)

        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

    # def updateFPS(self):
    #     fps = str(int(self.clock.get_fps()))
    #     fps = self.font.render(fps, 1, pygame.Color("white"))
    #     return fps

    def gameLoop(self):
        while self.playing:
            self.checkEvents()
            
            if self.START_KEY:
                self.playing = False
            
            # self.display.fill(self.BLACK)

            # #self.drawText('Thanks for playing', 25, self.width/2, self.height/2)
            # self.window.fill(pygame.Color("gray"))

            # # Techo
            # self.window.fill(pygame.Color("saddlebrown"), (0, 0,  self.width, int(self.height / 2)))

            # # Piso
            # self.window.fill(pygame.Color("dimgray"), (0, int(self.height / 2),  self.width, int(self.height / 2)))


            # self.rayCaster.render()

            if self.playing:
                self.rend.time += self.deltaTime
                self.deltaTime = self.clock.tick(60) / 1000
                self.rend.update()
                self.rend.render()

            #FPS
            # self.window.fill(pygame.Color("black"), (0,0,30,30) )
            # self.window.blit(self.updateFPS(), (0,0))
            # self.clock.tick(60)


            pygame.display.flip()

            # self.window.blit(self.display, (0,0))
            # pygame.display.update()
            self.resetKeys()

    def checkEvents(self):
        
        if self.playing:
            keys = pygame.key.get_pressed()

            # Traslacion de camara
            if keys[K_d]:
                self.rend.camPosition.x += 1 * self.deltaTime
            if keys[K_a]:
                self.rend.camPosition.x -= 1 * self.deltaTime
            if keys[K_s]:
                self.rend.camPosition.z += 1 * self.deltaTime
            if keys[K_w]:
                self.rend.camPosition.z -= 1 * self.deltaTime
            if keys[K_DOWN]:
                self.rend.camPosition.y -= 1 * self.deltaTime
            if keys[K_UP]:
                self.rend.camPosition.y += 1 * self.deltaTime

            if keys[K_q]:
                if self.rend.valor > 0:
                    self.rend.valor -= 0.1 * self.deltaTime

            if keys[K_e]:
                if self.rend.valor < 0.2:
                    self.rend.valor += 0.1 * self.deltaTime

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False

            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    self.playing, self.isPaused = False, True
                    self.curr_menu.run_display = True
                
                # Menu handling
                if ev.key == pygame.K_RETURN and not self.playing:
                    self.START_KEY = True
                elif ev.key == pygame.K_BACKSPACE and not self.playing:
                    self.BACK_KEY = True
                elif ev.key == pygame.K_DOWN and not self.playing:
                    self.DOWN_KEY = True
                elif ev.key == pygame.K_UP and not self.playing:
                    self.UP_KEY = True
                
                if self.isPaused:
                    if ev.key == pygame.K_ESCAPE:
                        self.playing, self.isPaused = True, False
                        self.curr_menu.run_display = False

                if not self.isPaused and self.playing:
                    if ev.key == K_1:
                        self.rend.filledMode()
                    if ev.key == K_2:
                        self.rend.wireframeMode()
                    if ev.key == K_f:
                        self.rend.changeActiveModel()
    
    def resetKeys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def drawText(self, text, size, x, y):
        # font = pygame.font.SysFont(self.fontName, size)
        text_surface = self.font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)