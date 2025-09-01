## main.py
import pygame
import sys
from menu import Menu
from jogo import Jogo

pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Click Rush")

def game_over_screen(tela, largura, altura, score):
    fonte_title = pygame.font.Font(None, 96)
    fonte_botao = pygame.font.Font(None, 48)
    clock = pygame.time.Clock()

    w = 300; h = 70
    cx = largura // 2
    btn_reiniciar = pygame.Rect(cx - w//2, 300, w, h)
    btn_menu = pygame.Rect(cx - w//2, 390, w, h)
    btn_sair = pygame.Rect(cx - w//2, 480, w, h)

    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        tela.fill((0,0,0))

        # Título (bordas e brilho)
        title_surf = fonte_title.render("GAME OVER", True, (255,0,0))
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            bord = fonte_title.render("GAME OVER", True, (255,255,255))
            rect = bord.get_rect(center=(cx + dx, 140 + dy))
            tela.blit(bord, rect.topleft)
        rect = title_surf.get_rect(center=(cx, 140))
        tela.blit(title_surf, rect.topleft)

        # score
        fonte_info = pygame.font.Font(None, 36)
        score_surf = fonte_info.render(f"Sua pontuação: {score}", True, (255,255,255))
        score_rect = score_surf.get_rect(center=(cx, 210))
        tela.blit(score_surf, score_rect.topleft)

        # desenhar botões (capsule)
        def draw_capsule(rect, text):
            sombra = pygame.Rect(rect.x+6, rect.y+6, rect.w, rect.h)
            pygame.draw.rect(tela, (40,10,10), sombra, border_radius=40)
            pygame.draw.rect(tela, (200,10,10), rect, border_radius=40)
            pygame.draw.rect(tela, (120,0,0), rect, 4, border_radius=40)
            brilho = pygame.Surface((rect.width, rect.height//2), pygame.SRCALPHA)
            pygame.draw.ellipse(brilho, (255,255,255,60), (0, -rect.height//3, rect.width, rect.height))
            tela.blit(brilho, (rect.x, rect.y))
            txt = fonte_botao.render(text, True, (255,255,255))
            txt_r = txt.get_rect(center=rect.center)
            tela.blit(txt, txt_r)

        draw_capsule(btn_reiniciar, "Reiniciar")
        draw_capsule(btn_menu, "Menu")
        draw_capsule(btn_sair, "Sair")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_reiniciar.collidepoint(event.pos):
                    return "reiniciar"
                if btn_menu.collidepoint(event.pos):
                    return "menu"
                if btn_sair.collidepoint(event.pos):
                    pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "reiniciar"
                if event.key == pygame.K_m:
                    return "menu"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(60)


def main():
    while True:
        menu = Menu(tela, LARGURA, ALTURA)
        escolha = menu.run()  # "jogo" or exit handled inside

        if escolha == "jogo":
            jogo = Jogo(tela, LARGURA, ALTURA)
            resultado, score = jogo.run()
            if resultado == 'menu':
                continue
            elif resultado == 'gameover':
                action = game_over_screen(tela, LARGURA, ALTURA, score)
                if action == "reiniciar":
                    # reinicia imediatamente (volta ao loop e inicia novamente)
                    continue
                elif action == "menu":
                    continue
                else:
                    # sair tratado dentro game_over_screen
                    pass

if __name__ == "__main__":
    main()
