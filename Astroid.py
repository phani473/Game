import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
original_screen_size = (800, 600)
screen = pygame.display.set_mode(original_screen_size, pygame.RESIZABLE)  # Use RESIZABLE mode
fullscreen = False  # Initially not in fullscreen
pygame.display.set_caption("Space Ship Saviour")

# Load asteroid and spaceship images
asteroid_image = pygame.image.load("astroid1.png")
asteroid_image = pygame.transform.scale(asteroid_image, (50, 50))  # Resize the image to fit the game
spaceship_image = pygame.image.load("Spaceship.png")
spaceship_image = pygame.transform.scale(spaceship_image, (60, 60))  # Resize the image to fit the game

# Background image
background_image = pygame.image.load("space.jpeg")
background_image = pygame.transform.scale(background_image, original_screen_size)

# Obstacle attributes
obstacles = []
obstacle_speed_limit = 10

# Timing variables
last_obstacle_spawn_time = pygame.time.get_ticks()
last_speed_increase_time = pygame.time.get_ticks()
start_time = pygame.time.get_ticks()
collision_time = 0

# Score
score = 0

# Function to reset the game state
def reset_game():
    global obstacles, last_obstacle_spawn_time, last_speed_increase_time, start_time, collision_time, score
    obstacles = []
    last_obstacle_spawn_time = pygame.time.get_ticks()
    last_speed_increase_time = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()
    collision_time = 0
    score = 0

