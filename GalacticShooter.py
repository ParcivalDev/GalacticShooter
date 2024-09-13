"""
Galactic Shooter - Un juego de disparos en 2D
Autor: ParcivalDev
"""

import os  # Módulo para interactuar con el sistema de archivos
import sys  # Módulo para interactuar con el intérprete del sistema
import pygame  # Módulo para manejar gráficos y sonidos en videojuegos
import io  # Módulo para manejar datos en formato binario en memoria
import random  # Módulo para generar números aleatorios

# --------------------------------------------------
# Función para obtener la ruta del archivo actual
def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', None)
        if base_path:
            return os.path.join(base_path, relative_path)
        return os.path.join(os.path.dirname(__file__), relative_path)
    except Exception as e:
        print(f"Error al obtener la ruta del recurso: {e}")
        return None

# Función para obtener los datos binarios de un archivo
def get_resource_data(filename):
    # Obtiene la ruta del archivo
    filepath = resource_path(filename)
    if filepath:
        with open(filepath, 'rb') as f:  # Abre el archivo en modo lectura binaria
            return f.read()  # Lee y retorna los datos binarios del archivo
    raise FileNotFoundError(f"No se encontró el archivo: {filename}")

# Función para cargar una imagen desde los datos binarios
def load_image_from_data(data):
    return pygame.image.load(io.BytesIO(data))
# --------------------------------------------------


# Configurar la pantalla
WIDTH, HEIGHT = 800, 600
# Inicializa Pygame
pygame.init()
# Crea una ventana de 800x600 píxeles
screen = pygame.display.set_mode((800, 600))
# Establece el título de la ventana
pygame.display.set_caption("Galactic Shooter")

# --------------------------------------------------

# Cargar datos binarios de las imágenes
start_img_data = get_resource_data('assets/start.png')
game_over_img_data = get_resource_data('assets/game_over.png')
laser_img_data = get_resource_data('assets/laser.png')
background_img_data = get_resource_data('assets/fondo_espacio.jpg')
player_img_data = get_resource_data('assets/player.png')
obstacle_img_data = get_resource_data('assets/enemigo.jpg')
life_heart_img_data = get_resource_data('assets/life_heart.png')
explosion_img_data = get_resource_data('assets/explosion.png')


# Cargar y establecer el icono
icon_data = get_resource_data('assets/player.png')  # Reemplaza con la ruta a tu imagen de icono
icon_image = load_image_from_data(icon_data)  # Convertir datos binarios en una superficie
icon_image = pygame.transform.scale(icon_image, (32, 32))  # Escalar a 32x32 píxeles
pygame.display.set_icon(icon_image)  # Establecer la imagen como el ícono de la ventana

# Cargar imágenes desde los datos binarios
start_img = load_image_from_data(start_img_data)
game_over_img = load_image_from_data(game_over_img_data)
laser_img = load_image_from_data(laser_img_data)
background_img = load_image_from_data(background_img_data)
player_img = load_image_from_data(player_img_data)
obstacle_img = load_image_from_data(obstacle_img_data)
life_heart_img = load_image_from_data(life_heart_img_data)
explosion_img = load_image_from_data(explosion_img_data)


# Música de fonndo y efectos de sonido
pygame.mixer.music.load(resource_path("assets/hysteria.ogg"))
pygame.mixer.music.play(-1)  # Repite la canción infinitas veces
collision_sound = pygame.mixer.Sound(resource_path("assets/collision.ogg"))
explosion_sound = pygame.mixer.Sound(resource_path("assets/explosion.ogg"))
laser_shot_sound = pygame.mixer.Sound(resource_path("assets/laser_shot.ogg"))

# Ajustar el volumen de la música de fondo
pygame.mixer.music.set_volume(0.2)  # Volumen al 20%
# Ajustar el volumen del sonido de colisión
collision_sound.set_volume(0.25)  # Volumen al 25%
# Ajustar el volumen del sonido de explosión
explosion_sound.set_volume(0.5)  # Volumen al 50%
# Ajustar el volumen del disparo láser
laser_shot_sound.set_volume(0.03)  # Volumen al 3%

# --------------------------------------------------

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (64, 255, 0)

# Jugador
player_width = 70
player_height = 70
# Crea un rectángulo para el jugador y lo posiciona en el centro inferior de la ventana
player = pygame.Rect(WIDTH//2 - player_width // 2,
    HEIGHT - player_height - 10,
    player_width,
    player_height)
# Con doble / toma el entero de la división
# Al ancho de la ventana se le resta el ancho del personaje para que estea en el centro de la ventana

# Obstáculo
obstacle_width = 40
obstacle_height = 40
max_obstacles = 4
obstacles = []  # Inicialmente no hay ningún obstáculo en la lista

# Balas (Disparos)
bullets = []
bullet_width = 100
bullet_height = 120
bullet_speed = 10  # Velocidad de las balas. Es - porque van hacia arriba
last_shot_time = 0
shoot_delay = 500  # Retraso de disparo en milisegundos

