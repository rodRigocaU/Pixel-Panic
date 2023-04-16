import pygame
import time
import random
import sys
import math

# Para importar funcion main de nivel 1 que ejecute todo el nivel
#sys.path.append('./Code/Level_1')
#import nivel1


pygame.init()

WIDTH = 800
HEIGHT = 600

# Definir los colores que se van a utilizar
GREEN2 = (0,255,0)
WHITE = (255, 255, 255)
GREEN = (127, 255, 212)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Panic Pixel")

# Crear una nueva superficie para el título
font = pygame.font.Font(None, 72)
font.set_bold(True)
text = font.render("Panic Pixel", True, (255, 255, 255))
text_rect = text.get_rect(center=(WIDTH // 2, 50))


# Cargar los fondos y escalarlos al tamaño de la ventana
background1 = pygame.image.load("./Assets/fondos/fondoMenu1.jpg").convert()
background1 = pygame.transform.scale(background1, (WIDTH, HEIGHT))

background2 = pygame.image.load("./Assets/fondos/fondoMenu2.jpg").convert()
background2 = pygame.transform.scale(background2, (WIDTH, HEIGHT))

#Reproducir musica para el menu
#music = pygame.mixer.Sound("./assets/musica/musica1.mp3")
#music.play()

# Botones texto
font_button = pygame.font.Font(None, 60)
font_button_hover = pygame.font.Font(None, 72)

# Renderizar los textos de los botones
button1_text = font_button.render("Jugar", True, GREEN2)
button2_text = font_button.render("Salir", True, GREEN2)

# Renderizar los textos de los botones al pasar el mouse
button1_text_hover = font_button_hover.render("Jugar", True, GREEN)
button2_text_hover = font_button_hover.render("Salir", True, GREEN)

# Obtener los rectángulos de los textos
button1_rect = button1_text.get_rect()
button2_rect = button2_text.get_rect()
button1_rect.center = (WIDTH // 2, HEIGHT // 2 - (WIDTH // 20) )
button2_rect.center = (WIDTH // 2, HEIGHT // 2 + 100)

# Obtener los rectángulos de los textos
button1_rect_hover = button1_text_hover.get_rect()
button2_rect_hover = button2_text_hover.get_rect()
button1_rect_hover.center = (WIDTH // 2, HEIGHT // 2 - (WIDTH // 20) )
button2_rect_hover.center = (WIDTH // 2, HEIGHT // 2 + 100)


should_shake = False
in_transition = False
zoom = 1.0
alpha = 0
transition_speed = 3

def zoom_transition(background, alpha):
    global zoom, should_shake

    zoom += 0.01
    scale_factor = math.pow(zoom, 2.0)

    # Crear una nueva superficie centrada en la ventana que tenga la imagen de fondo escalada
    background_scaled = pygame.transform.scale(background, (int(background.get_width() * scale_factor), int(background.get_height() * scale_factor)))
    scaled_surface = pygame.Surface((WIDTH, HEIGHT))
    scaled_rect = background_scaled.get_rect(center=scaled_surface.get_rect().center)
    scaled_surface.blit(background_scaled, scaled_rect)

    if should_shake:
        x_offset = random.randint(-5, 5)
        y_offset = random.uniform(-2, 2)
        screen.blit(scaled_surface, (x_offset, y_offset))
    else:
        screen.blit(scaled_surface, (0, 0))

    white_surface = pygame.Surface((int(WIDTH * scale_factor), int(HEIGHT * scale_factor)))
    white_surface.set_alpha(alpha)
    white_surface.fill((255, 255, 255))
    white_surface_scaled = pygame.transform.scale(white_surface, (WIDTH, HEIGHT))
    screen.blit(white_surface_scaled, (0, 0))

    return scaled_surface

def alpha_transition(background, alpha):
    screen.blit(background, (0, 0))
    white_surface = pygame.Surface((WIDTH, HEIGHT))
    white_surface.set_alpha(alpha)
    white_surface.fill((255, 255, 255))
    screen.blit(white_surface, (0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Verificar si se hizo clic en un botón
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos

            # Verificar si se hizo clic en el botón "Comenzar juego"
            if button1_rect_hover.collidepoint(mouse_pos):
                in_transition = True
                should_shake = True

                #Parar musica para colocar musica de transicion y proximo nivel
                #music.stop()
                background1 = background2

                # Realizar la transición de fondo y efecto de zoom de forma simultanea
                while alpha < 255:
                    alpha += transition_speed
                    background1_scaled = zoom_transition(background1, alpha)
                    pygame.display.update()

                should_shake = False
                in_transition = False
                
                # Llama a que se ejecute nivel
                
                # result_nivel1 = nivel1.main()
                # if result_nivel2 == "quit" or result_nivel2 == "lose":
                #     running = False
                #     pygame.quit()
                #     sys.exit()


            # Verificar si se hizo clic en el botón "Salir"
            elif button2_rect_hover.collidepoint(mouse_pos):
                running = False
                pygame.quit()
                sys.exit()


    # Obtener la posición del cursor del mouse
    mouse_pos = pygame.mouse.get_pos()

    if button1_rect.collidepoint(mouse_pos):
        button1_text_rendered = button1_text_hover
        button1_rect_rendered = button1_rect_hover
    else:
        button1_text_rendered = button1_text
        button1_rect_rendered = button1_rect

    if button2_rect.collidepoint(mouse_pos):
        button2_text_rendered = button2_text_hover
        button2_rect_rendered = button2_rect_hover
    else:
        button2_text_rendered = button2_text
        button2_rect_rendered = button2_rect


    if in_transition:
        background1_scaled = zoom_transition(background1, alpha)
        pygame.display.update()

    else:
        # Calcular la posición centrada de la imagen no escalada
        rect = background1.get_rect()
        rect.center = screen.get_rect().center

        screen.blit(background1, rect)

        # Dibujar el titulo y botones en la pantalla
        screen.blit(text, text_rect)
        screen.blit(button1_text_rendered, button1_rect_rendered)
        screen.blit(button2_text_rendered, button2_rect_rendered)

        # Actualizar la pantalla
        pygame.display.update()