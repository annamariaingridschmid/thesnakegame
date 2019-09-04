import pygame
import random
import os
import numpy as np

# initialize
pygame.init()
pygame.mixer.pre_init()
pygame.mixer.init()


def init_variables():
    """Initialize all the required variables for the game to start."""
    
    # Game speed
    speed = 200
    
    # We add a ticking event for the snake to move automatically
    MOVEEVENT = pygame.USEREVENT+1 
    t = speed
    pygame.time.set_timer(MOVEEVENT, t)

    # We define basic colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (140, 255, 0)
    RED = (255, 0, 0)
    BLUE = (137, 207, 240)

    # puts the window of the game in the center of the screen
    os.environ['SDL_VIDEO_CENTERED'] = '0'

    # defines the size of one cell
    width = 35
    height = width

    # number of rows and columns
    grid_size = 20

    # margin between the different cells of the grid 
    margin = 1  

    # Compute the size of the grid
    max_x_screen_size = grid_size*(width+margin) + margin
    max_y_screen_size = grid_size*(height+margin) + margin

    # We give pygame the size of our game window 
    screen = pygame.display.set_mode((max_x_screen_size, max_y_screen_size))

    # inital settings
    # snake defines the size of the snake
    snake = [1]

    # snake moves records all the snake moves
    snake_moves = []

    # Edit score
    score = 0

    # If the game is in superspeed mode
    superspeed = False

    return speed,MOVEEVENT,t,BLACK,WHITE,GREEN,RED,BLUE,width,height,grid_size,margin,max_x_screen_size,max_y_screen_size,screen,snake,snake_moves,score, superspeed   


def load_sprites():
    """Load the sprites into the game"""

    # We import the mushroom
    apple = pygame.image.load("mushroom.jpg")
    apple = pygame.transform.scale(apple, (width, height))
    apple_rect = apple.get_rect()

    # We need to import the bomb image
    bomb = pygame.image.load("bomb_2.jpg")
    bomb = pygame.transform.scale(bomb, (width, height))
    bomb_rect = bomb.get_rect()

    return apple,apple_rect, bomb, bomb_rect

def start_music():
    """Start the music"""

    # We define the first song
    filename = "03 Chibi Ninja.mp3"
    volume = 5

    # We load the sound
    pygame.mixer.music.load(filename) #music player
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

    # We load the sound effects
    eat_sound = pygame.mixer.Sound("apple-crunch.wav")
    boom_sound = pygame.mixer.Sound("boom.wav")
    return eat_sound, boom_sound

def show_rendert_txt(text, color, y, font_size):
    """Use to display text in a Game like font
    
    Args:
        text (string): text string
        color (rgb): rgb color e.g. (255,0,0)
        text (string): text string
        text (string): text string
    
    Returns:
        None
    
    """
    txt_to_display_font = pygame.font.Font('techkr/TECHKR__.TTF', font_size)
    txt_to_display = txt_to_display_font.render(text,0,color)
    txt_to_display_rect = txt_to_display.get_rect()
    txt_to_display_rect.center = (max_x_screen_size/2, y)
    txt_to_display_rect.y = y
    screen.blit(txt_to_display, txt_to_display_rect)

def intro():
    """Show the intro screen."""
    screen.fill(BLACK)
    show_rendert_txt("SnakeHSG", (255, 179, 0), 30, 250)
    intro = pygame.image.load("snake_intro.png")
    intro = pygame.transform.scale(intro, (200, 200))
    intro_rect = intro.get_rect()
    intro_rect.center = (max_x_screen_size/2, 400)
    show_rendert_txt("please press SPACE...", (255, 255, 255), 490, 60)
    show_rendert_txt("(C) 2019, Chantal, Anna-Maria, Ylli, Fabio and Mr. Bastien", (255, 255, 255), 670, 40)
    screen.blit(intro, intro_rect) # prints/renders the apple on new position
    pygame.display.flip()
    

