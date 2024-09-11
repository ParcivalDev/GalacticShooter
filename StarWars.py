import pygame
import random

# Inicializa todos los módulos de Pygame
pygame.init()

# Configurar la pantalla
WIDTH = 800  # ancho
HEIGHT = 600 # alto

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Star Wars")


# Colores
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

# Jugador
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
obstacles = [] # Inicialmente no hay ningún meteorito en la lista


# Cargar imágenes
background_img = pygame.image.load("fondo_espacio.jpg")
player_img = pygame.image.load("player.png")
obstacle_img = pygame.image.load("enemigo.jpg")

# Ajustar tamño de las imágenenes
player_img = pygame.transform.scale(player_img,(70,70))
obstacle_img = pygame.transform.scale(obstacle_img,(40,40))


# Puntuación
score = 0
high_score = 0 # Puntuación más alta
font = pygame.font.Font(None, 24)
#--------------------------------------------------
# Vidas del jugador
lives = 3

# Música de fonndo y efectos de sonido
pygame.mixer.music.load("hysteria.mp3") #####O MIXER_MUSIC???
pygame.mixer.music.play(-1) # Repite la canción infinitas veces
collision_sound = pygame.mixer.Sound("collision.mp3")
#--------------------------------------------------
# Reloj para controlar FPS 
clock = pygame.time.Clock()

#--------------------------------------------------
# Variables para controlar la dificultad y el fondo animado
difficulty_increment_score = 40
max_obstacles = 4  # Empieza con 2
# Variable para recordar el puntaje en el que la dificultad aumentó por última vez
last_difficulty_increase = 0
# Pausar el juego
paused = False

def draw_text(text, font, color, x, y):
    """Función para dibujar texto en pantalla."""
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

def game_over():
    """Pantalla de Game Over."""
    screen.fill(BLACK)
    draw_text(f"Game Over! Puntuación: {score}", font, RED, WIDTH//2 - 100, HEIGHT//2)
    pygame.display.flip()
    pygame.time.wait(3000)  # Espera 3 segundos antes de cerrar el juego
#--------------------------------------------------

# Bucle principal del juego para que la ventana no se cierre
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # .quit no es un tipo de evento. Es una función
            running = False
            
    

    keys = pygame.key.get_pressed() # Tecla que ha sido presionada
#--------------------------------------------------
    # Pausar el juego correctamente
    if keys[pygame.K_p]:
        pygame.time.wait(300)  # Esperar 300 ms para evitar múltiples cambios rápidos
        paused = not paused

    
    if paused:
        continue  # Salta el ciclo si el juego está en pausa
#--------------------------------------------------
    
    
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
    if len(obstacles)<max_obstacles:
        obstacle = pygame.Rect(random.randint(0,WIDTH - obstacle_width), 0, obstacle_width, obstacle_height) 
        velocidad = random.randint(4,10)
        # Para que no genere obstáculos cortados en el eje X
        obstacles.append((obstacle,velocidad)) # Se guarda cada obstáculo con su velocidad
    
    # Mover los obstáculos
    for obstacle_info in obstacles:
        obstacle, velocidad = obstacle_info # Desempaqueta la tupla en dos variables
        obstacle.y += velocidad
        if obstacle.top > HEIGHT:
            obstacles.remove(obstacle_info) # Cuando los obstáculos pasen del alto de la ventana estos desaparecen de la lista y así se generan unos nuevos
            score += 1 # Para aumentar la puntuación
    
    # # Detectar colisiones
    # for obstacle_info in obstacles:
    #     obstacle, _ = obstacle_info
    #     if player.colliderect(obstacle):
    #         print("¡Colisión detectada!")
    #         running = False
    
      # Aumentar dificultad con la puntuación
    if score >= last_difficulty_increase + difficulty_increment_score:
        max_obstacles += 1
        last_difficulty_increase = score  # Actualiza el último puntaje en el que se incrementó la dificultad
        for i in range(len(obstacles)):
            obstacles[i] = (obstacles[i][0], obstacles[i][1] + 1)  # Aumentar velocidad de los obstáculos

    # Detectar colisiones
    for obstacle_info in obstacles:
        obstacle, _ = obstacle_info
        if player.colliderect(obstacle):
            collision_sound.play()  # Reproducir sonido de colisión
            lives -= 1  # Restar una vida
            obstacles.remove(obstacle_info)  # Eliminar obstáculo que choca
            if lives == 0:
                if score > high_score:
                    high_score = score  # Actualizar la puntuación más alta
                game_over()
                running = False  # Terminar el juego
                
                
    
    screen.blit(background_img, (0,0)) # Imagen de fondo. Se coloca de primero para no tapar el contenido
   # Actualizar el fondo


    #pygame.draw.rect(screen, player_color, player) # Dibuja el jugador
    screen.blit(player_img, player)
    
    for obstacle_info in obstacles:
        obstacle, _ = obstacle_info # Ignoramos la velocidad con guión bajo
        #pygame.draw.rect(screen, obstacle_color, obstacle) # Dibuja los obstáculos
        screen.blit(obstacle_img,obstacle)
        
    # Mostrar puntuación
    # score_text = font.render(f"Puntuación: {score}", True, WHITE)  # True para que no salga pixelado
    # screen.blit(score_text, (10,10))
    
    # Mostrar puntuación y vidas
    draw_text(f"Puntuación: {score}", font, WHITE, 10, 10)
    draw_text(f"Vidas: {lives}", font, RED, 10, 30)
    draw_text(f"Puntuación más alta: {high_score}", font, WHITE, 10, 50)

    
    pygame.display.flip() # Actualiza la pantalla
    clock.tick(60)

pygame.quit()