# Power-up
life_heart = None  # Variable para almacenar el power-up (si existe)
life_heart_health_increase = 25  # Aumento de salud al recoger un power-up
life_heart_width = 35
life_heart_height = 20
# Puntuación
score = 0
level = 1
score_to_next_level = 25  # Puntuación necesaria para subir de nivel
high_score = 0  # Puntuación más alta
font = pygame.font.Font(None, 24)  # Fuente para mostrar el texto

# Vida del jugador
max_health = 100
current_health = max_health  # Salud actual del jugador

# Otras variables del juego
explosions = []  # Para manejar las explosiones
running = True
paused = False
game_over_screen = False
explosion_duration = 250  # Duración de las explosiones en milisegundos

# Reloj para controlar FPS
clock = pygame.time.Clock()

# --------------------------------------------------
# Ajustar tamño de las imágenes
start_img = pygame.transform.scale(start_img, (WIDTH, HEIGHT))
game_over_img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))
player_img = pygame.transform.scale(player_img, (player_width, player_height))
obstacle_img = pygame.transform.scale(
    obstacle_img, (obstacle_width, obstacle_height))
life_heart_img = pygame.transform.scale(
    life_heart_img, (life_heart_width, life_heart_height))
laser_img = pygame.transform.scale(laser_img, (100, 120))
explosion_img = pygame.transform.scale(explosion_img, (50, 50))
# --------------------------------------------------


def draw_text(text, font, color, x, y):
    """Función para dibujar texto en pantalla."""
    screen_text = font.render(
        text, True, color)  # True para que el texto se vea más nítido
    screen.blit(screen_text, [x, y])  # Dibuja el texto


def start_menu():
    """Pantalla de inicio del juego."""
    menu_running = True
    while menu_running:
        # Imagen de fondo. Se coloca de primero para no tapar el contenido
        screen.blit(start_img, (0, 0))
        # Actualiza toda la pantalla para mostrar el contenido que ha sido dibujado
        pygame.display.flip()
        for event in pygame.event.get():  # Itera sobre todos los eventos
            if event.type == pygame.QUIT:
                pygame.quit()  # Si se cierra la ventana finaliza todo
                return False
            if event.type == pygame.KEYDOWN:  # Si pulsa una tecla
                if event.key == pygame.K_s:  # Si es la 'S' sale del menú
                    menu_running = False
                elif event.key == pygame.K_q:  # Si es la 'Q' sale del juego
                    pygame.quit()
                    return False
    return True  # Solo cuando el usuario pulsa 'S'


def game_over():
    """Pantalla de Game Over."""
    screen.fill(BLACK)
    screen.blit(game_over_img, (0, 0))
    pygame.display.flip()

# --------------------------------------------------

# Función que dibuja una barra de salud
def draw_health_bar(screen, x, y, health, max_health):
    bar_width = 100
    bar_height = 10
    # Calcula el ancho del relleno según el porcentaje de salud
    fill = (health / max_health) * bar_width
    outline_rect = pygame.Rect(
        x, y, bar_width, bar_height)  # Rectángulo exterior
    fill_rect = pygame.Rect(x, y, fill, bar_height)  # Rectángulo interior
    pygame.draw.rect(screen, RED, fill_rect)
    # 2 indica el grosor del rectángulo exterior
    pygame.draw.rect(screen, WHITE, outline_rect, 2)

# Función que reinicia el juego y sus variables
def restart_game():
    pygame.mixer.music.play()
    # Sin global no puede modificar estas variables ya que Python tratará de crear nuevas variables
    global player, bullets, obstacles, explosions, score, current_health, level, max_obstacles
    # player en este momento es un pygame.Rect. No podría modificar el ancho, por ejemplo
    # Coloca al jugador en el centro horizontalmente
    player.x = WIDTH // 2 - player_width // 2
    # Coloca al jugador verticalmente en la parte inferior con un margen de 10
    player.y = HEIGHT - player_height - 10
    bullets.clear()
    obstacles.clear()
    explosions.clear()
    score = 0
    current_health = max_health
    level = 1
    max_obstacles = 4

# --------------------------------------------------