def game_over():
    """Shows the game_over screen and set the score"""
    screen.fill(BLACK) # Change to a black screen

    # Show the text
    show_rendert_txt("YOU DIED!", (255,0,0), 60, 250)
    show_rendert_txt(f"Score {score}", (255,255,255), 260, 80)
    show_rendert_txt("Try again?...LOSER!", (255,255,255), 400, 80)
    show_rendert_txt("(Y)es?...(N)o?", (255,255,255), 500, 80)
    pygame.display.flip()

def show_snake(x_snake,y_snake, snake, snake_moves):
    """Display the snake on the grid
    
    Args:
        x_snake (int) : x position of snake
        y_snake (int) : y position of snake
        snake (list) : snake size
        snake_moves (list) : list of past moves of the snake
    Returns:
        None
    """
    # For the size of the snake we draw circle.
    for i in range(len(snake)):
        # If snake is 1 then it is part of the snake
        if snake[i] == 1:
            # We define the position of the snake by using the snake_moves at index 
            pos = (snake_moves[i][0], snake_moves[i][1])

            # If it is superspeed the colors are randomly selected, like the star in mario
            if superspeed:
                red = random.randint(0,255)
                green = random.randint(0,255)
                blue = random.randint(0,255)

            # Else we use standard green shades to color the snake
            else:
                green = 255
                green = green - i * 10
                if green < 0:
                    green = 255
                red = 140
                blue = 0

            pygame.draw.ellipse(screen, (red,green,blue), pygame.Rect(snake_moves[i][0], snake_moves[i][1], width, height))
        
def show_eyes(pos_eyes_1, pos_eyes_2):
    """Display the eyes of the snake
    
    Args:
        pos_eyes_1 (int): position of the first eye
        pos_eyes_2 (int): position of the first eye
    """
    color_eyes = BLACK
    radius = 4
    pygame.draw.circle(screen,color_eyes, pos_eyes_1, radius)
    pygame.draw.circle(screen,color_eyes, pos_eyes_2, radius)   

def show_tongue(x_tongue, y_tongue, width, height):
    """Display the tongue of the snake
    
    Args:
        x_tongue (int): x positon of the tongue
        y_tongue (int): y positon of the tongue
        width (int): width of the tongue
        heigh (int): height of the tongue
    """
    color_tongue = RED
    pygame.draw.rect(screen,color_tongue, pygame.Rect(x_tongue, y_tongue, width, height))      

def record_snake_position(x_snake, y_snake):
    """Record the postion of the snake
    
    Args:
        x_snake (int): x position of the snake
        y_snake (int): y position of the snake
    
    Returns:
        snake_moves (list): list of the past snake moves
    """
    # We append the moves
    snake_moves.append((x_snake,y_snake))
    return snake_moves

def show_apple(x_apple,y_apple):
    """Display the apple at given x and y
    
    Args:
        x_apple (int) : X position of the apple
        y_apple (int) : y position of the apple
    """

    apple_rect.x = x_apple
    apple_rect.y = y_apple
    color_apple = BLACK

def show_obstacle(x_obstacle,y_obstacle):
    """Display the bomb at given x and y
    
    Args:
        x_bomb (int) : X position of the bomb
        y_bomb (int) : y position of the bomb
    """
    bomb_rect.x = x_obstacle
    bomb_rect.y = y_obstacle

def show_grid():
    """Display the grid"""
    for row in range(grid_size):
        for column in range(grid_size):
            color = BLACK
            pygame.draw.rect(screen,color,[(margin + width) * column + margin,(margin + height) * row + margin,width,height])

# if the postion of the apple and the snake incl. body are the same, then change the x and y positoin of the apple
def create_random_position_apple(snake,snake_moves,grid_size, width, height, margin):
    """Create a new apple at a random position

    Args:
        snake (list) : list of the body of the snake
        snake_moves (list) : list of snake's past moves
        grid_size (tuple) : tuple of width / height
        height (int) : height of the window size
        width (int) : width of the window size
    
    Returns:
        x_apple_new (int) : the new apple x position
        y_apple_new (int) : the new apple y position
    """
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

