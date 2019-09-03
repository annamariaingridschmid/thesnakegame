import pygame
import random
import os

# initialize
pygame.init()
pygame.mixer.pre_init()
pygame.mixer.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (137, 207, 240)

# puts the window of the game in the center of the PC screen
os.environ['SDL_VIDEO_CENTERED'] = '0'

# defines the size of one cell of the total grid
width = 35
height = width

grid_size = 20 # number of rows and columns
margin = 1  # margin between the different cells of the grid


max_x_screen_size = grid_size*(width+margin)
max_y_screen_size = grid_size*(height+margin)


size = [max_x_screen_size, max_y_screen_size ]
screen = pygame.display.set_mode(size)


# inital settings
snake = [1]
snake_moves = []
score = 0

# load picture
apple = pygame.image.load("mushroom.png")
apple = pygame.transform.scale(apple, (width, height))
apple_rect = apple.get_rect()

font=pygame.font.SysFont("Verdana",30)

# start playing the background music
pygame.mixer.music.load("03 Chibi Ninja.mp3") #music player
pygame.mixer.music.set_volume(10)
pygame.mixer.music.play()

def show_snake(x_snake,y_snake, snake, snake_moves):
    color_snake_head = RED
    for i in range(len(snake)):
        if snake[i] == 1:
            pygame.draw.rect(screen,color_snake_head, pygame.Rect(snake_moves[i][0], snake_moves[i][1], width, height))
        
def show_eyes(pos_eyes_1, pos_eyes_2):
    color_eyes = BLACK
    radius = 4
    pygame.draw.circle(screen,color_eyes, pos_eyes_1, radius)
    pygame.draw.circle(screen,color_eyes, pos_eyes_2, radius)   

def show_tongue(x_tongue, y_tongue, width, height):
    color_tongue = GREEN
    pygame.draw.rect(screen,color_tongue, pygame.Rect(x_tongue, y_tongue, width, height))      

def record_snake_position(x_snake, y_snake):
    snake_moves.append((x_snake,y_snake))
    return snake_moves

def show_apple(x_apple,y_apple):
    apple_rect.x = x_apple
    apple_rect.y = y_apple
    color_apple = BLACK
    # pygame.draw.rect(screen,color_apple, pygame.Rect(x_apple, y_apple, width, height))

def show_grid():
    for row in range(grid_size):
        for column in range(grid_size):
            color = BLACK
            pygame.draw.rect(screen,color,[(margin + width) * column + margin,(margin + height) * row + margin,width,height])

# if the postion of the apple and the snake incl. body are the same, then change the x and y positoin of the apple
def create_random_position_apple(snake,snake_moves,grid_size, width, height, margin):
    x_apple_new = margin + (random.randint(0,grid_size-1)*(width+margin))
    y_apple_new = margin + (random.randint(0,grid_size-1)*(height+margin))
    for i in range(len(snake)):
       if snake[i] == 1:
            if snake_moves==[]:
               pass
            else:
                if (x_apple_new, y_apple_new) in snake_moves:
                    x_apple_new = margin + (random.randint(0,grid_size-1)*(width+margin))
                    y_apple_new = margin + (random.randint(0,grid_size-1)*(height+margin))
            return x_apple_new, y_apple_new


def eat_apple_and_define_new(x_head, y_head, x_apple, y_apple, score, grid_size, width, height, margin, snake,snake_moves):
    if (x_head == x_apple) and (y_head == y_apple):
        snake.append(1)
        score +=1
        x_apple, y_apple = create_random_position_apple(snake, snake_moves, grid_size, width, height, margin)
        snake, snake_moves = cut_lenght_of_list(snake, snake_moves)
    else:
        snake.insert(0,0)
    return x_apple, y_apple, score, snake, snake_moves

def cut_lenght_of_list(snake, snake_moves):
    snake_new = []
    snake_moves_new = []
    for i in range(len(snake)):
       if snake[i] == 1:
            snake_new.append(snake[i])
            snake_moves_new.append(snake_moves[i])
    return snake_new, snake_moves_new

# define start position for the snake --> center 
rect_xp = int(margin + (grid_size/2*(width+margin)))
rect_yp = int(margin + (grid_size/2*(height+margin)))

# define by how many pixel the snake shall move up, down, left or right when hiting the button (one cell)
rect_change_xp = width+margin
rect_change_yp = width+margin

