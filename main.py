# Make a flappy bird using pygame

# I don't have any images, use the pygame.draw.circle to draw
# the player and the pygame.draw.rectangle to draw the pipe

# I've got an image for the player, make the image named
# "texugo" be blit to the screen, exactly like the circle

# Now the collides function of the Pipe class
# is messed up, could you make it work?

# There's no radius anymore just the image size

# When the player dies, I want to show his
# score for 5 seconds and then end the game

import pygame
import random

# Inicia o pygame
pygame.init()

# Janela do jogo
width = 288
height = 512
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

#Imagem do texugo dentro do jogo
texugo_img = pygame.image.load("texugo.jpg")


# Classe do jogador
class Bird:
    def __init__(self):
        self.x = 50
        self.y = 200
        self.gravity = 0.25
        self.velocity = 0
        self.jump_height = -5
        self.radius = 20
        self.size = texugo_img.get_size()

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = self.jump_height

    def draw(self):
        window.blit(texugo_img, (self.x, self.y))


# Classe dos canos
class Pipe:
    def __init__(self):
        self.x = width
        self.pipe_gap = 150
        self.pipe_width = 70
        self.top_height = random.randint(100, 300)
        self.bottom_height = height - self.pipe_gap - self.top_height
        self.passed = False

    def update(self):
        self.x -= 2 * (score // 5 + 3)/3

    def offscreen(self):
        return self.x < -self.pipe_width

    def collides(self, bird):
        if bird.y < self.top_height or bird.y + 40 > height - self.bottom_height:
            if bird.x + 40 > self.x and bird.x < self.x + self.pipe_width:
                return True
        return False

    def draw(self):
        pygame.draw.rect(window, GREEN, (self.x, 0, self.pipe_width, self.top_height))
        pygame.draw.rect(window, GREEN, (self.x, height - self.bottom_height, self.pipe_width, self.bottom_height))

# Variáveis do jogo, como o jogador, os canos, os pontos e a fonte
bird = Bird()
pipes = [Pipe()]
score = 0
font = pygame.font.Font(None, 40)

# Loop do jogo, como o tempo, se a janela está rodando, se deu gameover e o tempo de gameover
clock = pygame.time.Clock()
running = True
game_over = False
game_over_time = None
while running:
    # Checar se o jogador quer sair do jogo, além de checar se ele quer pular
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_SPACE:
                bird.jump()
            elif game_over and event.key == pygame.K_ESCAPE:
                running = False

    # Se o jogo estiver rodando:
    if not game_over:
        # Atualizar o jogador
        bird.update()
        for pipe in pipes:
            # Atualizar os canos
            pipe.update()

            # Checar a colisão do jogador com o cano
            if pipe.collides(bird):
                game_over = True
                game_over_time = pygame.time.get_ticks()

            # Checar se o jogador passou do cano
            if not pipe.passed and pipe.x + pipe.pipe_width < bird.x:
                pipe.passed = True
                score += 1
                pipes.append(Pipe())

            # Checar se o cano está fora da tela para deletá-lo
            if pipe.offscreen():
                pipes.remove(pipe)

        # Checar a colisão vertical para dar gameover
        if bird.y < 0 or bird.y > height:
            game_over = True
            game_over_time = pygame.time.get_ticks()

    # Desenhar o jogador e os canos na tela
    window.fill(WHITE)
    for pipe in pipes:
        pipe.draw()
    bird.draw()

    # Mostrar a pontuação
    if not game_over:
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        window.blit(score_text, (10, 10))
    else:
        window.fill((0, 0, 0))
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        window.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height()))
        window.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))

        # Wait for 5 seconds and end the game
        if game_over_time is not None and pygame.time.get_ticks() - game_over_time >= 3000:
            running = False

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()