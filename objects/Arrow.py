import pygame
import math


class Arrow(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        # Kordinate i brzina strele
        self.x = x
        self.y = y
        self.vel = 7

        # Izracunavanje ugla i pucanje strele
        self.targetx = self.game.posx
        self.targety = self.game.posy
        self.angle = math.atan2(self.targety - self.y, self.targetx - self.x)
        self.angle_degrees = math.degrees(self.angle)
        self.dx = math.cos(self.angle) * self.vel
        self.dy = math.sin(self.angle) * self.vel
        # print('Angle in degrees:', -self.angle_degrees)

        # Slika i pravougaonik
        self.arrow = pygame.image.load('images/arrow_resizable.png').convert_alpha()
        self.arrow_rect = self.arrow.get_rect()
        self.arrow_rect.center = (self.x, self.y)

    # Iscrtavnje strele
    def draw(self, display):
        # Strela se prvobitno rotira u zavisnosti od ugla koji se racuna prilikom klika misa
        arrow_img = pygame.transform.rotate(self.arrow, -self.angle_degrees - 90)
        display.blit(arrow_img, (self.arrow_rect.x, self.arrow_rect.y))  # iscrtavanje slike

    # Provera sudara 2 pravougla
    def collided(self, other_rect):
        if self.arrow_rect.colliderect(other_rect):
            self.game.ducks_died += 1
            self.game.score += 5
            return True  # vraca True kako bi if petlja prosla

    # kretanje strele
    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.arrow_rect.x = int(self.x)
        self.arrow_rect.y = int(self.y)

