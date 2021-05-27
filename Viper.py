# Import Libaries
import sys 
import pygame 
import time 
import random 
import tkinter as tk

# Colours
white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
light_red =(255,0,0)
green = (0,155,0)
light_green = (0,210,0)
grey = (211,211,211)
yellow = (200,200,0)
light_yellow = (240,240,0)
light_blue = (0,50,255)
blue = (0,0,255)

# Global variables
DIFFICULTY = 1                              # Increse difficulty variable to increase the speed of the snake
START_LENGTH = 2                            # Length of the starting snake
WAIT = 0.1/DIFFICULTY                       # Changes the speed of the snake
PACE = 10                                   # Amount of pixels moved by snake
APPLE_THICKNESS = 30                        # Amount of pixels that makes up the apple
HEAD_THICKNESS = 20                         # Amount of pixels that makes up one body part of the snake
DISPLAY_WIDTH = 800                         # Width of display
DISPLAY_HEIGHT = 600                        # Height of display
RES  = [DISPLAY_WIDTH, DISPLAY_HEIGHT]      # Display size
FAILURE_MAX = 3                             # Amount of attempts for the login
PASSWORDS = []                              # Passwords array
BLUEAPPLE = (DISPLAY_WIDTH, DISPLAY_HEIGHT) # Initial blue apple position

# Setting display
pygame.init()
SCREEN = pygame.display.set_mode(RES)
pygame.display.set_caption("Viper")
icon = pygame.image.load('Apple1.png')
pygame.display.set_icon(icon)

# Declaring images
body = pygame.image.load('body.png')
head = pygame.image.load('snakeHead.png')
body2 = pygame.image.load('body2.png')
head2 = pygame.image.load('snakeHead2.png')
boost = pygame.image.load('boost.png')

# Declaring fonts
smallfont = pygame.font.SysFont('Calibri', 25)
medfont = pygame.font.SysFont('Calibri', 50)
largefont = pygame.font.SysFont('Elephant', 80)

SCREEN.fill(grey) # Grey screen

# Mob class used to generate each snake 
class Mob():  
    
    # Setting mobs intial values
    def __init__(self):
        self.headx = 0
        self.heady = 0
        self.length = START_LENGTH
        self.elements = [[self.headx, self.heady]]

        # While the length of elements isnt equal to the start length of the snake minus 1
        while len(self.elements) != (self.length - 1):
            self.elements.append([self.headx, self.heady]) # Add the element to the elements list
        self.speed = [PACE * 2, 0] # Starting speed
        pygame.display.update() # Update screen

    # Movement of the snake
    def movement(self):    
        self.elements.pop()
        self.headx += self.speed[0] # Starting x speed 
        self.heady += self.speed[1] # Starting y speed
        self.elements = [[self.headx, self.heady]] + self.elements[0:] # Saving new coordinate
        self.check_dead() # Check if dead
        self.check_apple() # Check apple
        update() # Update
        
    # Check dead function
    def check_dead(self):
        global Loser
        Loser = 0
        # If head coordinates equal coordinates in list of elements
        if [self.headx, self.heady] in self.elements[1:]:
            if [SNAKE.headx, SNAKE.heady] in SNAKE.elements[1:] and [SNAKE2.headx, SNAKE2.heady] in SNAKE2.elements[1:]:
                Loser += 3
            elif [SNAKE.headx, SNAKE.heady] in SNAKE.elements[1:]:
                Loser += 2
            else:
                Loser += 1
            end_game_loop() 
        # If head coordinates touch edge of screen 
        if SNAKE.headx >= DISPLAY_WIDTH or SNAKE.headx < 0 or SNAKE.heady >= DISPLAY_HEIGHT or SNAKE.heady < 0:
            Loser += 2
            end_game_loop() 
        if SNAKE2.headx >= DISPLAY_WIDTH or SNAKE2.headx < 0 or SNAKE2.heady >= DISPLAY_HEIGHT or SNAKE2.heady < 0:
            Loser += 1
            end_game_loop() 
        # Draw
        if [SNAKE.headx, SNAKE.heady] == [SNAKE2.headx, SNAKE2.heady]:
            Loser += 3
            end_game_loop()
        # Snake 1 loses
        if [SNAKE.headx, SNAKE.heady] in SNAKE2.elements[0:]:
            Loser += 2
            end_game_loop()
        # Snake 2 loses
        if [SNAKE2.headx, SNAKE2.heady] in SNAKE.elements[0:]:
            Loser += 1
            end_game_loop()

    # Check apple function
    def check_apple(self):
        chance = random.randrange(0, 5)
        #If the coordinates of the snake head, plus the size, is equal to the coordinates of the apple, plus the size, then detect collision
        if self.headx > apple_x and self.headx < apple_x + APPLE_THICKNESS or self.headx + HEAD_THICKNESS > apple_x and self.headx + HEAD_THICKNESS < apple_x + APPLE_THICKNESS:
            if self.heady > apple_y and self.heady < apple_y + APPLE_THICKNESS:
                self.elements.append(self.elements[-1])
                Sound()
                create_apple() # Make new apple      
                if chance == 1:
                    create_boost(True)
                        
            elif self.heady + HEAD_THICKNESS > apple_y and self.heady + HEAD_THICKNESS < apple_y + APPLE_THICKNESS:
                self.elements.append(self.elements[-1])
                Sound()
                create_apple()
                if chance == 1:
                    create_boost(True)

        if self.headx > blue_apple_x and self.headx < blue_apple_x + APPLE_THICKNESS or self.headx + HEAD_THICKNESS > blue_apple_x and self.headx + HEAD_THICKNESS < blue_apple_x + APPLE_THICKNESS:
            if self.heady > blue_apple_y and self.heady < blue_apple_y + APPLE_THICKNESS:
                for i in range(3):
                    self.elements.append(self.elements[-1])
                Sound()
                create_boost(False) # Make new apple              
                        
            elif self.heady + HEAD_THICKNESS > blue_apple_y and self.heady + HEAD_THICKNESS < blue_apple_y + APPLE_THICKNESS:
                for i in range(3):
                    self.elements.append(self.elements[-1])
                Sound()
                create_boost(False)

