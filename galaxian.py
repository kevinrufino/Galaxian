#!/usr/bin/env python3

import pygame
import random
import sys

from pygame import image


class Overlay(pygame.sprite.Sprite):
    def __init__(self):
        # Equivalent statements:
        # pygame.sprite.Sprite.__init__(self)
        super(pygame.sprite.Sprite, self).__init__()
        self.image = pygame.Surface((800, 20))
        # self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.render('Score: 0        Lives: 5')
        
    def render(self, text):
        self.text = self.font.render(text, True, (0, 0, 0))
        self.image.blit(self.text, self.rect)
    
    def draw(self, screen):
        screen.blit(self.text, (0, 0))

        # This brings image to forground
        # background_image = pygame.image.load("assets/649694main_pia15417-43_full.jpg").convert()
        # screen.blit(background_image, [0, 0])

    def update(self, score, lives):
        self.render('Score: ' + str(score) + '        Lives: ' + str(lives))

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # self.image = pygame.Surface((40, 60))
        # self.image.fill((0, 0, 0))

        self.image = image.load('assets/ship-sprit.PNG').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = 375
        self.rect.y = 530

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50, 50))
        # self.color = ( random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) )
        # self.image.fill(self.color)

        self.image = image.load('assets/coronavirus.PNG').convert_alpha()
        self.rect = self.image.get_rect()

    # Fix this to update move every over one every frame
    def update(self):
        if self.rect.x < 750:
            self.rect.x += 1
        else:
            self.rect.x -= 750

class Shot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((10, 25))
        # pygame.draw.circle(self.image, (0, 0, 0), (5, 5), 5)
        self.image = image.load('assets/blue-lazer.PNG').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = -10
        self.rect.y = 530
        self.vector = [ 0, 0 ]
        self.thud_sound = pygame.mixer.Sound('assets/thud.wav')

    def update(self, game, blocks, paddle):
        # This changes the angle after collision with edge
        if self.rect.x < 1 or self.rect.x > 795:
            self.vector[0] *= -1
        if self.rect.y < 0:
            # This removes "ball" once reached top
            game.shots.remove(self)

            # This would have the ball bounce back from the top
            # self.vector[1] *= -1
            # pygame.event.post(game.new_life_event)
        # This removes "ball" if too far from left or right from paddle
        # if self.rect.y > paddle.rect.y + 20:
        #     game.shots.remove(self)
            # pygame.event.post(game.new_life_event)

        # Collision with blocks?
        hitObject = pygame.sprite.spritecollideany(self, blocks)
        if hitObject:
            self.thud_sound.play()
            # self.vector[0] = -1.1
            # self.vector[1] *= -1.1
            hitObject.kill()
            game.score += 1
            game.shots.remove(self)

        # Collision with paddle?
        # if pygame.sprite.collide_rect(self, paddle):
        #     self.vector[1] *= -1.2
        #     self.vector[0] += random.random()
        #     if random.randint(0,1) == 1:
        #         self.vector[0] *= -1

        self.rect.x += self.vector[0]
        # speed of shot
        self.rect.y += self.vector[1] - 1

class EnemyShot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((10, 25))
        # pygame.draw.circle(self.image, (0, 0, 0), (5, 5), 5)
        self.image = image.load('assets/red-lazer.PNG').convert_alpha()
        self.rect = self.image.get_rect()
        # change these to select random enemies coordinates
        self.rect.x = -10
        self.rect.y = 0
        self.vector = [ 0, 0 ]
        self.thud_sound = pygame.mixer.Sound('assets/thud.wav')

    def update(self, game, blocks, paddle):
        self.rect.y = game.paddle.rect.y - 100
        # This changes the angle after collision with edge
        if self.rect.x < 1 or self.rect.x > 795:
            self.vector[0] *= -1
        if self.rect.y > 600:
            # This removes "ball" once reached bottom
            game.enemyShots.remove(self)

            # This would have the ball bounce back from the top
            # self.vector[1] *= -1
            # pygame.event.post(game.new_life_event)
        # This removes "ball" if too far from left or right from paddle
        # if self.rect.y > paddle.rect.y + 20:
        #     game.enemyShots.remove(self)
            # pygame.event.post(game.new_life_event)

        # Collision with blocks?
        hitObject = pygame.sprite.spritecollideany(self, paddle)
        if hitObject:
            self.thud_sound.play()
            # self.vector[0] = -1.1
            # self.vector[1] *= -1.1
            hitObject.kill()
            game.score += 1
            game.enemyShots.remove(self)

        self.rect.x += self.vector[0]
        # speed of shot
        self.rect.y += self.vector[1] - 1

