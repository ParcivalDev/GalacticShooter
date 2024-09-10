import pygame
import random

# Inicializa todos los módulos de Pygame
pygame.init()

# Configurar la pantalla
WIDTH = 800  # ancho
HEIGHT = 600 # alto

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SuperHeroe")


# Colores
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

# Jugador
player_color = WHITE
player_width = 50
player_height = 50
player = pygame.Rect(WIDTH//2 - player_width //2, 
                     HEIGHT - player_height - 10, 
                     player_width, 
                     player_height)
# Con doble / toma el entero de la división
# Al ancho de la ventana se le resta el ancho del personaje para que estea en el centro de la ventana


# Obstáculo
obstacle_width = 30
obstacle_height = 30
obstacle_color = RED
obstacles = [] # Inicialmente no hay ningún meteorito en la lista


# Cargar imágenes
background_img = pygame.image.load("fondo_espacio.jpg")
player_img = pygame.image.load("player.png")
obstacle_img = pygame.image.load("enemigo.jpg")

player_img = pygame.transform.scale(player_img,(70,70))
obstacle_img = pygame.transform.scale(obstacle_img,(40,40))


# Puntuación
score = 0
font = pygame.font.Font(None, 24)

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal del juego para que la ventana no se cierre
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # .quit no es un tipo de evento. Es una función
            print("Cerrando..")
            running = False

    keys = pygame.key.get_pressed() # Tecla que ha sido presionada
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.left > 10: # Si pongo 0 tocará el borde. Sin los () se sale del mapa
        player.x -= 5
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right < WIDTH - 10: # Si pongo 0 tocará el borde
        player.x += 5

    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.top > 10: # Si pongo 0 tocará el borde superior
        player.y -= 5
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.bottom < HEIGHT - 10: # Si pongo 0 tocará el borde
        player.y += 5
        # Una vez que el borde inferior del jugador toca o supera el límite establecido (HEIGHT - 10), el jugador se detiene y no puede moverse más abajo
        
        
    # Generación de obstáculos de manera random
    if len(obstacles)<8:
        obstacle = pygame.Rect(random.randint(0,WIDTH - obstacle_width), 0, obstacle_width, obstacle_height) 
        velocidad = random.randint(5,10)
        # Para que no genere obstáculos cortados en el eje X
        obstacles.append((obstacle,velocidad)) # Se guarda cada obstáculo con su velocidad
    
    # Mover los obstáculos
    for obstacle_info in obstacles:
        obstacle, velocidad = obstacle_info # Desempaqueta la tupla en dos variables
        obstacle.y += velocidad
        if obstacle.top > HEIGHT:
            obstacles.remove(obstacle_info) # Cuando los obstáculos pasen del alto de la ventana estos desaparecen de la lista y así se generan unos nuevos
            score += 1 # Para aumentar la puntuación
    
    # Detectar colisiones
    for obstacle_info in obstacles:
        obstacle, _ = obstacle_info
        if player.colliderect(obstacle):
            print("¡Colisión detectada!")
            running = False
    
    
    screen.fill(BLACK) # Pinta la pantalla
    screen.blit(background_img, (0,0)) # Imagen de fondo. Se coloca de primero para no tapar el contenido
    
    
    #pygame.draw.rect(screen, player_color, player) # Dibuja el jugador
    screen.blit(player_img, player)
    
    for obstacle_info in obstacles:
        obstacle, _ = obstacle_info # Ignoramos la velocidad con guión bajo
        #pygame.draw.rect(screen, obstacle_color, obstacle) # Dibuja los obstáculos
        screen.blit(obstacle_img,obstacle)
        
    # Mostrar puntuación
    score_text = font.render(f"Puntuación: {score}", True, WHITE)  # True para que no salga pixelado
    screen.blit(score_text, (10,10))
    
    pygame.display.flip() # Actualiza la pantalla
    clock.tick(60)

pygame.quit()