# Create boost apple
def create_boost(make):
    global BLUEAPPLE   
    BLUEAPPLE = ()      
    global blue_apple_x
    blue_apple_x = ()   
    global blue_apple_y
    blue_apple_y = ()

    if make:
        # Random generate x coordinate value between 0 and the display width, minus the apple thickness
        blue_apple_x = round(random.randrange(0, DISPLAY_WIDTH-APPLE_THICKNESS))
        # Random generate y coordinate value between 0 and the display height, minus the apple thickness
        blue_apple_y = round(random.randrange(0, DISPLAY_HEIGHT-APPLE_THICKNESS))
        BLUEAPPLE = (blue_apple_x, blue_apple_y)
    else:
        blue_apple_x = DISPLAY_WIDTH
        blue_apple_y = DISPLAY_HEIGHT
        BLUEAPPLE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

# Create apple function
def create_apple():
    global APPLE   
    APPLE = ()      
    global apple_x
    apple_x = ()   
    global apple_y
    apple_y = () 

    # Random generate x coordinate value between 0 and the display width, minus the apple thickness
    apple_x = round(random.randrange(0, DISPLAY_WIDTH-APPLE_THICKNESS))
    # Random generate y coordinate value between 0 and the display height, minus the apple thickness
    apple_y = round(random.randrange(0, DISPLAY_HEIGHT-APPLE_THICKNESS))
    # Set y and x values
    APPLE = (apple_x, apple_y)     
    update()
    
# Main event loop
def event_loop():
    while True:
        time.sleep(WAIT) # Frame rate speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit
                exit_dead()
            elif event.type == pygame.KEYDOWN:
                # Down
                if (event.key == pygame.K_DOWN)	and \
                    (SNAKE.speed != [0, -2*PACE]):
                    SNAKE.speed = [0, 2*PACE]
                # Up
                elif (event.key == pygame.K_UP) and \
                    (SNAKE.speed != [0, 2*PACE]):
                    SNAKE.speed = [0, -2*PACE]
                # Right
                elif (event.key == pygame.K_RIGHT) and \
                    (SNAKE.speed != [-2* PACE, 0]):
                    SNAKE.speed = [2*PACE, 0]
                # Left
                elif (event.key == pygame.K_LEFT) and \
                    (SNAKE.speed != [2* PACE, 0]):
                    SNAKE.speed = [-2*PACE, 0]
                # a
                elif (event.key == pygame.K_a) and \
                    (SNAKE2.speed != [2* PACE, 0]):
                    SNAKE2.speed = [-2*PACE, 0]
                # d
                elif (event.key == pygame.K_d) and \
                    (SNAKE2.speed != [-2* PACE, 0]):
                    SNAKE2.speed = [2*PACE, 0]
                # w
                elif (event.key == pygame.K_w) and \
                    (SNAKE2.speed != [0, 2*PACE]):
                    SNAKE2.speed = [0, -2*PACE]
                # s
                elif (event.key == pygame.K_s)	and \
                    (SNAKE2.speed != [0, -2*PACE]):
                    SNAKE2.speed = [0, 2*PACE]
                # esc
                elif event.key == pygame.K_ESCAPE:
                    exit_dead()
                # p
                elif event.key == pygame.K_p:
                    Pause()
        SNAKE.movement() # Snake 1 movement
        SNAKE2.movement() # Snake 2 movement

