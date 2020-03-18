#!/usr/bin/env python3

import pygame
import random
import sys


class Overlay(pygame.sprite.Sprite):
    def __init__(self):
        # Equivalent statements:
        # pygame.sprite.Sprite.__init__(self)
        super(pygame.sprite.Sprite, self).__init__()
        self.image = pygame.image.load('assets/background.png')
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.render('Score: 0        Lives: 5')

    def render(self, text):
        self.text = self.font.render(text, True, (0, 0, 0))
        self.image.blit(self.text, self.rect)

    def draw(self, screen):
        screen.blit(self.text, (0, 0))

    def update(self, score, lives):
        self.render('Score: ' + str(score) + '        Lives: ' + str(lives))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 530

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/enemy.png')
        self.rect = self.image.get_rect()
        self.vector = [5, 0]

    def update(self, blocks):
        if self.rect.x <= 0:
            self.vector[0] = 5
        if self.rect.x >= 740:
            self.vector[0] = -5
        hitObject = pygame.sprite.spritecollideany(self, blocks)
        if hitObject:
            for block in blocks:
                block.vector[0] = self.vector[0]
        self.rect.x += self.vector[0]


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/laser.png')
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 560
        self.vector = [0, 0]
        self.thud_sound = pygame.mixer.Sound('assets/thud.wav')

    def update(self, game, blocks, paddle):
        if self.rect.y > 600:
            self.kill()
        hitObject = pygame.sprite.spritecollideany(self, blocks)
        if hitObject:
            self.thud_sound.play()
            hitObject.kill()
            self.kill()
            game.score += 1
        if pygame.sprite.collide_rect(self, paddle) & self.vector[1] < 0:
            self.kill()
            game.lives -= 1
        self.rect.y += self.vector[1]


class Game:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(50)
        pygame.mixer.music.load('assets/loop.wav')
        pygame.mixer.music.play(-1)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        self.balls = pygame.sprite.Group()
        self.paddle = Player()
        self.new_life_event = pygame.event.Event(pygame.USEREVENT + 1)
        self.blocks = pygame.sprite.Group()
        self.overlay = Overlay()
        self.screen.fill((255, 205, 255))
        self.ready = True
        self.score = 0
        self.lives = 5
        for i in range(0, 4):
            for j in range(0, 6):
                block = Enemy()
                block.rect.x = j * 100 + 100
                block.rect.y = i * 100 + 20
                self.blocks.add(block)

    def run(self):
        self.done = False
        while not self.done:
            self.screen.fill((255, 205, 255))
            for event in pygame.event.get():
                if event.type == self.new_life_event.type:
                    # self.lives -= 1
                    if self.lives > 0:
                        ball = Laser()
                        ball.rect.x = self.paddle.rect.x
                        self.balls.add(ball)
                        self.ready = True
                    else:
                        pygame.quit()
                        sys.exit(0)
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        ball = Laser()
                        ball.rect.x = self.paddle.rect.x + 43
                        ball.rect.y = self.paddle.rect.y
                        ball.vector = [0, -2]
                        self.balls.add(ball)
                    if event.key == pygame.K_SPACE:
                        ball = Laser()
                        ball.rect.x = self.paddle.rect.x + 43
                        ball.rect.y = self.paddle.rect.y
                        ball.vector = [0, -2]
                    if event.key == pygame.K_LEFT:
                        self.paddle.rect.x -= 5
                        if self.paddle.rect.x <= 0:
                            self.paddle.rect.x = 0
                    if event.key == pygame.K_RIGHT:
                        self.paddle.rect.x += 5
                        if self.paddle.rect.x >= 750:
                            self.paddle.rect.x = 750
                # if self.ready:
                # self.balls.sprites()[0].rect.x = self.paddle.rect.x + 25
            self.balls.update(self, self.blocks, self.paddle)
            self.overlay.update(self.score, self.lives)
            self.blocks.update(self.blocks)
            self.balls.draw(self.screen)
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
        self.text = self.font.render('Breakout!', True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.image.blit(self.text, self.rect)

    def draw(self, screen):
        screen.blit(self.text, (0, 0))


if __name__ == "__main__":
    game = Game()
    game.run()
