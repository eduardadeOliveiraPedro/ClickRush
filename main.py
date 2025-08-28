import pygame

print('Setup Start')
pygame.init()
window = pygame.display.set_mode(size = (600, 480))
print('Setup End')

print('Loop Start')
while True:
#cheque para todos os eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #fechar a janela
            quit() #encerrar o pygame