# Updating screen
def update():
    SCREEN.fill(grey)
    for element in SNAKE.elements[1:]:
        SCREEN.blit(body, [element[0], element[1], HEAD_THICKNESS, HEAD_THICKNESS]) # Drawing body
    SCREEN.blit(head, [SNAKE.headx, SNAKE.heady, HEAD_THICKNESS, HEAD_THICKNESS])   # Drawing head
    for element in SNAKE2.elements[1:]:
        SCREEN.blit(body2, [element[0], element[1], HEAD_THICKNESS, HEAD_THICKNESS])# Drawing second body
    SCREEN.blit(head2, [SNAKE2.headx, SNAKE2.heady, HEAD_THICKNESS, HEAD_THICKNESS])# Drawing second head
    SCREEN.blit(icon, (APPLE))                                                      # Drawing apple
    SCREEN.blit(boost, (BLUEAPPLE))                                                 # Drawing boost
    score()
    pygame.display.update()
    
# Start screen
def StartScreen():
    intro = True # Start screen is true

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit
                exit_dead()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m: # m
                    clear_score_ratio() # Clear score tracker

        # Make start screen
        SCREEN.fill(grey)
        reading_winRation()
        user_name_display()
        high_score()
        # Text added to the screen
        message_to_screen('Welcome to Viper!', green, -150, 'large')
        message_to_screen('The objective of the game is to kill the other player', black, -30)
        message_to_screen('The more apples you eat, the longer you get,', black, 10)
        message_to_screen('If you run into yourself, or the edges, or the other player you die!', black, 50)
        # Buttons displayed on screen
        button('Play', (DISPLAY_WIDTH/4)-50,500,100,50, green, light_green, action = 'play')
        button('Controls', (DISPLAY_WIDTH/2)-50,500,100,50, yellow, light_yellow, action = 'controls')
        button('Quit', ((DISPLAY_WIDTH/4)*3)-50,500,100,50, red, light_red, action = 'quit')
        pygame.display.update()

# Control Screen
def game_controls():
    controls = True # Control page true

    while controls:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit
                exit_dead()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m: # m             
                    clear_score_ratio() # Clear score tracker               
        
        SCREEN.fill(grey)
        # Add text to screen
        message_to_screen('Controls', red, -100, 'large')
        message_to_screen('P1 Move Snake: Arrow keys', black, -30)
        message_to_screen('P2 Move Snake: W,A,S,D keys', black, 10)
        message_to_screen('Pause: P', black, 50)
        message_to_screen('To clear win ratio: M', black, 90)       
        # Add buttons to screen
        button('Play', (DISPLAY_WIDTH/4)-50,500,100,50, green, light_green, action = 'play')
        button('Quit', ((DISPLAY_WIDTH/4)*3)-50,500,100,50, red, light_red, action = 'quit')
        pygame.display.update()

# Pause screen
def Pause():
    paused = True # Pause screen true
    # Text displayed
    message_to_screen('PAUSED', black, -100, size='large')
    message_to_screen('Press P to CONTINUE or Q to QUIT', black, 25)
    pygame.display.update()

    while paused:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: # p
                    paused = False
                elif event.key == pygame.K_q:
                    exit_dead()
            
        time.sleep(0.25) # Delay

# Displaying score
def score():
    text = smallfont.render('Green: ' + str(len(SNAKE.elements) - START_LENGTH + 1), True, black)
    SCREEN.blit(text, [700,570]) # Where it will render

    text2 = smallfont.render('Blue: ' + str(len(SNAKE2.elements) - START_LENGTH + 1), True, black)
    SCREEN.blit(text2, [5,5])
    pygame.display.update()

