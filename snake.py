from statistics import mode
import sys, pygame
import math
from board import Board
import consts
from layout import Layout


pygame.init()

layout = Layout((400,500),10,10)

screen = pygame.display.set_mode(layout.screen_size)
board_surface = pygame.Surface((layout.board_rect[2], layout.board_rect[3]))
header_surface = pygame.Surface((layout.header_rect[2], layout.header_rect[3]))

black = 0, 0, 0
white = 255, 255, 255
line_color = 128, 128, 128
empty_color = (0, 0, 0)
food_color = (200, 0, 0)
body_color = (0, 0, 200)

title_font = pygame.font.SysFont(None, 48)
score_font = pygame.font.SysFont(None, 30)

clock = pygame.time.Clock()
FPS = 4

board = Board(layout.num_of_cols, layout.num_of_rows)

food_img = pygame.image.load('apple.png')
food_img.convert()
food_rect = food_img.get_rect()
scale =  layout.get_scale_factor(food_rect.width)
food_img = pygame.transform.rotozoom(food_img, 0, scale)
food_rect = food_img.get_rect()

snake_head_img = pygame.image.load('snake_head.png')
snake_head_img.convert()
snake_rect = snake_head_img.get_rect()
scale =  layout.get_scale_factor(snake_rect.width)
snake_head_img = pygame.transform.rotozoom(snake_head_img, 0, scale)
snake_rect = snake_head_img.get_rect()


def get_rotation_based_dir(img, dir):
    '''Rotate the given image based on the direction. The image base points down'''
    if dir[0] == 1:
        return pygame.transform.rotozoom(img, 90, 1)
    if dir[0] == -1:
        return pygame.transform.rotozoom(img, -90, 1)
    if dir[1] == 1:
        return pygame.transform.rotozoom(img, 0, 1)
    if dir[1] == -1:
        return pygame.transform.rotozoom(img, 180, 1)

def draw_board(dest):
    '''Draw the board structure'''
    for line in range(0, layout.board_rect[3] + layout.cell_height, layout.cell_height):
        pygame.draw.line(dest, line_color, (0, line), (layout.board_rect[2], line))
    for col in range(0, layout.board_rect[2] + layout.cell_width, layout.cell_width):
        pygame.draw.line(dest, line_color, (col, 0), (col, layout.board_rect[3]))

    
def draw_head(dest, rect, dir):
    '''Draw the head image'''
    img = get_rotation_based_dir(snake_head_img, dir)
    dest.blit(img, rect)


def draw_body(dest, rect):
    '''Draw the body'''
    pygame.draw.rect(dest, body_color, (rect[0] + rect[2] // 4, rect[1] + rect[3] // 4, rect[2] // 2, rect[3] // 2))


def draw_food(dest, rect):
    '''Draw the food'''
    dest.blit(food_img, rect)


def draw_cell(dest, dir):
    '''Run on each cell and call the correct drawing function'''
    for pos in board.get_snake_cells_pos():
        rect = layout.get_cell_rect(pos[0], pos[1], False)
        if (pos[2]):
            draw_head(dest, rect, dir)
        else:
            draw_body(dest, rect)
    pos = board.get_food()
    rect = layout.get_cell_rect(pos[0], pos[1], False)
    draw_food(dest, rect)


def draw_title(dest, font, rect, title):
    img = font.render(title, True, (255, 255, 255))
    img_rect = img.get_rect()
    img_rect.center = (rect[2] // 2, rect[3] // 2)
    dest.blit(img, img_rect )


def draw_score(dest, font, rect, score):
    img = font.render(f'Score: {score}', True, (0, 0, 255))
    dest.blit(img, rect)


def draw_header(dest, score):
    dest.fill(black)
    draw_title(dest, title_font, (0, 0, layout.header_rect[2], layout.header_rect[3] * 0.75), 'Snake')
    draw_score(dest, score_font, (10, layout.header_rect[3] * 0.75, layout.header_rect[2]- 20, layout.header_rect[3] * 0.25), score)


def check_board(x, y):
    res = board.check_pos(x, y)
    if res == consts.RESULT_INVALID_POS:
        sys.exit()
    if res == consts.RESULT_FOOD:
        board.generate_food()
        return 1
    return 0

def main_loop():
    head = [1,0]
    pos = [0,0]
    val = 1
    screen.fill(black)
    draw_header(header_surface, val)
    screen.blit(header_surface,(0,0))
    board.generate_food()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.__dict__['key'] == pygame.K_UP:
                    head = [0,-1]
                if event.__dict__['key'] == pygame.K_DOWN:
                    head = [0,1]
                if event.__dict__['key'] == pygame.K_LEFT:
                    head = [-1,0]
                if event.__dict__['key'] == pygame.K_RIGHT:
                    head = [1,0]    
       
        
        board_surface.fill(black)
        
        pos[0] = pos[0] + head[0]
        pos[1] = pos[1] + head[1]
        res = check_board(pos[0],pos[1])
        if res == 1:
            val += 1
            draw_header(header_surface, val)
            screen.blit(header_surface,(0,0))
        board.set_head(pos[0],pos[1], val)
        board.update()
        draw_cell(board_surface, head)
        draw_board(board_surface)
        screen.blit(board_surface, (0,100))
        pygame.display.flip()
        res = clock.tick(FPS)


main_loop()

