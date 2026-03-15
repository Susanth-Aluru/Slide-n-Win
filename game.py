import pygame
from sys import exit
import random


def populate(array, numbers):
    i = 0
    for row in array:
        for index in range(len(row)):
            row[index] = numbers[i]
            i = i+1


numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
target = [[1, 2, 3, 4],[5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

# print(numbers)
board = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
def reload():
    random.shuffle(numbers)
    populate(board, numbers)

reload()
#functions
def get_0_pos():
    found = False
    index_x_0 = 0
    index_y_0 = 0
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 0:
                index_x_0 = x
                index_y_0 = y
                found = True
                break
        if found == True:
            return (index_x_0, index_y_0)

# variables required for game
gameState = 0
# x = 0
# y = 0
# starting stuff
pygame.init()

class EndScreen(pygame.sprite.Sprite):
    def __init__(self,pos_y,pos_x):
        super().__init__()
        self.sprites = [pygame.image.load("graphics/youWon-"+str(i)+".png") for i in range(0,198)]
        self.current_sprite = 0
        self.elapsed = 600
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
    def update(self):
        self.elapsed = pygame.time.get_ticks() - self.elapsed
        if self.elapsed > 600:
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[self.current_sprite] 
        else:
            self.elapsed = 600   


movingSprites = pygame.sprite.Group()
endscreen = EndScreen(0,0)
movingSprites.add(endscreen)
icon = pygame.image.load('graphics/icon.png')
screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption("Slide 'n' Win")
clock = pygame.time.Clock()
pygame.display.set_icon(icon)

# images initializing
background = pygame.image.load('graphics/background.png').convert_alpha()
background_2 = pygame.image.load('graphics/icon(2).png')
game_over = pygame.image.load('graphics/youWon-0.png')


# blocks intitializing
blocks = {
    1: pygame.image.load('graphics/blocks/block_1.png'),
    2: pygame.image.load('graphics/blocks/block_2.png'),
    3: pygame.image.load('graphics/blocks/block_3.png'),
    4: pygame.image.load('graphics/blocks/block_4.png'),
    5: pygame.image.load('graphics/blocks/block_5.png'),
    6: pygame.image.load('graphics/blocks/block_6.png'),
    7: pygame.image.load('graphics/blocks/block_7.png'),
    8: pygame.image.load('graphics/blocks/block_8.png'),
    9: pygame.image.load('graphics/blocks/block_9.png'),
    10: pygame.image.load('graphics/blocks/block_10.png'),
    11: pygame.image.load('graphics/blocks/block_11.png'),
    12: pygame.image.load('graphics/blocks/block_12.png'),
    13: pygame.image.load('graphics/blocks/block_13.png'),
    14: pygame.image.load('graphics/blocks/block_14.png'),
    15: pygame.image.load('graphics/blocks/block_15.png')
}

while True:
    zero_pos = get_0_pos()
    back_display = screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gameState == 1:
            index_x = zero_pos[0]
            index_y = zero_pos[1]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    next_item_pos = index_x +1
                    if next_item_pos < len(board[index_y]):
                        board[index_y][index_x] = board[index_y][next_item_pos]
                        board[index_y][next_item_pos] = 0 
                elif event.key == pygame.K_RIGHT:
                    last_item_pos = index_x - 1
                    if last_item_pos >= 0:
                        board[index_y][index_x] = board[index_y][last_item_pos]
                        board[index_y][last_item_pos] = 0
                elif event.key == pygame.K_DOWN:
                    below_item_pos = index_y -1
                    if below_item_pos >=0:
                        board[index_y][index_x] = board[below_item_pos][index_x]
                        board[below_item_pos][index_x] = 0
                elif event.key == pygame.K_UP:
                    below_item_pos = index_y + 1
                    if below_item_pos < len(board):
                        board[index_y][index_x] = board[below_item_pos][index_x]
                        board[below_item_pos][index_x] = 0  
                elif event.key == pygame.K_r:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL: # cheat key to refresh the game
                        reload()
                elif event.key == pygame.K_e:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL: #cheat key to end the game
                        board = target.copy()

            if board == target:
                gameState = 2       
    if gameState == 0:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:gameState = 1
        screen.blit(background_2,(0,0))
    if gameState == 1:
        back_display
        for x in range(len(board)):
            for y in range(len(board[x])):
                    co_x = x * 120
                    co_y = y * 120
                    if board[y][x] != 0:
                        screen.blit(blocks[board[y][x]], (co_x, co_y))  
    if gameState == 2:
        movingSprites.draw(screen)
        movingSprites.update()                                      
    pygame.display.update()
    clock.tick(60)