# Starting position of snakes
def StartPos():
    # Snake 1
    SNAKE.headx = 100
    SNAKE.heady = 500
    # Snake 2
    SNAKE2.headx = 100
    SNAKE2.heady = 100

# Sound effect
def Sound():
    pygame.mixer.music.load('Apple_bite.mp3')# Loading sound
    pygame.mixer.music.set_volume(0.5) # Setting volume
    pygame.mixer.music.play(1) # Playing it once   

# Defining texts
def text_objects(text, color, size):
    if size == 'small':
        textSurface = smallfont.render(text, True, color)
    elif size == 'medium':
        textSurface = medfont.render(text, True, color)
    elif size == 'large':
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()

# Screen text
def message_to_screen(msg, color, y_displace=0, size = 'small'):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/2) + y_displace
    SCREEN.blit(textSurf, textRect)

# Adding text to buttons
def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size ='small'):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    SCREEN.blit(textSurf, textRect)

# Button function
def button(text, x, y, width, height, inactive_colour, active_colour, action = None):
    # Cursor pos
    cur = pygame.mouse.get_pos()
    # Click pos
    click = pygame.mouse.get_pressed()

    # When cursor is over button
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(SCREEN, active_colour, (x,y,width,height)) # Change colour
        if click[0] == 1 and action != None: # If pressed
            if action == 'quit':
                exit_dead()

            if action == 'controls':
                game_controls()

            if action == 'play':
                load_game()
                event_loop()           
    else:
        pygame.draw.rect(SCREEN, inactive_colour, (x,y,width,height)) # Render buttons

    text_to_button(text,black,x,y,width,height)

# Displaying win ratio
def reading_winRation():
    title = 'Win Ratio'
    message_to_screen(title, blue, 110, 'medium')
    file_score = open('score.txt', 'r') # Read
    score_snake = file_score.readline()
    score_snake = score_snake.split() # Split
    g = str(score_snake[0]) # Player 1
    b = str(score_snake[1]) # Player 2
    file_score.close() # Close file
    text = 'Green Snake ' + g + ' | ' + 'Blue Snake ' + b
    message_to_screen(text, black, 160, 'small') # Displaying score ratio 

# Increasing winners ratio
def change_score(win):
    if win == 1:#if player 1 wins
        file_score = open('score.txt', 'r')
        t = file_score.readline()
        t = t.split()
        num = int(t[0])
        num += 1
        t[0] = str(num)
        new_score = " ".join(t)
        file_score.close()
        file_score = open('score.txt', 'w')
        file_score.write(new_score)
        file_score.close()
    elif win == 2:#if player 2 wins
        file_score = open('score.txt', 'r')
        t = file_score.readline()
        t = t.split()
        num = int(t[1])
        num += 1
        t[1] = str(num)
        new_score = " ".join(t)
        file_score.close()
        file_score = open('score.txt', 'w')
        file_score.write(new_score)
        file_score.close()

# Resetting win ratio
def clear_score_ratio():
    file_score = open('score.txt', 'w')
    i = '0 0'
    file_score.write(i)
    file_score.close()

# Selecting winner
def who_won():
    if Loser == 1:
        message_to_screen('GREEN SNAKE WINS', green, y_displace=-50, size='medium')
        change_score(1)
    elif Loser == 2:
        message_to_screen('BLUE SNAKE WINS', blue, y_displace=-50, size='medium')
        change_score(2)
    elif Loser == 3:
        message_to_screen('DRAW', light_yellow, y_displace=-50, size='medium')
    pygame.display.update()

# Ending game loop
def end_game_loop():
    who_won()
    new_high_score()
    time.sleep(2)
    StartScreen()

# Resetting snake body
def reset_elements():
    SNAKE.elements = []
    while len(SNAKE.elements) != (START_LENGTH - 1):
        SNAKE.elements.append([SNAKE.headx, SNAKE.heady])

    SNAKE2.elements = []
    while len(SNAKE2.elements) != (START_LENGTH - 1):
        SNAKE2.elements.append([SNAKE2.headx, SNAKE2.heady])

# Starting movement direction
def starting_direction():
    SNAKE.speed = [PACE * 2, 0]
    SNAKE2.speed = [PACE * 2, 0]

