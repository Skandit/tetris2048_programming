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





# track whether the drawing canvas has been set up
canvas_initialized = False

#colors ........................................
BG     = Color(0x00,0x22,0x4D)
GRID   = Color(0x5D,0x0E,0x41)
BLOCK  = Color(0xFF,0x20,0x4E)
MERGE  = Color(0xA0,0x15,0x3E)
# The main function where this program starts execution
def start():
    global canvas_initialized
    
    stddraw.clearKeysTyped()#clear the keys typed

    grid_h = 20
    grid_w = 12
    panel_w = 8
    canvas_w = 40 * (grid_w + panel_w) # screens size control
    canvas_h = 40 * grid_h # screens size control

    if not canvas_initialized:
        stddraw.setCanvasSize(canvas_w, canvas_h)
        stddraw.setXscale(-0.5, grid_w + panel_w - 0.5)
        stddraw.setYscale(-0.5, grid_h - 0.5)
        canvas_initialized = True
   
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w

   
    grid = GameGrid(grid_h, grid_w)
    grid.score = 0


    menuxcords = grid.menu_x
    menuycords = grid.menu_y
    menuhcords = grid.menu_h
    menuwcords = grid.menu_w


    grid.next_tetromino = Tetromino(random.choice(['I','O','Z','S','L','J','T','X']))
    current_tetromino = grid.next_tetromino
    grid.current_tetromino = current_tetromino
    grid.next_tetromino = Tetromino(random.choice(['I','O','Z','S','L','J','T','X']))
    
    #to do more smooth drop
    


    #holds the info if game is paused. 
    is_paused = False
    #show main starting screen.
    display_game_menu(20, 20)
    
    
    #main loop 
    while True:
        #checks if user paused the game by button
        if stddraw.mousePressed():
                mx, my = stddraw.mouseX(), stddraw.mouseY()
                if(menuxcords <= mx <= menuxcords + menuwcords and
        menuycords <= my <= menuycords + menuhcords):
                        is_paused = True
                        print("Stopped")
                        choice1 = display_pause_menu(grid_h, grid_w + panel_w)
                        is_paused = False
                        if choice1 == 'restart':
                            return  # exit start() to trigger a full restart
                        # if 'resume', continue the game loop
                        continue
        if stddraw.hasNextKeyTyped():
            
            key = stddraw.nextKeyTyped()
            if key == "p":
                is_paused = True
                choice = display_pause_menu(grid_h, grid_w + panel_w)
                is_paused = False
                if choice == 'restart':
                    return  # exit start() to trigger a full restart
                # if 'resume', continue the game loop
                continue
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
            success = current_tetromino.move("down", grid)
            
        if not success:
            if current_tetromino.type == "X":
                game_over, gained = grid.update_grid(None, None)

            else:
                tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
                game_over, gained = grid.update_grid(tiles, pos)

            if game_over:

                print("Game Over")
                for a in range(0, 20):
                    for b in range(12):
                        grid.tile_matrix[a][b] = None
                display_restart_menu(grid_h, grid_w + panel_w, grid.score)
                return
            if grid.has_won():
                display_win_menu(grid_h, grid_w + panel_w, grid.score)
                return
            else:
                grid.score += gained
                if gained > 0:
                    grid.score_flash_timer = 0.5

            current_tetromino = grid.next_tetromino
            grid.current_tetromino = current_tetromino
            grid.next_tetromino = Tetromino(random.choice(['I','O','Z','S','L','J','T','X']))

        grid.display()



# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
    # the type (shape) of the tetromino is determined randomly
    tetromino_types = ['I', 'O', 'Z', 'S', 'L', 'J', 'T', 'X']
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
    button_resume_x, button_resume_y = img_center_x - button_w / 2, 4
    # add the resume game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_resume_x, button_resume_y, button_w, button_h)
    # add the text on the resume game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Resume the Game"
    stddraw.text(img_center_x, 5, text_to_display)
    
    # the dimensions for the restart game button
    button_w, button_h = grid_width - 1.5, 2
    # the coordinates of the bottom left corner for the restart game button
    button_restart_x, button_restart_y = img_center_x - button_w / 2, 1
    # add the restart game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_restart_x, button_restart_y, button_w, button_h)
    
    # add the text on the restart game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Restart the Game"
    stddraw.text(img_center_x, 2, text_to_display)

    # the user interaction loop for the simple menu
    

    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if mouse_x >= button_resume_x and mouse_x <= button_resume_x + button_w:
                if mouse_y >= button_resume_y and mouse_y <= button_resume_y + button_h:
                    return 'resume' # break the loop to end the method and start the game
            if mouse_x >= button_restart_x and mouse_x <= button_restart_x + button_w:
                if mouse_y >= button_restart_y and mouse_y <= button_restart_y + button_h: 
                    return 'restart' # break the loop to end the method and start the game
                
                
def display_restart_menu(grid_height,grid_width,score):
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

    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(32)
    stddraw.setPenColor(text_color)
    stddraw.text(img_center_x, 8, "GAME OVER")
    stddraw.setFontSize(24)
    stddraw.text(img_center_x, 6.5, f"Score: {score}")

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

def display_win_menu(grid_height,grid_width,score):
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

    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(32)
    stddraw.setPenColor(text_color)
    stddraw.text(img_center_x, 8, "YOU WON")
    stddraw.setFontSize(24)
    stddraw.text(img_center_x, 6.5, f"Score: {score}")

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
   # keep the window open and allow restarting
    while True:
        start()