# Mostrar la pantalla de inicio
if not start_menu():  # Si la función devuelve True significa que el usuario pulsó 'S'
    running = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # .quit no es un tipo de evento. Es una función que cierra todo
            # QUIT es un evento que indica que el usuario solicitó cerrar la ventana del juego
            running = False

    keys = pygame.key.get_pressed()  # Tecla que ha sido presionada

    # Si pongo 0 tocará el borde. Sin los () se sale del mapa
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.left > 10:
        player.x -= 5  # Mueve al jugador 5 píxeles a la izquierda
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right < WIDTH - 10:
        player.x += 5
    # Si pongo 0 tocará el borde superior
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.top > 10:
        player.y -= 5
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.bottom < HEIGHT - 10:
        player.y += 5

    # Disparar balas con la tecla espacio dependiendo del tiempo que haya pasado
    if keys[pygame.K_SPACE] and pygame.time.get_ticks() - last_shot_time > shoot_delay:
        bullet = pygame.Rect(player.centerx - bullet_width // 2,
                             player.top - bullet_height // 2, bullet_width, bullet_height)
        bullets.append(bullet)
        laser_shot_sound.play()
        last_shot_time = pygame.time.get_ticks()

        # Pausar el juego correctamente
    if keys[pygame.K_p]:
        # Esperar 300 ms para evitar múltiples cambios rápidos
        pygame.time.wait(300)
        paused = not paused
        if paused:
            pygame.mixer.music.pause()  # Pausar la música cuando el juego está en pausa
        else:
            pygame.mixer.music.unpause()  # Reanudar la música cuando el juego se reanuda

    if paused:
        continue  # Salta el while si el juego está en pausa y vuelve al principio

    if game_over_screen:  # Comprueba si está en la ventana de Game Over
        pygame.mixer.music.stop()
        game_over()
        if keys[pygame.K_r]:
            game_over_screen = False
            restart_game()
        if keys[pygame.K_q]:
            running = False
        continue  # Salta el resto del ciclo

# --------------------------------------------------

    # Mover las balas
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)  # Eliminar balas que salen de la pantalla

    # Generación de obstáculos de manera random
    # Si no supera el máximo se genera un obstáculo en un punto random del eje X y en el 0 del Y
    if len(obstacles) < max_obstacles:
        obstacle = pygame.Rect(random.randint(
            0, WIDTH - obstacle_width), 0, obstacle_width, obstacle_height)
        # Velocidad aleatoria que aumenta según el nivel
        velocidad = random.randint(5, 12)
        # Se guarda cada obstáculo con su velocidad
        obstacles.append((obstacle, velocidad))

    # Mover los obstáculos
    for obstacle_info in obstacles:
        obstacle, velocidad = obstacle_info  # Desempaqueta la tupla en dos variables
        obstacle.y += velocidad # El obstáculo va hacia abajo
        if obstacle.top > HEIGHT:
            # Cuando los obstáculos pasen del alto de la ventana estos desaparecen de la lista y así se generan unos nuevos
            obstacles.remove(obstacle_info)

# --------------------------------------------------

# Aumentar nivel
    if score >= score_to_next_level:
        level += 1
        max_obstacles += 2
        shoot_delay = max(100, shoot_delay - 50)
        score_to_next_level += 50


# Detectar colisiones
    for obstacle_info in obstacles:
        obstacle, _ = obstacle_info
        if player.colliderect(obstacle):
            collision_sound.play()  # Reproducir sonido de colisión
            current_health -= 25
            obstacles.remove(obstacle_info)  # Eliminar obstáculo que choca
            if current_health <= 0:
                if score > high_score:
                    high_score = score  # Actualizar la puntuación más alta
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
                explosions.append(
                    [explosion_img, obstacle.center, pygame.time.get_ticks()])
                break


# Generar salud aleatoriamente
    if life_heart is None and random.randint(0, 1000) < 5:
        life_heart = pygame.Rect(random.randint(
            0, WIDTH - 30), random.randint(0, HEIGHT - 30), life_heart_width, life_heart_height)
        # Posicion eje X - posición eje Y - ancho - alto
    if life_heart and player.colliderect(life_heart):
        # Aumenta vida sin exceder el máximo
        current_health = min(max_health, current_health +
                                life_heart_health_increase)
        life_heart = None  # Desaparece el corazón al ser usado

# --------------------------------------------------

    # Imagen de fondo. Se coloca de primero para no tapar el contenido
    screen.blit(background_img, (0, 0))

    # Dibuja el jugador con la posición y el tamaño definido por el rectángulo player
    screen.blit(player_img, player)

    for obstacle_info in obstacles:
        obstacle, _ = obstacle_info  # Ignoramos la velocidad con guión bajo
        screen.blit(obstacle_img, obstacle) # Dibuja los obstáculos

    # Dibuja las balas
    for bullet in bullets:
        screen.blit(laser_img, bullet)

    # Dibujar el corazón
    if life_heart:
        screen.blit(life_heart_img, life_heart)
    
    for explosion in explosions[:]: # Hace una copia de la lista para evitar 
        # problemas al modificar la lista original
        img, pos, time = explosion
        if pygame.time.get_ticks() - time > explosion_duration:
            explosions.remove(explosion)
        else:
            screen.blit(img, pos)

    # Mostrar puntuación y nivel
    draw_text(f"Puntuación: {score}", font, WHITE, 10, 10)
    draw_text(f"Nivel: {level}", font, WHITE, 10, 30)
    draw_text(f"Puntuación más alta: {high_score}", font, WHITE, 10, 50)

    # Mostrar barra de vida
    draw_health_bar(screen, 10, 70, current_health, max_health)

    pygame.display.flip()  # Actualiza la pantalla
    clock.tick(60)

pygame.quit()
# El orden en el que se dibujan los elementos en la pantalla con pygame es importante,
# ya que los elementos que se dibujan después pueden superponerse a los elementos dibujados antes