# Function to display "GAME OVER" and score
def show_game_over():
    screen.fill((0, 0, 0))  # Fill the screen with black
    font_game_over = pygame.font.Font(None, 72)
    game_over_text = font_game_over.render("GAME OVER", True, (255, 255, 0))  # Yellow color
    # Center game over text
    screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, screen.get_height() // 2 - game_over_text.get_height() // 2))
    font_score = pygame.font.Font(None, 36)
    score_text = font_score.render("Score: " + str(score), True, (255, 255, 0))  # Yellow color
    # Center score text
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, screen.get_height() // 2 + 50))
    font_restart = pygame.font.Font(None, 36)
    restart_text = font_restart.render("Press R to Restart", True, (255, 255, 0))  # Yellow color
    # Center restart text
    screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, screen.get_height() // 2 + 100))
    font_exit = pygame.font.Font(None, 36)
    exit_text = font_exit.render("Press ESC to Exit", True, (255, 255, 0))  # Yellow color
    # Center exit text
    screen.blit(exit_text, (screen.get_width() // 2 - exit_text.get_width() // 2, screen.get_height() // 2 + 150))
    pygame.display.flip()

# Class for a clickable button
class Button:
    def __init__(self, x, y, width, height, text, font_size=36, base_color=(0, 150, 255), hover_color=(0, 120, 215), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.base_color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, pos, event):
        return self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN

# Function to display start screen
def show_start_screen():
    screen.fill((0, 0, 0))  # Fill the screen with black
    start_button = Button(screen.get_width() // 2 - 100, screen.get_height() // 2 - 30, 200, 60, "Start")
    start_button.draw(screen)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                handle_exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.is_clicked(mouse_pos, event):
                    waiting = False
            start_button.update(pygame.mouse.get_pos())

# Function to handle exit event
def handle_exit():
    pygame.quit()
    sys.exit()

# Function to toggle fullscreen
def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        pygame.display.set_mode(original_screen_size, pygame.FULLSCREEN)
    else:
        pygame.display.set_mode(original_screen_size, pygame.RESIZABLE)

# Main game loop
running = True
game_over = False
player_x = 50
player_y = original_screen_size[1] // 2
player_speed = 10
player_size = 20

# Display start screen
show_start_screen()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            handle_exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                handle_exit()
            elif event.key == pygame.K_r and game_over:
                reset_game()
                game_over = False
            elif event.key == pygame.K_F11:
                toggle_fullscreen()  # Toggle fullscreen when F11 key is pressed
        elif event.type == pygame.VIDEORESIZE:
            original_screen_size = event.size
            screen = pygame.display.set_mode(original_screen_size, pygame.RESIZABLE)
            # Adjust game elements based on the new screen size
            background_image = pygame.transform.scale(background_image, original_screen_size)
            player_x = player_x * original_screen_size[0] / screen.get_width()
            player_y = player_y * original_screen_size[1] / screen.get_height()
            for obstacle in obstacles:
                obstacle[0] = obstacle[0] * original_screen_size[0] / screen.get_width()
                obstacle[1] = obstacle[1] * original_screen_size[1] / screen.get_height()

    if not game_over:
        # Get key states and update player position
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += player_speed

        # Boundary checks for player movement
        player_x = max(0, min(player_x, original_screen_size[0] - player_size))
        player_y = max(0, min(player_y, original_screen_size[1] - player_size))

        # Collision detection between player and obstacles
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3])
            if player_rect.colliderect(obstacle_rect):
                print("GAME OVER")
                game_over = True

        # Collision detection between obstacles
        if pygame.time.get_ticks() - collision_time > 100:
            for i in range(len(obstacles)):
                for j in range(i + 1, len(obstacles)):
                    obstacle1 = obstacles[i]
                    obstacle2 = obstacles[j]
                    obstacle1_rect = pygame.Rect(obstacle1[0], obstacle1[1], obstacle1[2], obstacle1[3])
                    obstacle2_rect = pygame.Rect(obstacle2[0], obstacle2[1], obstacle2[2], obstacle2[3])
                    if obstacle1_rect.colliderect(obstacle2_rect):
                        # Swap velocities of colliding obstacles
                        obstacle1[4], obstacle1[5] = -obstacle1[4], -obstacle1[5]
                        obstacle2[4], obstacle2[5] = -obstacle2[4], -obstacle2[5]
                        collision_time = pygame.time.get_ticks()

        # Move the obstacles
        for obstacle in obstacles:
            obstacle[0] += obstacle[4]
            obstacle[1] += obstacle[5]
            # Limit speed to obstacle_speed_limit
            obstacle[4] = min(max(obstacle[4], -obstacle_speed_limit), obstacle_speed_limit)
            obstacle[5] = min(max(obstacle[5], -obstacle_speed_limit), obstacle_speed_limit)

        # Check if the obstacles hit the screen edges
        for obstacle in obstacles:
            if obstacle[0] <= 0 or obstacle[0] >= original_screen_size[0] - obstacle[2]:
                obstacle[4] *= -1
            if obstacle[1] <= 0 or obstacle[1] >= original_screen_size[1] - obstacle[3]:
                obstacle[5] *= -1

        # Spawn an extra obstacle every 30 seconds
        current_time = pygame.time.get_ticks()
        if current_time - last_obstacle_spawn_time > 5000:  # 30000 milliseconds = 30 seconds
            last_obstacle_spawn_time = current_time
            obstacle_y = random.randint(0, original_screen_size[1] - 50)
            obstacle = [original_screen_size[0] - 100, obstacle_y, 50, 50, random.randint(-3, 3), random.randint(-3, 3)]
            obstacles.append(obstacle)

        # Increase obstacle speed every 30 seconds
        if current_time - last_speed_increase_time > 30000:  # 30000 milliseconds = 30 seconds
            last_speed_increase_time = current_time
            for obstacle in obstacles:
                obstacle[4] *= 1.1  # Increase speed along x-axis
                obstacle[5] *= 1.1  # Increase speed along y-axis

        # Calculate score based on time played
        elapsed_time = (current_time - start_time) / 1000  # Convert milliseconds to seconds
        score = int(elapsed_time)

        # Draw everything
        screen.blit(background_image, (0, 0))  # Draw background image
        screen.blit(spaceship_image, (player_x, player_y))  # Draw spaceship image
        for obstacle in obstacles:
            screen.blit(asteroid_image, (obstacle[0], obstacle[1]))  # Draw asteroid images
        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))  # White color
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

        # Control the frame rate
        pygame.time.Clock().tick(60)
    else:
        show_game_over()

# Reset screen size when exiting the game
pygame.display.set_mode(original_screen_size)
# Quit Pygame
pygame.quit()
sys.exit()