# defines the size of the snake's tongue
tong_width = 5
tong_height = 15

# defines the position of the snake's tongue depended from the position of the snake
x_tongue = rect_xp + 15
y_tongue = rect_yp + 25

# defines the position of the eyes depended from the position of the snake
pos_eyes_1 = (rect_xp + 10, rect_yp + 10)
pos_eyes_2 = (rect_xp - 10 + width, rect_yp + 10)

# speed_x = 0
# speed_y = -VSPEED

# define the initial  position of the 1st apple
x_apple_random, y_apple_random = create_random_position_apple(snake, snake_moves, grid_size, width, height, margin)

# record inital snake position in the histroy log
snake_moves.append((rect_xp, rect_yp))

# records initial timer (start ticker)
start_ticks=pygame.time.get_ticks()

done = False

while done == False:
    for event in pygame.event.get():    # check for any events
        if event.type == pygame.QUIT:
            done = True

        # Kill game if snake leaves boundries
        if rect_xp>max_x_screen_size or rect_xp<0:
            done = True
        if rect_yp>max_y_screen_size or rect_yp<0:
            done = True
        
        # Kill game if snake hits its body
        if (rect_xp, rect_yp) in snake_moves:
            idx = snake_moves.index((rect_xp, rect_yp))
            if (snake[idx]) == 1 and (idx < len(snake)-1):
                done = True
                            
        # act upon key events and sets new x and y positions for snake, tongue, eyes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rect_xp=-rect_change_xp+rect_xp
                x_tongue = rect_xp - 5
                y_tongue = rect_yp + 15
                tong_width = 15
                tong_height = 5
                pos_eyes_1 = (rect_xp - 10 + width, rect_yp - 10 + height)
                pos_eyes_2 = (rect_xp - 10 + width, rect_yp + 10)
            if event.key == pygame.K_RIGHT:
                rect_xp=rect_change_xp+rect_xp
                x_tongue = rect_xp + 25
                y_tongue = rect_yp + 15
                tong_width = 15
                tong_height = 5
                pos_eyes_1 = (rect_xp + 10, rect_yp + 10)
                pos_eyes_2 = (rect_xp + 10, rect_yp - 10 + height)
            if event.key == pygame.K_UP:
                rect_yp=-rect_change_yp+rect_yp
                x_tongue = rect_xp + 15
                y_tongue = rect_yp - 5
                tong_width = 5
                tong_height = 15
                pos_eyes_1 = (rect_xp + 10, rect_yp - 10 + height)
                pos_eyes_2 = (rect_xp - 10 + width, rect_yp - 10 + height)
            if event.key == pygame.K_DOWN:
                rect_yp=rect_change_yp+rect_yp
                x_tongue = rect_xp + 15
                y_tongue = rect_yp + 25
                tong_width = 5
                tong_height = 15
                pos_eyes_1 = (rect_xp + 10, rect_yp + 10)
                pos_eyes_2 = (rect_xp - 10 + width, rect_yp + 10)


            record_snake_position(rect_xp, rect_yp) # adds the latest position to a list (--> snake_move)
            x_apple_random, y_apple_random, score, snake, snake_moves = eat_apple_and_define_new(rect_xp, rect_yp,x_apple_random, y_apple_random, score,grid_size, width, height, margin, snake, snake_moves)
            # print(f"Apple new position = x : {x_apple_random} and y : {y_apple_random}")
            # print(snake)
            # print(snake_moves)


    screen.fill(pygame.Color('WHITE'))
    show_grid()
    show_snake(rect_xp,rect_yp, snake, snake_moves)
    show_tongue(x_tongue, y_tongue, tong_width, tong_height)
    show_eyes(pos_eyes_1, pos_eyes_2)
    show_apple(x_apple_random, y_apple_random) # renders new position of apple
    screen.blit(apple, apple_rect) # prints/renders the apple on new position

    #show timer & score
    time_display=font.render(f"Time: {int((pygame.time.get_ticks()-start_ticks)/1000)} s",1,WHITE)
    screen.blit(time_display,(510,0))  #prints the timer on the screen
    score_display=font.render(f"Score: {score}",1,WHITE)
    screen.blit(score_display,(510,36))  #prints the timer on the screen


    pygame.display.update()
