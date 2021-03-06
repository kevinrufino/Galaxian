#!/usr/bin/env python3

import pygame
import random
import sys
from pygame import *

# I recieved helped from multiple stack overflows, but forgot to add any of the links
# pygame.org was also a huge help for understanding pygame modules


class Overlay(pygame.sprite.Sprite):
    # constructor
    def __init__(self, *groups):
        # inheriting from parent
        super(pygame.sprite.Sprite, self).__init__()
        super().__init__(*groups)
        # sets score style
        self.image = pygame.Surface((800, 20))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.render('Score: 0        Lives: 5')
        
    def render(self, text):
        self.text = self.font.render(text, True, (255, 255, 255))
        self.image.blit(self.text, self.rect)
    
    def draw(self, screen):
        screen.blit(self.text, (0, 0))

    # updates lives and score every game
    def update(self, score, lives):
        self.render('Score: ' + str(score) + '        Lives: ' + str(lives))

class Ship(pygame.sprite.Sprite):
    # constructor
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.load('assets/ship-sprit.PNG').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 275
        self.rect.y = 700

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Enemies(pygame.sprite.Sprite):
    # constructor
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # move counter for setting enemy path
        self.right_moves = 180
        self.left_moves = 0
        # frame count for explosion
        self.explosion_timer = 2
        # "enemies spotted! it's the coronavirus!"
        self.image = image.load('assets/coronavirus.PNG').convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, ship, enemyShots):
        # sets path for enemies
        if self.right_moves >= 0:
            self.rect.x += 1
            self.right_moves -= 1
            if self.right_moves == 0:
                self.left_moves = 180
        elif self.left_moves >= 0:
            self.rect.x -= 1
            self.left_moves -= 1
            if self.left_moves == 0:
                self.right_moves = 180

        # randomly shoots
        shoot = random.randrange(1000)
        if shoot == 98:
            enemyShot = EnemyShot()
            enemyShots.add(enemyShot)
            enemyShot.rect.y = self.rect.y + 50
            enemyShot.rect.x = self.rect.x + 25

class Shot(pygame.sprite.Sprite):
    # constructor
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # sets our lasers to blue
        self.image = image.load('assets/blue-lazer.PNG').convert_alpha()
        self.rect = self.image.get_rect()
        # positions lasers in front of ship
        self.rect.x = -10
        self.rect.y = 700
        # not actual laser sounds
        self.thud_sound = pygame.mixer.Sound('assets/thud.wav')

    def update(self, game, enemies, ship):
        # This removes the shot once reached edges of map
        if self.rect.y > 800 or self.rect.y < 0 or self.rect.x < 0 or self.rect.x > 595:
            game.shots.remove(self)

        # Collision with enemies
        hitObject = pygame.sprite.spritecollideany(self, enemies)
        if hitObject:
            self.thud_sound.play()
            game.score += 1
            game.shots.remove(self)
            game.phase_two(hitObject)

        # speed of shot
        self.rect.y -= 2

class EnemyShot(pygame.sprite.Sprite):
    # constructor
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # "OH NO! the coronavirus shoots red lasers!"
        self.image = image.load('assets/red-lazer.PNG').convert_alpha()
        self.rect = self.image.get_rect()
        self.thud_sound = pygame.mixer.Sound('assets/thud.wav')

    def update(self, game, enemies, ship):
        # This removes enemyShots once reached edges
        if self.rect.y > 800 or self.rect.y < 0 or self.rect.x < 0 or self.rect.x > 595:
            game.enemyShots.remove(self)

        hitObject = pygame.sprite.spritecollideany(self, ship)
        if (type(hitObject) == ship):
            self.thud_sound.play()
            hitObject.kill()
            game.lives -= 1
            game.enemyShots.remove(self)

        # Collision with ship
        if pygame.sprite.collide_rect(self, enemies):
            self.thud_sound.play()
            game.enemyShots.remove(self)
            pygame.event.post(game.new_life_event)

        # speed of shot
        self.rect.y += 1

