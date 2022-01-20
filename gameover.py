import pygame
import time
import datetime


class GameOver:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

        self.state = "Main Menu"
        self.restartx, self.restarty = self.mid_w, self.mid_h + 30
        self.exitx, self.exity = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.restartx + self.offset, self.restarty)

    def draw_cursor(self):
        self.game.draw_text('->', 15, self.cursor_rect.x, self.cursor_rect.y, self.game.BLACK)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.game.bg, (0, 0))
            self.game.draw_text('Gameover', 72, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 60, self.game.BLACK)
            self.game.draw_text(f'SCORE: {self.game.score}', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20, self.game.BLACK)
            self.game.draw_text("Main Menu", 30, self.restartx, self.restarty, self.game.BLACK)
            self.game.draw_text("Exit", 30, self.exitx, self.exity, self.game.BLACK)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Main Menu':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.restartx + self.offset, self.restarty)
                self.state = 'Main Menu'
        elif self.game.UP_KEY:
            if self.state == 'Main Menu':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.restartx + self.offset, self.restarty)
                self.state = 'Main Menu'

    def write_highscore(self):
        x = datetime.datetime.now()
        with open('highscores.txt', 'a') as f:
            f.write(f'{x.strftime("%c")} - {self.game.score}\n')

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Main Menu':
                self.game.click_sound.play()
                self.write_highscore()
                exec(open("main.py").read())  # pokrece main ponovo
            elif self.state == 'Exit':
                self.game.click_sound.play()
                self.write_highscore()
                time.sleep(1)
                pygame.quit()
                exit()
            self.run_display = False