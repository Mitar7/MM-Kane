import pygame
import spritesheet
import random
from menu import *
from objects.Duck import Duck
from objects.Player import Player
from objects.Arrow import Arrow
from gameover import GameOver


class Game:
    def __init__(self):
        pygame.init()
        # Podesavanja ekrana
        pygame.display.set_caption('MM - Kane')
        icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(icon)
        self.running, self.playing = True, False  # playing je loop igrice, running je loop programa
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1166, 700
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.clock = pygame.time.Clock()  # kreiranje sata
        self.hud = pygame.image.load('images/hud1.png')
        # Font
        self.font_name = 'fonts/Inconsolata-VariableFont.ttf'

        # Boje
        self.bg = pygame.image.load('images/bg1.png')
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

        # Meniji
        self.main_menu = MainMenu(self)
        self.highscore = HighscoreMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

        # Zvukovi i muzika
        self.click_sound = pygame.mixer.Sound('sounds/click.wav')
        self.game_over_sound = pygame.mixer.Sound('sounds/gameover.wav')
        self.music = pygame.mixer.music.load('sounds/music.wav')
        # self.music = pygame.mixer.music.load('sounds/bgmusic.mp3')
        pygame.mixer.music.set_volume(0.1)  # Jacina zvuka
        pygame.mixer.music.play(-1)  # Muzika je aktivna sve vreme

        # Pozicija misa
        self.crosshair = pygame.image.load('images/crosshair.png').convert_alpha()
        self.posx, self.posy = self.DISPLAY_W / 2, self.DISPLAY_H / 2

        # Podesavanja igraca
        self.score = 0
        self.ammo = []
        self.player = Player(0, self.DISPLAY_H - 215, self)

        # Podesavanje strela
        self.arrow_img = pygame.image.load('images/arrow_resizable.png').convert_alpha()

        # Timeri
        self.gametime = 0
        self.spawntime = 0

        # Podesavanje patke
        self.ducks_passed = 0
        self.ducks_died = 0
        self.last_spawn = pygame.time.get_ticks()
        self.ducks = []

    def game_loop(self):
        # pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0),
        # (0, 0, 0, 0, 0, 0, 0, 0))  # kursor postaje nevidljiv
        pygame.mouse.set_visible(False)
        while self.playing:
            self.check_events()
            self.window.blit(self.display, (0, 0))
            self.display.blit(self.bg, (0, 0))
            self.display_hud()  # prikazivanje huda

            if self.BACK_KEY:
                self.playing = False  # Ukoliko pritisnemo Backspace igrica se zaustavlja
            if (self.player.arrows == 0 and len(self.ammo) == 0) or self.ducks_passed == 5:
                gameover = GameOver(self)
                gameover.display_menu()

            # Update informacija igraca
            self.player.blit(self.display)
            self.player.control()

            # update informacija patke
            for duck in self.ducks:
                duck.blit(self.display)
                duck.update()
                duck.move()
                if duck.left_screen():
                    self.ducks.pop(self.ducks.index(duck))
            
            # kreiranje novih pataka
            self.spawntime = pygame.time.get_ticks()
            min = 60000
            if self.spawntime > min * 3:
                if self.spawntime - self.last_spawn > 1000:
                    print('Prosala su 3 minuta igra se ubrzava!')
                    self.last_spawn = self.spawntime
                    duck = Duck(-150, random.randrange(120, self.player.y - 30), self)
                    duck.vel += 2
                    self.ducks.append(duck)
            if self.spawntime > min * 2:
                if self.spawntime - self.last_spawn > 1250:
                    print('Prosala su 2 minuta igra se ubrzava!')
                    self.last_spawn = self.spawntime
                    duck = Duck(-150, random.randrange(120, self.player.y - 30), self)
                    duck.vel += 1.5
                    self.ducks.append(duck)
            if self.spawntime > min:  # nakon minuta na svaku 1.5 sekundu igra spawnuje patku
                if self.spawntime - self.last_spawn > 1500:
                    print('Prosao je minut igra se ubrzava!')
                    self.last_spawn = self.spawntime
                    duck = Duck(-150, random.randrange(120, self.player.y - 30), self)
                    duck.vel += 1
                    self.ducks.append(duck)
            else:
                if self.spawntime - self.last_spawn > 2000:  # u pocetku igre patke se spawnuju na 2 sekunde
                    self.last_spawn = self.spawntime
                    duck = Duck(-150, random.randrange(120, self.player.y - 30), self)
                    self.ducks.append(duck)

            for arrow in self.ammo:
                for duck in self.ducks:
                    if arrow.collided(duck.duck_rect):
                        duck.bird_death.play()
                        for _ in range(duck.dead_animation_steps - 1):
                            duck.update_dead()
                            duck.blit_dead(self.display)
                            duck.dead_frame += 1
                        duck.dead = True
                        if self.player.arrows < 8:
                            self.player.arrows += 1
                        self.ducks.pop(self.ducks.index(duck))  # pogodjena patka nestaje
                        self.ammo.pop(self.ammo.index(arrow))   # strela kojom smo pogodili nestaje
                if self.DISPLAY_W > arrow.x > 0 and arrow.y > 0:
                    arrow.move()
                else:
                    self.ammo.pop(self.ammo.index(arrow))

            pygame.display.update()
            self.reset_keys()  # Pritisnuti tasteri se resetuju na kraju loopa
            self.clock.tick(60)  # FPS igre je 60

    # provera pritisnutih tastera
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Izlaz iz igre
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.posy < self.player.y:
                    if self.player.arrows > 0 and len(self.ammo) < 1:
                        self.ammo.append(Arrow(self, round(self.player.x + self.player.width // 2), round(self.player.y + self.player.height // 2)))
                        self.player.left = False
                        self.player.right = False
                        self.player.shooting = True
            if event.type == pygame.MOUSEMOTION:
                self.posx, self.posy = pygame.mouse.get_pos()

    # resetuje pritisnute tastere
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    # iscritava test
    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def display_hud(self):
        self.gametime = pygame.time.get_ticks()  # vreme u igri
        self.display.blit(self.hud, (320, 0))
        self.draw_text(f'Score: {self.score}', 22, self.DISPLAY_W - 75, 25, self.WHITE)
        self.draw_text('Arrows left: ', 25, self.DISPLAY_W - 300, 25, self.WHITE)
        for x in range(self.player.arrows):
            self.display.blit(self.arrow_img, (self.DISPLAY_W - 145 - 10 * x, 5))
        self.draw_text(f'Birds passed: {self.ducks_passed}', 25, self.DISPLAY_W - 500, 25, self.WHITE)
        self.draw_text(f'Birds killed: {self.ducks_died}', 25, self.DISPLAY_W - 725, 25, self.WHITE)
        if self.gametime < 60000:
            self.draw_text(f'Time: {round(self.gametime / 1000,2)}s', 25, self.DISPLAY_W - 100, self.DISPLAY_H - 30, self.WHITE)
        else:
            self.draw_text(f'Time: {round((self.gametime / 1000) / 60, 2)} min', 25, self.DISPLAY_W - 100, self.DISPLAY_H - 30, self.WHITE)
        self.display.blit(self.crosshair, (self.posx - 15, self.posy - 15))

    def game_over(self):
        self.draw_text('Game over', 48, self.DISPLAY_W / 2, self.DISPLAY_H / 2 + 40, self.BLACK)