import pygame
import random

# Inicializa todos los módulos de Pygame
pygame.init()

# Configurar la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Galactic Gunner")


# Colores
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (64, 255, 0)

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

# Balas (Disparos)
bullets = []
bullet_width = 3
bullet_height = 7
bullet_speed = -10
last_shot_time = 0
shoot_delay = 200  # Retraso de disparo en milisegundos

# Power-up
power_up = None
power_up_active = False
power_up_duration = 5000
power_up_start_time = 0
power_up_health_increase = 25  # Aumento de salud al recoger un power-up


# Cargar imágenes
background_img = pygame.image.load("assets/fondo_espacio.jpg")
player_img = pygame.image.load("assets/player.png")
obstacle_img = pygame.image.load("assets/enemigo.jpg")
power_up_img = pygame.image.load("assets/power_up.png")
explosion_img = pygame.image.load("assets/explosion.png")


# Ajustar tamño de las imágenenes
player_img = pygame.transform.scale(player_img,(70,70))
obstacle_img = pygame.transform.scale(obstacle_img,(40,40))
power_up_img = pygame.transform.scale(power_up_img, (30, 30))
explosion_img = pygame.transform.scale(explosion_img, (50, 50))

# Puntuación
score = 0
high_score = 0 # Puntuación más alta
font = pygame.font.Font(None, 24)
#--------------------------------------------------
# Vidas del jugador
max_health = 100
current_health = max_health

# Variables del juego
max_obstacles = 4
level = 1
score_to_next_level = 50
explosions = []  # Para manejar las explosiones
running = True
paused = False
game_over_screen = False
explosion_duration = 300  # Duración en milisegundos


# Música de fonndo y efectos de sonido
pygame.mixer.music.load("assets/hysteria.mp3") #####O MIXER_MUSIC???
pygame.mixer.music.play(-1) # Repite la canción infinitas veces
collision_sound = pygame.mixer.Sound("assets/collision.mp3")
explosion_sound = pygame.mixer.Sound("assets/explosion.mp3")


#--------------------------------------------------
# Reloj para controlar FPS 
clock = pygame.time.Clock()

#--------------------------------------------------

