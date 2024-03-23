import pygame

class Player:
    def __init__(self, x, y,color, win):
        self.x = x
        self.y = y
        self.color = color
        self.win = win

    def draw(self):
        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= 1
        if keys[pygame.K_RIGHT]:
            self.x += 1
        if keys[pygame.K_UP]:
            self.y -= 1
        if keys[pygame.K_DOWN]:
            self.y += 1