import pygame
import random
import math
from pygame import mixer

# Initializing pygame
pygame.init()

# Creating the game screen
screen = pygame.display.set_mode((800, 600))

# Setting the title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("assets/images/invasion.png")
pygame.display.set_icon(icon)

# Adding start sound
start_sound = mixer.Sound("assets/audio/starting_voice.wav")
start_sound.play()

# Adding background music
mixer.music.load("assets/audio/background_music.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Player variables
player_img = pygame.image.load("assets/images/rocket.png")
player_x = 368   # Player's X position
player_y = 500   # Player's Y position
player_x_change = 0    # Auxiliary variable for player movement

# Enemy variables
enemy_img = []
enemy_x = []   
enemy_y = []   
enemy_x_change = []    
enemy_y_change = []    
num_of_enemies = 8

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("assets/images/ufo.png"))
    enemy_x.append(random.randint(0, 736))   # Random X position for the enemy
    enemy_y.append(random.randint(50, 200))   # Random Y position for the enemy
    enemy_x_change.append(1)   # Auxiliary variable for enemy X movement
    enemy_y_change.append(50)     # Auxiliary variable for enemy Y movement

# Explosion
explosion_img = pygame.image.load("assets/images/explosion.png")

# Bullet variables
bullet_img = pygame.image.load("assets/images/bullet.png")
bullet_x = 0
bullet_y = 500
bullet_x_change = 0
bullet_y_change = 3
bullet_visible = False

# Score
score = 0
font = pygame.font.Font("assets/fonts/relish_gargler.otf", 28)
score_text_x = 10
score_text_y = 10

# Time
elapsed_time_font = pygame.font.Font("assets/fonts/relish_gargler.otf", 28)
start_time = pygame.time.get_ticks()
time_text_x = 570
time_text_y = 10

# Game Over text
game_over_font = pygame.font.Font("assets/fonts/relish_gargler.otf", 64)

# Function to display score
def show_score(x, y):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def show_elapsed_time(x, y):
    elapsed_time = pygame.time.get_ticks() - start_time
    hours = elapsed_time // 3600000
    minutes = (elapsed_time % 3600000) // 60000
    seconds = (elapsed_time % 60000) // 1000
    elapsed_time_str = f'Time: {hours:02}:{minutes:02}:{seconds:02}'
    elapsed_time_text = elapsed_time_font.render(elapsed_time_str, True, (255, 255, 255))
    screen.blit(elapsed_time_text, (x, y))

# Function to display Game Over text
def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Function to draw the player
def player(x, y):
    screen.blit(player_img, (x, y))

# Function to draw the enemy
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

# Function to fire the bullet
def fire_bullet(x, y):
    global bullet_visible # Accessing the global variable bullet_visible to modify it
    bullet_visible = True # Making the bullet visible
    screen.blit(bullet_img, (x + 16, y + 10)) 

# Function to detect collisions
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:  
        return True 
    else: 
        return False
    
def darken_screen():
    dark_surface = pygame.Surface((800, 600))  # Create a surface with the same size as the screen
    dark_surface.set_alpha(180)  # Set the alpha (transparency) to 128 (out of 255)
    dark_surface.fill((0, 0, 0))  # Fill the surface with black color
    screen.blit(dark_surface, (0, 0))  # Blit the dark surface onto the screen

# Function to create a button
def button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Define the border radius for the button (adjust as needed)
    border_radius = 10
    border_thickness = 3

    inactive_color = pygame.color.Color(0, 0, 0)
    active_color = pygame.color.Color(0, 0, 63)

    if x + w > mouse[0] > x and y + h > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))
        
    # Draw border (thicker and white)
    border_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, (255, 255, 255), border_rect, border_thickness, border_radius=border_radius)

    # Draw button text (unchanged)
    small_text = pygame.font.Font("assets/fonts/relish_gargler.otf", 20)
    text_surf = small_text.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)

# Action for restart button
def restart_game():
    global game_over, start_time, score, enemy_x, enemy_y, player_x, player_y, bullet_y, bullet_visible, game_over_sound_played
    game_over = False
    start_time = pygame.time.get_ticks()
    score = 0
    player_x = 368
    player_y = 500
    bullet_y = 500
    bullet_visible = False
    game_over_sound_played = False  # Reset the flag
    for i in range(num_of_enemies):
        enemy_x[i] = random.randint(0, 736)
        enemy_y[i] = random.randint(50, 200)
    mixer.music.play(-1)
    pygame.time.set_timer(RANDOM_SOUND_EVENT, random.randint(8000, 16000))
    game_over_loop.stop()  # Stop the game over loop sound

# Action for exit button
def exit_game():
    pygame.quit()
    quit()

# Function to play a random sound
last_sound = None  # Variable to store the last sound played
sounds = ["assets/audio/gettocover.wav", "assets/audio/letsmoveletsmove.wav", "assets/audio/laugh.wav", "assets/audio/growl.wav"]