def start_menu():
    """Pantalla de inicio del juego."""
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        draw_text("Galactic Gunner", font, WHITE, WIDTH//2 - 50, HEIGHT//2 - 50)
        draw_text("Presiona 'S' para iniciar", font, WHITE, WIDTH // 2 - 100, HEIGHT // 2)
        draw_text("Presiona 'Q' para salir", font, WHITE, WIDTH // 2 - 100, HEIGHT // 2 + 40)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu_running = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return False
    return True


def draw_text(text, font, color, x, y):
    """Función para dibujar texto en pantalla."""
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

def game_over():
    """Pantalla de Game Over."""
    screen.fill(BLACK)
    draw_text(f"Game Over! Puntuación: {score}", font, RED, WIDTH//2 - 100, HEIGHT//2)
    draw_text("Presiona 'R' para reiniciar o 'Q' para salir", font, WHITE, WIDTH // 2 - 150, HEIGHT // 2 + 40)
    pygame.display.flip()
    # pygame.time.wait(3000)  # Espera 3 segundos antes de cerrar el juego
#--------------------------------------------------
def draw_health_bar(screen, x, y, health, max_health):
    bar_width = 100
    bar_height = 10
    fill = (health / max_health) * bar_width
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(screen, RED, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)

def restart_game():
    global player, bullets, obstacles, score, current_health, level, max_obstacles, power_up_active
    player.x = WIDTH // 2 - player_width // 2
    player.y = HEIGHT - player_height - 10
    bullets.clear()
    obstacles.clear()
    score = 0
    current_health = max_health
    level = 1
    max_obstacles = 4
    power_up_active = False


#-----------------------

# Mostrar la pantalla de inicio
if not start_menu():
    running = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # .quit no es un tipo de evento. Es una función
            running = False
            
    

    keys = pygame.key.get_pressed() # Tecla que ha sido presionada
#--------------------------------------------------
# Pantalla de Game Over
    if game_over_screen:
        game_over()
        if keys[pygame.K_r]:
            game_over_screen = False
            restart_game()
        if keys[pygame.K_q]:
            running = False
        continue
    
    
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
        
    
     # Disparar balas con la tecla espacio
    if keys[pygame.K_SPACE] and pygame.time.get_ticks() - last_shot_time > shoot_delay:
        bullet = pygame.Rect(player.centerx - bullet_width // 2, player.top, bullet_width, bullet_height)
        bullets.append(bullet)
        last_shot_time = pygame.time.get_ticks()

    # Mover las balas
    for bullet in bullets:
        bullet.y += bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)  # Eliminar balas que salen de la pantalla
    
    
    
        
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
    
    #   # Aumentar dificultad con la puntuación
    # if score >= last_difficulty_increase + difficulty_increment_score:
    #     max_obstacles += 1
    #     last_difficulty_increase = score  # Actualiza el último puntaje en el que se incrementó la dificultad
    #     for i in range(len(obstacles)):
    #         obstacles[i] = (obstacles[i][0], obstacles[i][1] + 1)  # Aumentar velocidad de los obstáculos

# Aumentar nivel
    if score >= score_to_next_level:
        level += 1
        max_obstacles += 2
        score_to_next_level += 50 * level
        
        
    # Detectar colisiones
    for obstacle_info in obstacles:
        obstacle, _ = obstacle_info
        if player.colliderect(obstacle):
            collision_sound.play()  # Reproducir sonido de colisión
            #lives -= 1  # Restar una vida
            current_health -= 20

            obstacles.remove(obstacle_info)  # Eliminar obstáculo que choca
            if current_health <= 0:
                if score > high_score:
                    high_score = score  # Actualizar la puntuación más alta
                # running = False  # Terminar el juego
                game_over_screen = True
                
    
     # Detectar colisiones entre balas y obstáculos
    for bullet in bullets:
        for obstacle_info in obstacles:
            obstacle, _ = obstacle_info
            if bullet.colliderect(obstacle):
                bullets.remove(bullet)
                obstacles.remove(obstacle_info)
                score += 1  # Incrementar la puntuación cuando se destruye un obstáculo
                explosion_sound.play()
                # explosions.append([explosion_img, obstacle.center])
                explosions.append([explosion_img, obstacle.center, pygame.time.get_ticks()])

                break         
    
    
     # Generar power-up aleatoriamente
    if power_up is None and random.randint(0, 1000) < 5:  # Probabilidad baja
        power_up = pygame.Rect(random.randint(0, WIDTH - 30), random.randint(0, HEIGHT - 30), 30, 30)

    # Colisión con power-up
    if power_up and player.colliderect(power_up):
        power_up_active = True
        power_up_start_time = pygame.time.get_ticks()
        current_health = min(max_health, current_health + power_up_health_increase)  # Aumenta vida sin exceder el máximo
        power_up = None

    # Verificar si el power-up ha expirado
    if power_up_active and pygame.time.get_ticks() - power_up_start_time > power_up_duration:
        power_up_active = False
        
        
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
    
    # Dibuja las balas
    for bullet in bullets:
        pygame.draw.rect(screen, GREEN, bullet)
        
     # Dibujar power-up
    if power_up:
        screen.blit(power_up_img, power_up)
        
    for explosion in explosions[:]:
        img, pos, time = explosion
        if pygame.time.get_ticks() - time > explosion_duration:
            explosions.remove(explosion)
        else:
            screen.blit(img, pos)
        
    # Mostrar puntuación y vidas
    # draw_text(f"Puntuación: {score}", font, WHITE, 10, 10)
    # draw_text(f"Vidas: {lives}", font, RED, 10, 30)
    # draw_text(f"Puntuación más alta: {high_score}", font, WHITE, 10, 50)
    # Mostrar puntuación y nivel
    draw_text(f"Puntuación: {score}", font, WHITE, 10, 10)
    draw_text(f"Nivel: {level}", font, WHITE, 10, 30)
    draw_text(f"Puntuación más alta: {high_score}", font, WHITE, 10, 50)

    # Mostrar barra de vida
    draw_health_bar(screen, 10, 70, current_health, max_health)
    
    pygame.display.flip() # Actualiza la pantalla
    clock.tick(60)

pygame.quit()