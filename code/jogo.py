# jogo.py
import pygame
import sys
import os
from circulo import Circulo
from jogador import Jogador

class Jogo:
    def __init__(self, tela, largura=800, altura=600):
        self.tela = tela
        self.largura = largura
        self.altura = altura

        self.base_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.base_dir, "assets")

        self.fundo = self._carregar_fundo()

        self.circulo = Circulo(largura, altura, raio=40)
        self.jogador = Jogador(vidas=3)

        self.font_hud = pygame.font.Font(None, 28)
        self.clock = pygame.time.Clock()

        self.total_time_sec = 30
        self.start_time = pygame.time.get_ticks()

        self._set_time_limit()
        self.spawn_time = pygame.time.get_ticks()

    def _carregar_fundo(self):
        candidatos = ["fundo.png", "fundo.jpg", "fundo.jpeg", "fundo.bmp"]
        for nome in candidatos:
            caminho = os.path.join(self.assets_dir, nome)
            if os.path.exists(caminho):
                try:
                    img = pygame.image.load(caminho).convert()
                    img = pygame.transform.scale(img, (self.largura, self.altura))
                    return img
                except pygame.error:
                    pass
        return None

    def _set_time_limit(self):
        base = 2000
        decrease = 200 * (self.jogador.phase - 1)
        min_ms = 400
        self.time_limit_ms = max(min_ms, base - decrease)

    def _draw_background(self):
        if self.fundo is not None:
            self.tela.blit(self.fundo, (0,0))
        else:
            self.tela.fill((10,10,10))

    def _draw_hud(self):
        now = pygame.time.get_ticks()
        elapsed_total = (now - self.start_time) // 1000
        remaining_total = max(0, self.total_time_sec - elapsed_total)

        score_surf = self.font_hud.render(f"Pontos: {self.jogador.score}", True, (255,255,255))
        phase_surf = self.font_hud.render(f"Fase: {self.jogador.phase}", True, (255,255,255))
        lives_surf = self.font_hud.render(f"Vidas: {self.jogador.lives}", True, (255,255,255))
        time_surf = self.font_hud.render(f"Tempo: {remaining_total}s", True, (255,255,255))

        self.tela.blit(score_surf, (10, 10))
        self.tela.blit(phase_surf, (10, 34))
        self.tela.blit(lives_surf, (10, 58))
        self.tela.blit(time_surf, (10, 82))

    def run(self):
        # retorna ('gameover', score) ou ('menu', None)
        while True:
            now = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return ('menu', None)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.circulo.verificar_clique(event.pos):
                        self.jogador.add_point()
                        self._set_time_limit()
                        self.circulo.reposicionar()
                        self.spawn_time = pygame.time.get_ticks()
                    else:
                        self.jogador.lose_life()
                        if self.jogador.lives <= 0:
                            return ('gameover', self.jogador.score)

            # verifica se tempo do circulo expirou
            if now - self.spawn_time > self.time_limit_ms:
                self.jogador.lose_life()
                if self.jogador.lives <= 0:
                    return ('gameover', self.jogador.score)
                self.circulo.reposicionar()
                self.spawn_time = pygame.time.get_ticks()

            # verifica tempo total do jogo
            elapsed_total = (now - self.start_time) // 1000
            if elapsed_total >= self.total_time_sec:
                return ('gameover', self.jogador.score)

            # desenhar
            self._draw_background()
            self.circulo.desenhar(self.tela)
            self._draw_hud()

            pygame.display.flip()
            self.clock.tick(60)
