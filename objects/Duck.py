import pygame
import spritesheet


class Duck:
    def __init__(self, x, y, game):
        self.game = game
        self.x = x
        self.y = y
        self.vel = 4
        self.dead = False
        # Slika patke i pravougao
        self.duck = pygame.image.load('images/Duck/player1-sprite.png').convert_alpha()
        self.duck_sheet = spritesheet.SpriteSheet(self.duck)
        self.duck_rect = self.duck.get_rect()
        # Promenjive za animaciju
        self.animation_list = []
        self.animation_steps = 4
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 150
        self.frame = 0

        # Slika mrtve patke
        self.duck_dead = pygame.image.load('images/Duck/duck_crash.png').convert_alpha()
        self.duck_dead_sheet = spritesheet.SpriteSheet(self.duck_dead)
        self.duck_dead_rect = self.duck_dead.get_rect()
        # Promenjive za animaciju
        self.dead_animation_list = []
        self.dead_animation_steps = 13
        self.dead_last_update = pygame.time.get_ticks()
        self.dead_animation_cooldown = 150
        self.dead_frame = 0

        # Zvukovi patke
        self.bird_death = pygame.mixer.Sound('sounds/bird_death.mp3')
        self.bird_escape = pygame.mixer.Sound('sounds/birdescape.wav')

        for x in range(self.animation_steps):
            self.animation_list.append(self.duck_sheet.get_image(x, 127, 127, 0.8, (0, 0, 0)))

        for x in range(self.dead_animation_steps):
            self.dead_animation_list.append(self.duck_dead_sheet.get_image(x, 127, 127, 0.8, (0, 0, 0)))

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0

    def update_dead(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.dead_last_update >= self.dead_animation_cooldown:
            self.dead_frame += 1
            self.dead_last_update = current_time
            if self.dead_frame >= len(self.dead_animation_list):
                self.dead_frame = 0

    def move(self):
        if not self.dead:
            self.x += self.vel

    def left_screen(self):
        if self.x >= self.game.DISPLAY_W:
            self.bird_escape.play()
            self.game.ducks_passed += 1
            return True

    def blit(self, display):
        if not self.dead:
            self.duck_rect = self.animation_list[self.frame].get_rect(center=(self.x, self.y))
            display.blit(self.animation_list[self.frame], self.duck_rect)

    def blit_dead(self, display):
        self.duck_dead_rect = self.dead_animation_list[self.dead_frame].get_rect(center=(self.x, self.y))
        display.blit(self.dead_animation_list[self.dead_frame], self.duck_dead_rect)