# Store password
def stored_password():
    try:
        file_username = open('USERNAME.txt', 'r')
    except:
        print('stored_password error')
    try:
        file_password = open('PASSWORD.txt', 'r')
    except:
        print('stored_password error')
    user = file_username.readline()
    name = user.split()
    num = len(name)
    passw = file_password.readline()
    logpass = passw.split()
    for i in range(0,num):
        use_pass = (name[i], logpass[i])
        PASSWORDS.append(use_pass)

    file_username.close()
    file_password.close()

# Tkinter Entry
def make_entry(parent, caption, width=None, **options):
    tk.Label(parent, text=caption).pack(side=tk.TOP)
    entry = tk.Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
    return entry

# Enter
def enter(event): 
    check_password()

# Check details
def check_password(failures=[]): 
    PASSWORDS.clear()
    stored_password()
    Encryption()
    amount_in_list = 0
    global player_amount
    for i in PASSWORDS:
        amount_in_list = amount_in_list + 1 # Finding the position of the user
        if (user.get(), final) == i:
            player_amount = (amount_in_list - 1)
            root.destroy()
            return
    #if login equals the password in list       
    if (user.get(), password.get()) in PASSWORDS:
        root.destroy()
        print('Logged in')
        return
    failures.append(1)
    # Checking if they have tried too many times
    if sum(failures) >= FAILURE_MAX:
        print('login attempts expired')
        root.destroy()
        exit_dead()
        raise SystemExit('Unauthorized login attempt')
    else:
        root.title('Try again. Attempt %i/%i' % (sum(failures)+1, FAILURE_MAX))

# Password hash encryption
def Encryption():
    global final # Finished encryption
    ascii_list = [] # Array to hold ascii values
    paword = (password.get()) # Retrieving password entered
    wordlist = list(paword) # Making it into a list             
    wordlist = [ch for ch in paword] # Seperating it into list of characters
    for i in wordlist:
        a = ord(i) # Getting ascii value and adding it to the list
        ascii_list.append(str(a))

    ascii = "".join(ascii_list) # Join the list together

    length = list(ascii)
    length = [ch for ch in ascii] # Seperating it into single digit list
    ascii_length = str(len(length)) # Finding length
    ascii_length = list(ascii_length) # Making length list
    new_list = ascii_list + ascii_length # Adding length value to the end of the ascii compressed value

    joined_new_list = "".join(new_list) # Joining it

    arrange = list(joined_new_list)
    arrange = [ch for ch in joined_new_list] # Seperating it into single digits
    # For each number, if the length of the list is greater or equal, then place number in its position in the list
    for i in arrange:
        if int(i) <= len(arrange):
            num = int(i) 
            arrange[num] = i
                
    final = "".join(arrange) # Joining final number together

# Stores a new username and password     
def new_user():
    Encryption()
    root.title('New User') # Set title
    
    for i in PASSWORDS:
        # If the list of passwords contains the login
        if(user.get(), final) == i:
            root.title('Taken Login')
        # If the length of the password or username is smaller than 4 or greater than 10
        elif (len(password.get()) < 4) or (len(password.get()) > 10):
            root.title('Password not suitable')
        elif (len(user.get()) < 4) or (len(user.get()) > 10):
            root.title('Username not suitable')
        else:
            try:
                file_username = open('NEW_USERNAME.txt', 'w')
            except:
                print('error')
            try:
                file_password = open('NEW_PASSWORD.txt', 'w')
            except:
                print('error')
            file_username.write(user.get()) # Write the username
            file_password.write(final) # Write the password
            file_username.close()
            file_password.close()

            try:
                f = open('NEW_USERNAME.txt', 'r')
            except:
                print('error')
            try:
                P = open('NEW_PASSWORD.txt', 'r')
            except:
                print('error')
            try:
                U = open('USERNAME.txt', 'r')
            except:
                print('error')
            try:              
                N = open('PASSWORD.txt', 'r')
            except:
                print('error')
            get = f.readline()
            ge = get.split()  # Split the file into a list     
            pas = P.readline()
            pa = pas.split()
            use = U.readline()
            name = use.split()
            passw = N.readline()
            logpass = passw.split()
            new_u = (name + ge) # Connect files
            new_p = (logpass + pa)
            new_u = " ".join(new_u)
            new_p = " ".join(new_p)
            f.close()
            P.close()
            U.close()
            N.close()

            # Append username and password to files
            try:
                fi_use = open('USERNAME.txt', 'w')
            except:
                print('error')
            try:
                fi_pas = open('PASSWORD.txt', 'w')
            except:
                print('error')
            fi_use.write(new_u) 
            fi_pas.write(new_p)
            fi_use.close()
            fi_pas.close()
            adding_new_player_score()
            root.title('Login Set')
            break

