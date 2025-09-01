# circulo.py
import pygame
import random

class Circulo:
    def __init__(self, largura, altura, raio=40, cor=(255,0,0)):
        self.largura = largura
        self.altura = altura
        self.raio = raio
        self.cor = cor
        self.reposicionar()

    def reposicionar(self):
        # evita ficar em cima do HUD/título: desloca y para baixo de 120px
        self.pos_x = random.randint(self.raio, self.largura - self.raio)
        self.pos_y = random.randint(self.raio + 120, self.altura - self.raio)

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (self.pos_x, self.pos_y), self.raio)
        pygame.draw.circle(tela, (255,255,255), (self.pos_x, self.pos_y), self.raio, 3)

    def verificar_clique(self, pos):
        mx, my = pos
        dx = mx - self.pos_x
        dy = my - self.pos_y
        distancia = (dx*dx + dy*dy) ** 0.5
        return distancia <= self.raio
