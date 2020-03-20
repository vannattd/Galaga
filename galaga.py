#!/usr/bin/env python3
# Group members: Logan Jaglowski and Dylan Vannatter
# version 1.0 3-20-2020
# CIS 343 01
# Prof. Woodring
# Files: galaga.py
# Purpose: Creating Galaga using Python 3 w/ pygame
# Game: Win by destroying all the enemy ships. Lose if you run out of lives. Shoot power up to increase speed.
# Controls: Move with left and right arrow keys and shoot with space bar or 'a'.

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
        # Overlay to keep track of our lives and score
        self.render('Score: 0        Lives: 5')

    def render(self, text):
        self.text = self.font.render(text, True, (0, 0, 0))
        self.image.blit(self.text, self.rect)

    def draw(self, screen):
        screen.blit(self.text, (0, 0))

    def update(self, score, lives):
        self.render('Score: ' + str(score) + '        Lives: ' + str(lives))


class Speed(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Loading image in for speed power up
        self.image = pygame.image.load('assets/speed.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Loading in player image and position
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 530

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Loading in enemy image
        self.image = pygame.image.load('assets/enemy.png')
        self.rect = self.image.get_rect()
        self.vector = [5, 0]
        self.iterator = 0

    def update(self, enemies):
        # Making enemies move and stay within boundaries
        for enemy in enemies:
            if enemy.rect.x >= 745:
                self.vector[0] = -5

        if self.rect.x <= 0:
            self.vector[0] = 5
            for enemy in enemies:
                enemy.vector[0] = self.vector[0]

        if self.rect.x >= 750:
            self.vector[0] = -5
            for enemy in enemies:
                enemy.vector[0] = self.vector[0]

        self.rect.x += self.vector[0]


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Loading in laser image
        self.image = pygame.image.load('assets/laser.png')
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 560
        self.vector = [0, 0]
        self.thud_sound = pygame.mixer.Sound('assets/thud.wav')

    def update(self, game, enemies, player, totalpowerup, power, existing):
        if self.rect.y > 600 | self.rect.y < 0:
            self.kill()
        hitObject = pygame.sprite.spritecollideany(self, enemies)
        # How to react when laser hits an enemy
        if hitObject:
            if self.vector[1] < 0:
                self.thud_sound.play()
                hitObject.kill()
                self.kill()
                game.score += 1
        # How to react if laser hits player
        if pygame.sprite.collide_rect(self, player):
            if self.vector[1] > 0:
                self.kill()
                game.lives -= 1
        hitPowerUp = pygame.sprite.spritecollideany(self, totalpowerup)
        # How to react when laser hits power up
        if hitPowerUp:
            if self.vector[1] < 0:
                game.powerUp = 1
                game.existingPower = 0
                self.kill()
                hitPowerUp.kill()

        self.rect.y += self.vector[1]


class Game:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(50)
        pygame.mixer.music.load('assets/loop.wav')
        pygame.mixer.music.play(-1)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        self.projectiles = pygame.sprite.Group()
        self.player = Player()
        self.new_life_event = pygame.event.Event(pygame.USEREVENT + 1)
        self.enemies = pygame.sprite.Group()
        self.overlay = Overlay()
        self.speed = Speed()
        self.totalPowerUps = pygame.sprite.Group()
        self.screen.fill((255, 205, 255))
        self.ready = True
        self.score = 0
        self.lives = 5
        self.powerUp = 0
        self.existingPower = 0
        self.powerUpCounter = 0
        # Spawning enemies
        for i in range(0, 4):
            for j in range(0, 6):
                enemy = Enemy()
                enemy.rect.x = j * 100 + 100
                enemy.rect.y = i * 100 + 20
                self.enemies.add(enemy)

    def run(self):
        self.done = False
        while not self.done:
            self.screen.fill((255, 205, 255))
            # How to react when lives are gone or enemies are gone
            for event in pygame.event.get():
                if self.lives <= 0 or self.score == 24:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    # Key press responses
                    if event.key == pygame.K_a:
                        laser = Laser()
                        laser.rect.x = self.player.rect.x + 43
                        laser.rect.y = self.player.rect.y
                        laser.vector = [0, -2]
                        self.projectiles.add(laser)
                    if event.key == pygame.K_SPACE:
                        laser = Laser()
                        laser.rect.x = self.player.rect.x + 43
                        laser.rect.y = self.player.rect.y
                        laser.vector = [0, -2]
                        self.projectiles.add(laser)
                    if event.key == pygame.K_LEFT:
                        if self.powerUp == 0:
                            self.player.rect.x -= 5
                        else:
                            self.player.rect.x -= 10
                        if self.player.rect.x <= 0:
                            self.player.rect.x = 0
                    if event.key == pygame.K_RIGHT:
                        if self.powerUp == 0:
                            self.player.rect.x += 5
                        else:
                            self.player.rect.x += 10
                        if self.player.rect.x >= 750:
                            self.player.rect.x = 750
            # Enemies shooting lasers
            for enemy in self.enemies:
                if random.randint(0, 1000) == 1:
                    laser = Laser()
                    laser.image = pygame.image.load('assets/elaser.png')
                    laser.rect.x = enemy.rect.x + 45
                    laser.rect.y = enemy.rect.y + 10
                    laser.vector = [0, 2]
                    self.projectiles.add(laser)
            # Randomly spawning power up
            if random.randint(0, 100) == 1:
                if self.powerUp == 0:
                    if self.existingPower == 0:
                        speed = Speed()
                        speed.rect.y = 400
                        speed.rect.x = random.randint(0, 700)
                        self.existingPower = 1
                        self.totalPowerUps.add(speed)

            # Keeping track of power ups
            if self.powerUpCounter == 400:
                self.powerUp = 0
                self.powerUpCounter = 0

            if self.powerUp == 1:
                self.powerUpCounter += 1

            # Updating the screen
            self.projectiles.update(self, self.enemies, self.player, self.totalPowerUps, self.powerUp,
                                    self.existingPower)
            self.overlay.update(self.score, self.lives)
            self.enemies.update(self.enemies)
            self.projectiles.draw(self.screen)
            self.player.draw(self.screen)
            self.enemies.draw(self.screen)
            self.overlay.draw(self.screen)
            self.totalPowerUps.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