# Makes a new players score
def adding_new_player_score():
    array = ['0']
    f = open('HIGH_SCORE.txt', 'r')
    fi = f.readline()
    fi = fi.split()
    new_num = (fi + array)
    new_num = " ".join(new_num)
    f.close()

    f = open('HIGH_SCORE.txt', 'w')
    f.write(new_num)
    f.close()    

# Displays the users username
def user_name_display():
    try:
        f = open('USERNAME.txt', 'r')
    except:
        print('error')
    username = f.readline()
    username = username.split()
    name = (username[player_amount])
    name = str(name)
    f.close()
    text = smallfont.render('Welcome: ' + (name), True, black)
    SCREEN.blit(text, [1,1])

# Displays the players best score
def high_score():
    f = open('HIGH_SCORE.txt', 'r')
    amounts = f.readline()
    amounts = amounts.split()
    best_points = int((amounts[player_amount]))
    best_score = str(best_points)
    f.close()
    text = smallfont.render('PB Snake Length: ' + (best_score), True, black)
    SCREEN.blit(text, [570,1])

# Setting HIGH_SCORE text file
def new_high_score():
    f = open('HIGH_SCORE.txt', 'r') # Open
    amou = f.readline() # Read
    amou = amou.split() # Split
    f.close()# Close
    # If snake greater than snake2
    if len(SNAKE.elements) > len(SNAKE2.elements):
        # If snake is greater than record
        if len(SNAKE.elements) > len(amou[player_amount]):
            f = open('HIGH_SCORE.txt', 'w')
            num = len(SNAKE.elements)
            amou[player_amount] = str(num)# Append list
            amou = " ".join(amou)
            f.write(amou)        
            f.close()
    # If snake2 greater than snake
    elif len(SNAKE2.elements) > len(SNAKE.elements):
        if len(SNAKE2.elements) > len(amou[player_amount]):
            f = open('HIGH_SCORE.txt', 'w')
            num = len(SNAKE2.elements)
            amou[player_amount] = str(num)
            amou = " ".join(amou)
            f.write(amou) 
            f.close()
    # If equal
    elif len(SNAKE.elements) == len(SNAKE2.elements):
        if len(SNAKE.elements) > len(amou[player_amount]):
            f = open('HIGH_SCORE.txt', 'w')
            num = len(SNAKE.elements)
            amou[player_amount] = str(num)
            amou = " ".join(amou)
            f.write(amou) 
            f.close()    

# Loading the game
def load_game():
    reset_elements()    # Reset snake bodys
    starting_direction()# Calling starting direction
    StartPos()          # Stating position of snake's
    create_apple()      # Create apple
    create_boost(False)  # Make boost

# Exit/dead funtion
def exit_dead():
    clear_score_ratio() # Clear score 
    pygame.quit()
    sys.exit()

# Login box
def login():
    root.geometry('300x160')
    root.title('Viper Login')
    # Login buttons
    b = tk.Button(parent, borderwidth=4, text="Login", width=10, pady=8, command=check_password)
    t = tk.Button(parent, borderwidth=2, text="New User", width=10, pady=4, command=new_user)
    # Placement of buttons
    b.pack(side=tk.BOTTOM)
    t.pack(side=tk.BOTTOM)
    # Enter key calls enter function
    password.bind('<Return>', enter)
    stored_password() # Store password
    user.focus_set()
    parent.mainloop()


# Start
if __name__ == "__main__":
    root = tk.Tk()
    parent = tk.Frame(root, padx=10, pady=10)
    parent.pack(fill=tk.BOTH, expand=True)
    user = make_entry(parent, "Username:", 16)
    password = make_entry(parent, "Password:", 16, show="*")
    login()
    SNAKE = Mob() # Create snake 1 object
    SNAKE2 = Mob() # Create snake 2 object
    StartScreen() # Calling StartScreen