class Game:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(50)
        pygame.mixer.music.load('assets/loop.wav')
        pygame.mixer.music.play(-1)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        self.shots = pygame.sprite.Group()
        self.shots.add(Shot())
        self.enemyShots = pygame.sprite.Group()
        self.enemyShots.add(EnemyShot())
        self.paddle = Paddle()
        self.new_life_event = pygame.event.Event(pygame.USEREVENT + 1)
        self.blocks = pygame.sprite.Group()
        self.overlay = Overlay()
        self.screen.fill((255, 255, 255))
        self.image = pygame.image.load('assets/space.jpg')
        self.ready = True
        self.score = 0
        self.lives = 5

        # This adds blocks on the screen
        for i in range(0, 4):
            for j in range(0, 12):
                block = Block()
                block.rect.x = j * 60 + 10
                block.rect.y = i * 60 + 10
                self.blocks.add(block)

    def run(self):
        self.done = False

        while not self.done:
            self.screen.blit(self.image, (0, 0))

            for event in pygame.event.get():
                shoot = random.randrange(100)
                if shoot > 50:
                    enemyShot = EnemyShot()
                    enemyShot.vector = [0, 1]
                    enemyShot.rect.y = self.paddle.rect.y
                    self.enemyShots.add(enemyShot)

                # This is what happends when we lose a life
                if event.type == self.new_life_event.type:
                    self.lives -= 1
                    if self.lives > 0:
                        self.ready = True
                        # ball = Ball()
                        # # ball.rect.x = self.paddle.rect.x + 25
                        # self.balls.add(ball)
                    else:
                        pygame.quit()
                        sys.exit(0)
                # Happens when you quit?
                if event.type == pygame.QUIT:
                    self.done = True
                # Happens when you press a key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.lives += 1
                        shot = Shot()
                        shot.vector = [ 0, -1 ]
                        self.shots.add(Shot)
                    if event.key == pygame.K_SPACE and self.ready:
                        # self.balls.sprites()[0].vector = [ 0, -1 ]
                        # self.balls.sprites()[0].rect.x = self.paddle.rect.x + 25

                        # self.ready = False
                        shot = Shot()
                        shot.vector = [0, -1]
                        shot.rect.x = self.paddle.rect.x + 25
                        self.shots.add(shot)


                    if event.key == pygame.K_LEFT:
                        self.paddle.rect.x -= 5
                        # Change this so that it updates where the ball will spawn
                        # self.balls.sprites()[0].rect.x -= 5
                        if self.paddle.rect.x <= 0:
                            self.paddle.rect.x = 0
                    if event.key == pygame.K_RIGHT:
                        self.paddle.rect.x += 5
                        # Change this so that it updates where the ball will spawn
                        # self.balls.sprites()[0].rect.x += 5
                        if self.paddle.rect.x >= 750:
                            self.paddle.rect.x = 750
                # if self.ready:
                #     self.balls.sprites()[0].rect.x = self.paddle.rect.x + 25
                # for i in range(0,400):
                # if self.blocks.sprites()[0].rect.x < 750:
                #     self.blocks.sprites()[0].rect.x += 1
            
            self.shots.update(self, self.blocks, self.paddle)
            self.enemyShots.update(self, self.paddle, self.blocks)
            self.overlay.update(self.score, self.lives)
            self.blocks.update()
            self.shots.draw(self.screen)
            self.enemyShots.draw(self.screen)
            self.paddle.draw(self.screen)
            self.blocks.draw(self.screen)
            self.overlay.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

class Intro(pygame.sprite.Sprite):
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