def create_random_position_obstacle(snake,snake_moves,grid_size, width, height, margin):
    """Create a new bomb at a random position

    Args:
        snake (list) : list of the body of the snake
        snake_moves (list) : list of snake's past moves
        grid_size (tuple) : tuple of width / height
        height (int) : height of the window size
        width (int) : width of the window size
    
    Returns:
        x_obstacle_new (int) : the new obstacle x position
        y_obstacle_new (int) : the new obstacle y position
    """
    x_obstacle_new = margin + (random.randint(0,grid_size-1)*(width+margin))
    y_obstacle_new = margin + (random.randint(0,grid_size-1)*(height+margin))
    for i in range(len(snake)):
       if snake[i] == 1:
            if snake_moves==[]:
               pass
            else:
                if (x_obstacle_new, y_obstacle_new) in snake_moves:
                    x_obstacle_new = margin + (random.randint(0,grid_size-1)*(width+margin))
                    y_obstacle_new = margin + (random.randint(0,grid_size-1)*(height+margin))
            return x_obstacle_new, y_obstacle_new

def update_speed(speed):
    """update the speed of the snake """
    pygame.time.set_timer(MOVEEVENT, speed)

def change_music(filename):
    """Changes the background music"""
    pygame.mixer.music.stop()
    pygame.mixer.music.load(filename) #music player
    pygame.mixer.music.play(-1)

def eat_apple_and_define_new(x_head, y_head, x_apple, y_apple, score, grid_size, width, height, margin, snake,snake_moves, speed, eat_sound):
    """Create a new apple at a random position

    Args:
        x_head (int) : x position of the snake
        y_head (int) : y position of the snake
        x_apple (int) : y position of the apple
        y_apple (int) : y position of the apple
        score (int) :  current score of the game
        grid_size (tuple) :  width and height
        width (int) :  width of a grid bloc
        height (int) :  height of a grid bloc
        margin (int) :  margin of a grid
        snake (list) : position of the body
        snake_moves (list) : past position of the snake's body
        speed (int) : game's speed
        eat_sound (pygame.Sound) : Eat an apple sound

    Returns:
        x_apple (int) : the x positon of the apple
        y_apple (int) : the y positon of the apple
        score (int) : game's score
        snake (list) : list of the snake position
        snake_moves (list) : the list snake moves
        speed (int) : game's speed
    """
    if (x_head == x_apple) and (y_head == y_apple):
        snake.append(1)
        if superspeed:
            score +=5
        else:
            score+=1

        if speed  > 100:
            speed -= 20
            update_speed(speed)
        eat_sound.play()
        x_apple, y_apple = create_random_position_apple(snake, snake_moves, grid_size, width, height, margin)
        snake, snake_moves = cut_lenght_of_list(snake, snake_moves)
    else:
        snake.insert(0,0)
    return x_apple, y_apple, score, snake, snake_moves, speed

def cut_lenght_of_list(snake, snake_moves):
    snake_new = []
    snake_moves_new = []
    for i in range(len(snake)):
       if snake[i] == 1:
            snake_new.append(snake[i])
            snake_moves_new.append(snake_moves[i])
    return snake_new, snake_moves_new

def reinitialize_game():
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


    # define the initial  position of the 1st apple
    x_apple_random, y_apple_random = create_random_position_apple(snake, snake_moves, grid_size, width, height, margin)

    x_obstacle, y_obstacle = create_random_position_obstacle(snake, snake_moves, grid_size, width, height, margin)

    # record inital snake position in the histroy log
    snake_moves.append((rect_xp, rect_yp))

    # records initial timer (start ticker)
    start_ticks=pygame.time.get_ticks()
    change_music("03 Chibi Ninja.mp3")
    done = False
    direction_state = "RIGHT"
    do_again = True
    gameover = False

    return rect_xp,rect_yp,rect_change_xp,rect_change_yp,tong_width,tong_height,x_tongue,y_tongue,pos_eyes_1,pos_eyes_2,x_apple_random,y_apple_random, x_obstacle, y_obstacle, snake_moves,start_ticks,done,direction_state,do_again,gameover

