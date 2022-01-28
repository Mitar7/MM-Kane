import pygame
import time
from sys import exit
from operator import itemgetter


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('->', 15, self.cursor_rect.x, self.cursor_rect.y, self.game.BLACK)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.highscorex, self.highscorey = self.mid_w, self.mid_h + 60
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 90
        self.quitx, self.quity = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.game.bg, (0, 0))
            self.game.draw_text('MM KANE', 48, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 40, self.game.BLACK)
            self.game.draw_text("Start Game", 30, self.startx, self.starty, self.game.BLACK)
            self.game.draw_text("Highscore", 30, self.highscorex, self.highscorey, self.game.BLACK)
            self.game.draw_text("Credits", 30, self.creditsx, self.creditsy, self.game.BLACK)
            self.game.draw_text("Quit", 30, self.quitx, self.quity, self.game.BLACK)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.highscorex + self.offset, self.highscorey)
                self.state = 'HighScore'
            elif self.state == 'HighScore':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'HighScore':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.highscorex + self.offset, self.highscorey)
                self.state = 'HighScore'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.click_sound.play()
                self.game.playing = True
            elif self.state == 'HighScore':
                self.game.click_sound.play()
                self.game.curr_menu = self.game.highscore
            elif self.state == 'Credits':
                self.game.click_sound.play()
                self.game.curr_menu = self.game.credits
            elif self.state == 'Quit':
                self.game.click_sound.play()
                time.sleep(0.5)
                pygame.quit()
                exit()
            self.run_display = False


class HighscoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        highscore = {}
        self.run_display = True

        with open('highscores.txt', 'r') as f:
            text = f.readlines()

        for line in text:
            date, score = line.split('-')
            highscore[date] = int(score)
        res = dict(sorted(highscore.items(), key=itemgetter(1), reverse=True)[:15])  # prikazuje TOP 15 rezultata

        while self.run_display:
            offset_y = 10
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.click_sound.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.blit(self.game.bg, (0, 0))
            self.game.draw_text('HighScores', 48, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 300, self.game.BLACK)

            for key, value in res.items():
                self.game.draw_text(f'Date:({key}) Score: {value}', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 250 + offset_y, self.game.BLACK)
                offset_y += 30

            self.draw_cursor()
            self.blit_screen()


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.click_sound.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.blit(self.game.bg, (0, 0))
            self.game.draw_text('Credits', 48, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50, self.game.BLACK)
            self.game.draw_text('Mitar Milovanovic', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2, self.game.BLACK)
            self.game.draw_text('Resources from:', 48, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 70, self.game.BLACK)
            self.game.draw_text('https://opengameart.org', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 130,self.game.BLACK)
            self.game.draw_text('https://www.spriters-resource.com', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 160,self.game.BLACK)
            self.blit_screen()
