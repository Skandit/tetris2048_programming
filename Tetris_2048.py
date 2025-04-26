################################################################################
#                                                                              #
#            The main program of Tetris 2048 Base Code                         #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)
import time
#colors ........................................
BG     = Color(0x00,0x22,0x4D)
GRID   = Color(0x5D,0x0E,0x41)
BLOCK  = Color(0xFF,0x20,0x4E)
MERGE  = Color(0xA0,0x15,0x3E)
# The main function where this program starts execution
def start():

    import random
    from tetromino import Tetromino
    from game_grid import GameGrid
    import lib.stddraw as stddraw

    move_interval = 0.1  # saniye cinsinden: her 0.1 saniyede bir sağ/sol kaydır
    last_move_time = time.time()


    grid_h = 20
    grid_w = 12
    panel_w = 8
    canvas_w = 40 * (grid_w + panel_w)
    canvas_h = 40 * grid_h

    stddraw.setCanvasSize(canvas_w, canvas_h)
    stddraw.setXscale(-0.5, grid_w + panel_w - 0.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)

   
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w

   
    grid = GameGrid(grid_h, grid_w)
    grid.score = 0

    grid.next_tetromino = Tetromino(random.choice(['I','O','Z','S','L','J','T']))
    current_tetromino = grid.next_tetromino
    grid.current_tetromino = current_tetromino
    grid.next_tetromino = Tetromino(random.choice(['I','O','Z','S','L','J','T']))
    
    #to do more smooth drop
    drop_interval = 0.5  # seconds per row
    last_drop_time = time.time()


    #holds the info if game is paused. 
    is_paused = False
    #show main starting screen.
    display_game_menu(20, 20)
    drop_interval_down_key = 0.05  # down tuşuna basarken satır atlama süresi
    is_down_pressed = False 
    #main loop 
    while True:
        
        if stddraw.hasNextKeyTyped():
            
            key = stddraw.nextKeyTyped()
            if key == "p":
                is_paused = not is_paused
                display_pause_menu(20, 20)
            elif not is_paused and key in ("left", "right", "down", "r"):
                if key in ("left", "right"):
                    current_tetromino.move(key, grid)
                elif key == "down":
                    while current_tetromino.move("down", grid):
                        pass

                elif key == "r":
                    current_tetromino.rotate_clockwise(grid)
                
            stddraw.clearKeysTyped()
        
        if not is_paused:
            now = time.time()
            if now - last_drop_time >= drop_interval:
                last_drop_time = now
            success = current_tetromino.move("down", grid)
            last_drop_time = now
        if not success:
            tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
            game_over, gained = grid.update_grid(tiles, pos)

            if game_over:

                print("Game Over")
                display_restart_menu(grid_h, grid_w)
                return
            else:
                grid.score += gained
                if gained > 0:
                    grid.score_flash_timer = 0.5

            current_tetromino = grid.next_tetromino
            grid.current_tetromino = current_tetromino
            grid.next_tetromino = Tetromino(random.choice(['I','O','Z','S','L','J','T']))

        grid.display()



# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
   # the type (shape) of the tetromino is determined randomly
   tetromino_types = ['I', 'O', 'Z', 'S', 'L', 'J', 'T']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   # the colors used for the menu
   background_color = Color(53,55,75)    
   button_color = Color(255, 32, 78)        
   text_color = Color(255, 255, 255)       

   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # compute the path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # the coordinates to display the image centered horizontally
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # the image is modeled by using the Picture class
   image_to_display = Picture(img_file)
   # add the image to the drawing canvas
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # the dimensions for the start game button
   button_w, button_h = grid_width - 1.5, 2
   # the coordinates of the bottom left corner for the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # add the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # add the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)
   # the user interaction loop for the simple menu
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the start game button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break  # break the loop to end the method and start the game
def display_pause_menu(grid_height, grid_width):
    background_color = Color( 64,  64,  64)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background drawing canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # compute the path of the image file
    img_file = current_dir + "/images/menu_image.png"
    # the coordinates to display the image centered horizontally
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # the image is modeled by using the Picture class
    image_to_display = Picture(img_file)
    # add the image to the drawing canvas
    stddraw.picture(image_to_display, img_center_x, img_center_y)

    # the dimensions for the resume game button
    button_w, button_h = grid_width - 1.5, 2
    # the coordinates of the bottom left corner for the resume game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    # add the resume game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # add the text on the resume game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Resume the Game"
    stddraw.text(img_center_x, 5, text_to_display)
    # the user interaction loop for the simple menu


    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end the method and start the game

def display_restart_menu(grid_height,grid_width):
    background_color = Color( 64,  64,  64)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background drawing canvas to background_color
    stddraw.clear(BG)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # compute the path of the image file
    img_file = current_dir + "/images/menu_image.png"
    # the coordinates to display the image centered horizontally
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # the image is modeled by using the Picture class
    image_to_display = Picture(img_file)
    # add the image to the drawing canvas
    stddraw.picture(image_to_display, img_center_x, img_center_y)

    # the dimensions for the restart game button
    button_w, button_h = grid_width - 1.5, 2
    # the coordinates of the bottom left corner for the restart game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    # add the restart game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)

    # add the text on the restart game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Restart the Game"
    stddraw.text(img_center_x, 5, text_to_display)

    # the user interaction loop for the simple menu
    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end the method and start the game

# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
   start()