class Game:
    # constructor for game loop
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(50)
        # pygame.mixer.music.load('assets/loop.wav')
        # pygame.mixer.music.play(-1)
        self.clock = pygame.time.Clock()
        self.start_ticks = 0
        self.seconds = 0
        # screen size vertical
        self.screen = pygame.display.set_mode((600, 800))
        # lasers
        self.shots = pygame.sprite.Group()
        self.shots.add(Shot())
        self.enemyShots = pygame.sprite.Group()
        self.enemyShots.add(EnemyShot())
        # protag's ship
        self.ship = Ship()
        # restart when you die
        self.new_life_event = pygame.event.Event(pygame.USEREVENT + 1)
        # explosion for 1 second
        self.explosion_event = pygame.USEREVENT + 2
        self.e = pygame.USEREVENT + 3
        # enemy group initialization
        self.enemies = pygame.sprite.Group()
        # overlay
        self.overlay = Overlay()
        self.screen.fill((255, 255, 255))
        # sets the battle in space
        self.image = pygame.image.load('assets/space.jpg')
        self.ready = True
        self.score = 0
        self.lives = 5

        # This adds enemies on the screen
        for i in range(0, 5):
            for j in range(0, 7):
                enemy = Enemies()
                enemy.rect.x = j * 60 + 10
                enemy.rect.y = i * 60 + 10
                self.enemies.add(enemy)

    # this gives the enemies invunerability after they've first been shot
    # "hard_mode: Activited!"
    def phase_two(self, enemies):
        enemies.image = image.load('assets/coronavirus2.PNG').convert_alpha()
        # starter tick
        self.start_ticks = pygame.time.get_ticks()
        if self.seconds > 1:
            enemies.kill()

    def run(self):
        self.done = False
        while not self.done:
            #this is the background
            self.screen.blit(self.image, (0, 0))
            #timer
            self.seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000

            for event in pygame.event.get():
                # This is what happends when we lose a life
                if event.type == self.new_life_event.type:
                    self.lives -= 1
                    if self.lives > 0:
                        self.ship.rect.x = 275
                        self.ship.rect.y = 700
                        self.ready = True

                    else:
                        pygame.quit()
                        sys.exit(0)

                # Happens when you quit?
                if event.type == pygame.QUIT:
                    self.done = True

                # Happens when you press a key
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE and self.ready:
                        shot = Shot()
                        shot.rect.x = self.ship.rect.x + 25
                        self.shots.add(shot)

                    if event.key == pygame.K_LEFT:
                        self.ship.rect.x -= 5
                        if self.ship.rect.x <= 0:
                            self.ship.rect.x = 0

                    if event.key == pygame.K_RIGHT:
                        self.ship.rect.x += 5
                        if self.ship.rect.x >= 550:
                            self.ship.rect.x = 550

            # call everything to update every frame
            self.shots.update(self, self.enemies, self.ship)
            self.enemyShots.update(self, self.ship, self.enemies)
            self.overlay.update(self.score, self.lives)
            self.enemies.update(self.ship, self.enemyShots)
            # draw everything every frame
            self.shots.draw(self.screen)
            self.enemyShots.draw(self.screen)
            self.ship.draw(self.screen)
            self.enemies.draw(self.screen)
            self.overlay.draw(self.screen)
            # load next frame
            pygame.display.flip()
            # 60 fps
            self.clock.tick(60)

class Intro(pygame.sprite.Sprite):
    # constructor
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((800, 120))
        self.font = pygame.font.Font('freesansbold.ttf', 96)
        self.text = self.font.render('Galaxian!', True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.image.blit(self.text, self.rect)

    def draw(self, screen):
        screen.blit(self.text, (0, 0))


if __name__ == "__main__":
    game = Game()
    game.run()