def move_snake(direction, rect_xp, rect_yp):
    """Returns the next move that the snake has to do"""
    if direction == "UP":
        rect_yp=-rect_change_yp+rect_yp
        x_tongue = rect_xp + 15
        y_tongue = rect_yp - 5
        tong_width = 5
        tong_height = 15
        pos_eyes_1 = (rect_xp + 10, rect_yp - 10 + height)
        pos_eyes_2 = (rect_xp - 10 + width, rect_yp - 10 + height)
        return rect_xp, rect_yp, x_tongue, y_tongue, tong_width, tong_height, pos_eyes_1,pos_eyes_2
    elif direction == "DOWN":        
        rect_yp=rect_change_yp+rect_yp
        x_tongue = rect_xp + 15
        y_tongue = rect_yp + 25
        tong_width = 5
        tong_height = 15
        pos_eyes_1 = (rect_xp + 10, rect_yp + 10)
        pos_eyes_2 = (rect_xp - 10 + width, rect_yp + 10)
        return rect_xp, rect_yp, x_tongue, y_tongue, tong_width, tong_height, pos_eyes_1,pos_eyes_2
    elif direction == "LEFT":
        rect_xp = rect_xp - rect_change_xp
        x_tongue = rect_xp - 5
        y_tongue = rect_yp + 15
        tong_width = 15
        tong_height = 5
        pos_eyes_1 = (rect_xp - 10 + width, rect_yp - 10 + height)
        pos_eyes_2 = (rect_xp - 10 + width, rect_yp + 10)
        return rect_xp, rect_yp, x_tongue, y_tongue, tong_width, tong_height, pos_eyes_1,pos_eyes_2
    else:
        rect_xp=rect_change_xp+rect_xp
        x_tongue = rect_xp + 25
        y_tongue = rect_yp + 15
        tong_width = 15
        tong_height = 5
        pos_eyes_1 = (rect_xp + 10, rect_yp + 10)
        pos_eyes_2 = (rect_xp + 10, rect_yp - 10 + height)
        return rect_xp, rect_yp, x_tongue, y_tongue, tong_width, tong_height, pos_eyes_1,pos_eyes_2

speed,MOVEEVENT,t,BLACK,WHITE,GREEN,RED,BLUE,width,height,grid_size,margin,max_x_screen_size,max_y_screen_size,screen,snake,snake_moves,score, superspeed = init_variables()
eat_sound, boom_sound = start_music()
apple, apple_rect, bomb, bomb_rect = load_sprites()
rect_xp,rect_yp,rect_change_xp,rect_change_yp,tong_width,tong_height,x_tongue,y_tongue,pos_eyes_1,pos_eyes_2,x_apple_random,y_apple_random, x_obstacle, y_obstacle, snake_moves,start_ticks,done,direction_state,do_again,gameover = reinitialize_game()

intro()
start = False

