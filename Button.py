import pygame
from setting import *

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, index, total_buttons, gap, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+2, self.height+2), 0)
            
        # Get the size of the window
        window_width, window_height = pygame.display.get_surface().get_size()
        
        # Calculate the coordinates of the center of the screen
        center_x = window_width / 2
        center_y = window_height / 2
        
        # Calculate the top left corner of the button so that the button is centered horizontally
        self.x = center_x - self.width / 2
        
        # Adjust the y coordinate based on the index of the button
        self.y = center_y + (index - total_buttons / 2) * (self.height + gap)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
    
class ImageButton():
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y        
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT
        
    def draw(self, win):          
        #Draw button on the screen
        win.blit(self.image, (self.rect.x, self.rect.y))
        
    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
        
        