import pygame


class Player:
    def __init__(self, x, y, game):
        # Podesavanja igraca
        self.game = game
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.vel = 6
        self.arrows = 8

        # Provera aktivnosti igraca
        self.left = False
        self.right = False
        self.shooting = False

        # Promenljive za pracenje indexa iscrtavanja
        self.walkCount = 0
        self.IdleCount = 0
        self.shootCount = 0

        # Slike igraca u razlicitim aktivnostima
        self.walkingRight = [pygame.image.load(r"images\Archer\Run_Idle\run_idle_000.png").convert_alpha(),
                             pygame.image.load(r"images\Archer\Run_Idle\run_idle_001.png").convert_alpha(),
                             pygame.image.load(r"images\Archer\Run_Idle\run_idle_002.png").convert_alpha(),
                             pygame.image.load(r"images\Archer\Run_Idle\run_idle_003.png").convert_alpha(),
                             pygame.image.load(r"images\Archer\Run_Idle\run_idle_004.png").convert_alpha(),
                             pygame.image.load(r"images\Archer\Run_Idle\run_idle_005.png").convert_alpha(),
                             pygame.image.load(r"images\Archer\Run_Idle\run_idle_006.png").convert_alpha(),
                             pygame.image.load(r"images\Archer\Run_Idle\run_idle_007.png").convert_alpha(),
                             pygame.image.load(r"images\Archer\Run_Idle\run_idle_008.png").convert_alpha()]
        self.walkingLeft = [pygame.image.load(r"images\Archer\Run_Idle\run_idle_Left_000.png").convert_alpha(),
                            pygame.image.load(r"images\Archer\Run_Idle\run_idle_Left_001.png").convert_alpha(),
                            pygame.image.load(r"images\Archer\Run_Idle\run_idle_Left_002.png").convert_alpha(),
                            pygame.image.load(r"images\Archer\Run_Idle\run_idle_Left_003.png").convert_alpha(),
                            pygame.image.load(r"images\Archer\Run_Idle\run_idle_Left_004.png").convert_alpha(),
                            pygame.image.load(r"images\Archer\Run_Idle\run_idle_Left_005.png").convert_alpha(),
                            pygame.image.load(r"images\Archer\Run_Idle\run_idle_Left_006.png").convert_alpha(),
                            pygame.image.load(r"images\Archer\Run_Idle\run_idle_Left_007.png").convert_alpha(),
                            pygame.image.load(r"images\Archer\Run_Idle\run_idle_Left_008.png").convert_alpha()]
        self.Idle = [pygame.image.load(r"images\Archer\Idle\idle_test_000.png").convert_alpha(),
                     pygame.image.load(r"images\Archer\Idle\idle_test_001.png").convert_alpha(),
                     pygame.image.load(r"images\Archer\Idle\idle_test_002.png").convert_alpha(),
                     pygame.image.load(r"images\Archer\Idle\idle_test_003.png").convert_alpha(),
                     pygame.image.load(r"images\Archer\Idle\idle_test_004.png").convert_alpha(),
                     pygame.image.load(r"images\Archer\Idle\idle_test_005.png").convert_alpha(),
                     pygame.image.load(r"images\Archer\Idle\idle_test_006.png").convert_alpha(),
                     pygame.image.load(r"images\Archer\Idle\idle_test_007.png").convert_alpha(),
                     pygame.image.load(r"images\Archer\Idle\idle_test_008.png").convert_alpha()]
        self.Shoot = [pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_000.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_001.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_002.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_003.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_004.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_005.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_006.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_007.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_008.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_009.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_010.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_011.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_012.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_013.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_014.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_015.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_016.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_017.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_018.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_019.png").convert_alpha(),
                      pygame.image.load(r"images\Archer\Shoot_Stand\shoot_stand_020.png").convert_alpha()]

        # Zvuk luka
        self.bow_sound = pygame.mixer.Sound('sounds/bow_sound.wav')

    # provera kontrole igraca
    def control(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > self.vel and not self.shooting:
            self.x -= self.vel
            self.left = True
            self.right = False
            self.shooting = False
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < self.game.DISPLAY_W - self.width - self.vel and not self.shooting:
            self.x += self.vel
            self.left = False
            self.right = True
            self.shooting = False
        else:
            self.right = False
            self.left = False
            self.shooting = False
            self.walkCount = 0

    # Iscrtvava igraca zavisnosti od aktivnosti
    def blit(self, display):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.shootCount + 1 >= 63:
            self.shootCount = 0
        if self.IdleCount + 1 >= 27:
            self.IdleCount = 0

        if self.left:
            display.blit(self.walkingLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            display.blit(self.walkingRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.shooting:
            self.bow_sound.play()
            self.arrows -= 1
            display.blit(self.Shoot[self.shootCount // 3], (self.x, self.y))
            self.shootCount += 1
        else:
            display.blit(self.Idle[self.IdleCount // 3], (self.x, self.y))
            self.IdleCount += 1

        for arrow in self.game.ammo:
            arrow.draw(self.game.display)
