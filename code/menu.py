# menu.py
import pygame
import sys

class Menu:
    def __init__(self, tela, largura, altura):
        self.tela = tela
        self.largura = largura
        self.altura = altura

        # fontes
        self.fonte_titulo = pygame.font.Font(None, 120)
        self.fonte_botao = pygame.font.Font(None, 56)

        # botões
        self.botao_largura = 300
        self.botao_altura = 80
        cx = largura // 2
        y_start = 260
        espaçamento = 120

        self.buttons = [
            {"text": "Iniciar", "rect": pygame.Rect(cx - self.botao_largura//2, y_start, self.botao_largura, self.botao_altura)},
            {"text": "Sair",    "rect": pygame.Rect(cx - self.botao_largura//2, y_start + espaçamento, self.botao_largura, self.botao_altura)}
        ]

        self.selected = 0

    def _draw_title(self):
        texto = "Click Rush"
        base = self.fonte_titulo.render(texto, True, (255,0,0))
        borda = self.fonte_titulo.render(texto, True, (255,255,255))
        sombra = self.fonte_titulo.render(texto, True, (30,30,30))
        rect = base.get_rect(center=(self.largura//2, 120))

        # sombra atrás
        self.tela.blit(sombra, (rect.x + 6, rect.y + 6))

        # borda forte (vários offsets)
        offsets = [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,-2),(-2,2),(2,2)]
        for dx, dy in offsets:
            self.tela.blit(borda, (rect.x + dx, rect.y + dy))

        # texto vermelho principal
        self.tela.blit(base, rect.topleft)

        # brilho superior
        brilho = pygame.Surface((rect.width, rect.height//2), pygame.SRCALPHA)
        pygame.draw.ellipse(brilho, (255,255,255,60), (0, -rect.height//3, rect.width, rect.height))
        self.tela.blit(brilho, rect.topleft)

    def _draw_button(self, button, active=False, mouse_over=False, clicked=False):
        rect = button["rect"]
        x, y, w, h = rect
        # sombra do botão
        sombra_rect = pygame.Rect(x+6, y+6, w, h)
        pygame.draw.rect(self.tela, (40,10,10), sombra_rect, border_radius=40)

        # cor base (mais claro se hover/active)
        cor_base = (200, 10, 10) if not (mouse_over or active) else (235, 30, 30)

        # se clicado, expandir (efeito "pressionado")
        draw_rect = pygame.Rect(x, y, w, h)
        if clicked:
            draw_rect = draw_rect.inflate(12, 8)
            draw_rect.x -= 6
            draw_rect.y -= 4

        # corpo e borda (cápsula)
        pygame.draw.rect(self.tela, cor_base, draw_rect, border_radius=40)
        pygame.draw.rect(self.tela, (120,0,0), draw_rect, 4, border_radius=40)

        # brilho na parte superior do botão
        brilho = pygame.Surface((draw_rect.width, draw_rect.height//2), pygame.SRCALPHA)
        pygame.draw.ellipse(brilho, (255,255,255,60), (0, -draw_rect.height//3, draw_rect.width, draw_rect.height))
        self.tela.blit(brilho, (draw_rect.x, draw_rect.y))

        # texto no centro
        txt = self.fonte_botao.render(button["text"], True, (255,255,255))
        txt_rect = txt.get_rect(center=draw_rect.center)
        self.tela.blit(txt, txt_rect)

        return draw_rect

    def run(self):
        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()

            # === EVENTOS: tratamos eventos primeiro para garantir clique confiável ===
            clicked_button_index = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # teclado: navegação e ENTER
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.buttons)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.buttons)
                    elif event.key == pygame.K_RETURN:
                        if self.selected == 0:
                            return "jogo"
                        elif self.selected == 1:
                            pygame.quit()
                            sys.exit()

                # clique do mouse: verificado via event.pos (muito mais confiável)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, b in enumerate(self.buttons):
                        if b["rect"].collidepoint(event.pos):
                            clicked_button_index = i
                            break

            # se um botão foi clicado durante o loop de eventos, processa a ação imediatamente
            if clicked_button_index is not None:
                if clicked_button_index == 0:
                    return "jogo"
                elif clicked_button_index == 1:
                    pygame.quit()
                    sys.exit()

            # === DESENHO: depois de processar eventos ===
            self.tela.fill((0,0,0))
            self._draw_title()

            # desenha botões com hover/pressed visuals
            mouse_pressed = pygame.mouse.get_pressed()[0]
            for i, b in enumerate(self.buttons):
                is_selected = (i == self.selected)
                mouse_over = b["rect"].collidepoint(mouse_pos)
                # para efeito visual: consideramos "clicked" quando mouse está pressionado em cima
                clicked = mouse_over and mouse_pressed
                self._draw_button(b, active=is_selected, mouse_over=mouse_over, clicked=clicked)

            pygame.display.flip()
            clock.tick(60)
