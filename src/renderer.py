import pygame
from pygame.locals import *
from pygame import mixer
from game import Game
import numpy as np
from gl import Renderer, ModelObj
import shaders
import glm

width = 500
height = 500

# g = Game(width, height)

deltaTime = 0.0

pygame.init()
screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.OPENGL )
clock = pygame.time.Clock()
pygame.display.set_caption("OpenGL Renderer")

# Background music
mixer.music.load('res/sfx/backgroundMusic.wav')
mixer.music.play(-1)

rend = Renderer(screen)
rend.setShaders(shaders.vertex_shader, shaders.fragment_shader)

face = ModelObj('res/obj/model.obj', 'res/textures/model.bmp')
pyr = ModelObj('res/obj/triangular.obj', 'res/textures/pyramid.bmp')
homer = ModelObj('res/obj/homer.obj', 'res/textures/homer.bmp')
weir = ModelObj('res/obj/coin.obj', 'res/textures/coin.jpg')

face.position.z = -5
pyr.position.z = -5
homer.position.z = -5
weir.position.z = -5

rend.activeModel = face

rend.scene.append(face)
rend.scene.append(pyr)
rend.scene.append(homer)
rend.scene.append(weir)

# print(glm.cross(glm.vec3(1,2,3), glm.vec3(4,5,6)))
# print(glm.normalize(glm.vec3(1,2,3) - glm.vec3(4,5,6)))
# print(glm.vec3(1,2,3) - glm.vec3(4,5,6))
# print(glm.mat2([[1,1],[2,3]]))

isRunning = True
while isRunning:


    keys = pygame.key.get_pressed()

    # Traslacion de camara
    if keys[K_d]:
        rend.camPosition.x += 1 * deltaTime
    if keys[K_a]:
        rend.camPosition.x -= 1 * deltaTime
    if keys[K_s]:
        rend.camPosition.z += 1 * deltaTime
    if keys[K_w]:
        rend.camPosition.z -= 1 * deltaTime
    if keys[K_DOWN]:
        rend.camPosition.y -= 1 * deltaTime
    if keys[K_UP]:
        rend.camPosition.y += 1 * deltaTime

    if keys[K_q]:
        if rend.valor > 0:
            rend.valor -= 0.1 * deltaTime

    if keys[K_e]:
        if rend.valor < 0.2:
            rend.valor += 0.1 * deltaTime

    # Rotacion de camara
    if keys[K_LEFT]:
        rend.camRotation.y += 15 * deltaTime
    if keys[K_RIGHT]:
        rend.camRotation.y -= 15 * deltaTime

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False

        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False

            if ev.key == K_1:
                rend.filledMode()
            if ev.key == K_2:
                rend.wireframeMode()
            if ev.key == K_f:
                rend.changeActiveModel()

    rend.time += deltaTime
    deltaTime = clock.tick(60) / 1000

    rend.update()
    rend.render()

    pygame.display.flip()

# while g.running:
#     g.curr_menu.displayMenu()
#     g.gameLoop()

pygame.quit()