while done == False:

    for event in pygame.event.get():    # check for any events
        if event.type == pygame.QUIT:
            done = True
        # Kill game if snake leaves boundries
        if rect_xp>max_x_screen_size or rect_xp<0:
            gameover = True
            
        if rect_yp>max_y_screen_size or rect_yp<0:
            gameover = True
                    
        # Kill game if snake hits its body
        if (rect_xp, rect_yp) in snake_moves:
            idx = snake_moves.index((rect_xp, rect_yp))
            if (snake[idx]) == 1 and (idx < len(snake)-1):
                gameover = True

        # Kill game if snake hits its obstacle
        if (x_obstacle, y_obstacle) == (rect_xp, rect_yp):
            boom_sound.play()
            pygame.time.delay(1000)
            gameover = True


        # act upon key events and sets new x and y positions for snake, tongue, eyes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True

            #Ture superspeed on
            if event.key == pygame.K_0:
                superspeed = True
                change_music("superspeed.mp3")
            if event.key == pygame.K_1:
                change_music("thriller.mp3")
            if event.key == pygame.K_2:
                change_music("tetris.mp3")
            if event.key == pygame.K_3:
                change_music("imblue.mp3")
            if event.key == pygame.K_4:
                change_music("another_one_bites.mp3")
            
            if event.key == pygame.K_5:
                change_music("mchammer.mp3")
            
            if event.key == pygame.K_m:
                pygame.mixer.music.stop()

            # Change the direction state when a key is pressed then the snake moves at ticks.
            if event.key == pygame.K_LEFT:
                direction_state = "LEFT"
            if event.key == pygame.K_RIGHT:
                direction_state = "RIGHT"
            if event.key == pygame.K_UP:
                direction_state = "UP" 
            if event.key == pygame.K_DOWN:
                direction_state = "DOWN"
            if event.key == pygame.K_n and gameover == True:
                pygame.quit()

            if event.key == pygame.K_y and gameover == True:
                speed,MOVEEVENT,t,BLACK,WHITE,GREEN,RED,BLUE,width,height,grid_size,margin,max_x_screen_size,max_y_screen_size,screen,snake,snake_moves,score, superspeed = init_variables()
                apple, apple_rect,bomb, bomb_rect = load_sprites()
                rect_xp,rect_yp,rect_change_xp,rect_change_yp,tong_width,tong_height,x_tongue,y_tongue,pos_eyes_1,pos_eyes_2,x_apple_random,y_apple_random, x_obstacle, y_obstacle, snake_moves,start_ticks,done,direction_state,do_again,gameover = reinitialize_game()

        if event.type == MOVEEVENT and start==True: # is called every 't' milliseconds
            # If superspeed => Increase the speed
            if superspeed == True:
                update_speed(50)

            rect_xp, rect_yp, x_tongue, y_tongue, tong_width, tong_height, pos_eyes_1,pos_eyes_2 = move_snake(direction_state, rect_xp, rect_yp)
            pygame.display.update()
            record_snake_position(rect_xp, rect_yp) # adds the latest position to a list (--> snake_move)
            x_apple_random, y_apple_random, score, snake, snake_moves, speed = eat_apple_and_define_new(rect_xp, rect_yp,x_apple_random, y_apple_random, score,grid_size, width, height, margin, snake, snake_moves,speed,eat_sound)

    if gameover:
        game_over()
    else:
        if start:
            screen.fill(pygame.Color('WHITE'))
            show_grid()
            show_snake(rect_xp,rect_yp, snake, snake_moves)
            show_tongue(x_tongue, y_tongue, tong_width, tong_height)
            show_eyes(pos_eyes_1, pos_eyes_2)
            show_apple(x_apple_random, y_apple_random) # renders new position of apple
            screen.blit(apple, apple_rect) # prints/renders the apple on new position
            show_obstacle(x_obstacle, y_obstacle)
            screen.blit(bomb, bomb_rect) # prints/renders the apple on new position
            #show timer & score
            font=pygame.font.SysFont("Verdana",30)    
            time_display=font.render(f"Time: {int((pygame.time.get_ticks()-start_ticks)/1000)} s",1,WHITE)
            screen.blit(time_display,(510,0))  #prints the timer on the screen
            score_display=font.render(f"Score: {score}",1,WHITE)
            screen.blit(score_display,(510,36))  #prints the timer on the screen
            score_display=font.render(f"Speed: {1/speed*1000}",1,WHITE)
            screen.blit(score_display,(510,72))  #prints the timer on the screen

            pygame.display.update()