def play_random_sound():
    global last_sound
    available_sounds = [sound for sound in sounds if sound != last_sound]
    random_sound = mixer.Sound(random.choice(available_sounds))
    random_sound.play()
    last_sound = random_sound

# Setting the timer for random sound events (8 to 16 seconds interval)
RANDOM_SOUND_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(RANDOM_SOUND_EVENT, random.randint(8000, 16000))

# Game Over sounds
game_over_voice = mixer.Sound("assets/audio/game-over-voice.wav")
game_over_loop = mixer.Sound("assets/audio/game-over-loop.wav")

# Variable to track if game over sound has been played
game_over_sound_played = False

# Game loop
running = True
game_over = False  # Flag to track game over state
game_over_time = 0  # Timer to track the game over voice sound

while running:

    # Setting the background
    screen.blit(pygame.image.load("assets/images/background.jpg"), (0, 0))

    for event in pygame.event.get():

        # Event to quit the game
        if event.type == pygame.QUIT:
            running = False

        # Event for key press (movement)
        if event.type == pygame.KEYDOWN:
            if not game_over:  # Only handle key events if the game is not over
                if event.key == pygame.K_LEFT:
                    player_x_change = -1.7
                if event.key == pygame.K_RIGHT:
                    player_x_change = 1.7
                if event.key == pygame.K_SPACE:
                    if not bullet_visible:
                        bullet_sound = mixer.Sound("assets/audio/shot.mp3")
                        bullet_sound.play()
                        bullet_x = player_x
                        fire_bullet(bullet_x, bullet_y)

        # Event for key release (stop movement)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0.0

        # Event for random sound
        if event.type == RANDOM_SOUND_EVENT:
            if not game_over:  # Only play sound if the game is not over
                play_random_sound()
                pygame.time.set_timer(RANDOM_SOUND_EVENT, random.randint(10000, 20000))

    if not game_over:
        # Updating player position (movement)
        player_x += player_x_change

        # Limiting player movement within screen
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        # Updating enemy position (movement)
        for i in range(num_of_enemies):
            # Game Over
            if enemy_y[i] > 440:
                for j in range(num_of_enemies):
                    enemy_y[j] = 2000  # Move all enemies off the screen
                game_over = True  # Set the game over flag
                mixer.music.stop()
                pygame.time.set_timer(RANDOM_SOUND_EVENT, 0)  # Stop the random sound timer
                if not game_over_sound_played:
                    game_over_voice.play()
                    game_over_time = pygame.time.get_ticks()  # Get the current time
                    game_over_sound_played = True
                break

            enemy_x[i] += enemy_x_change[i]

            # Limiting enemy movement within screen
            if enemy_x[i] <= 0:
                enemy_x_change[i] = 1.5  # Change direction to right when hitting left boundary
                enemy_y[i] += enemy_y_change[i]  # Move down when hitting left boundary
            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -1.5  # Change direction to left when hitting right boundary
                enemy_y[i] += enemy_y_change[i]  # Move down when hitting right boundary

            # Collision detection
            collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision:
                # Change enemy image to explosion image
                screen.blit(explosion_img, (enemy_x[i], enemy_y[i]))
                pygame.display.flip()  # Update screen
                explosion_sound = mixer.Sound("assets/audio/explosion.mp3")
                explosion_sound.play()
                bullet_y = 500  # Reset bullet Y position to player Y position
                bullet_visible = False  # Make bullet invisible
                score += 1  # Increase score by 1 for each collision
                enemy_x[i] = random.randint(0, 735)  # Reset enemy X position to a random value within screen
                enemy_y[i] = random.randint(50, 150)  # Reset enemy Y position to a random value within screen

            enemy(enemy_x[i], enemy_y[i], i)

        # Bullet movement
        if bullet_y <= -32:  # If bullet Y position is -32 or less, it has gone off the screen
            bullet_y = 500  # Reset bullet Y position to player Y position
            bullet_visible = False  # Make bullet invisible

        if bullet_visible:
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        # Call player and enemy functions with initial X and Y positions
        player(player_x, player_y)

        # Call show_score function
        show_score(score_text_x, score_text_y)

        # Call show_elapsed_time
        show_elapsed_time(time_text_x, time_text_y)
        
    else:
        darken_screen()  # Darken the screen when game over
        game_over_text()  # Display game over text

        # Check if the game over voice sound has finished playing
        if pygame.time.get_ticks() - game_over_time >= game_over_voice.get_length() * 2000:
            if not pygame.mixer.get_busy():
                game_over_loop.play(-1)  # Play the game over loop sound indefinitely

            # Display the buttons
            button("Restart", 150, 350, 100, 50, (0, 200, 0), (0, 255, 0), restart_game)
            button("Exit", 550, 350, 100, 50, (200, 0, 0), (255, 0, 0), exit_game)

    pygame.display.update()
