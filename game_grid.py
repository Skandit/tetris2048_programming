import lib.stddraw as stddraw  # used for displaying the game grid
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
import copy
#colors ........................................
BG     = Color(0x00,0x22,0x4D)
GRID   = Color(0x5D,0x0E,0x41)
BLOCK  = Color(0xFF,0x20,0x4E)
MERGE  = Color(0xA0,0x15,0x3E)
# A class for modeling the game grid
class GameGrid:
   # A constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create a tile matrix to store the tiles locked on the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = BG
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = GRID
      self.boundary_color = GRID
      # thickness values used for the grid lines and the grid boundaries
      self.line_thickness = 0.002
      self.box_thickness = 10 * self.line_thickness
      self.score = 0
      self.score_flash_timer = 0
      self.next_tetromino = None     # ekranın altındaki Next için
        # Menü butonunun koordinatları:
      self.menu_x, self.menu_y = grid_w + 1, grid_h - 5
      self.menu_w, self.menu_h = 6, 3
      self.panel_w = 8
      self.panel_x = grid_w
      self.panel_h = grid_h


   # A method for displaying the game grid
   def display(self):
    stddraw.clear(self.empty_cell_color)
    self.draw_panel()     
    self.draw_grid()        
    if self.current_tetromino:
        self.current_tetromino.draw()
    self.draw_boundaries()
    stddraw.show(250)
    # Update score flash timer
    if self.score_flash_timer > 0:
        self.score_flash_timer -= 0.25  
        if self.score_flash_timer < 0:
            self.score_flash_timer = 0

   # A method for drawing the cells and the lines of the game grid
   def draw_grid(self):
      # for each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
            # if the current grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
               # draw this tile
                    self.tile_matrix[row][col].draw(Point(col, row))
      
       
        
      
      # draw the inner lines of the game grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
            stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method for drawing the boundaries around the game grid
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method used checking whether the grid cell with the given row and column
   # indexes is occupied by a tile or not (i.e., empty)
   def is_occupied(self, row, col):
      # considering the newly entered tetrominoes to the game grid that may
      # have tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False  # the cell is not occupied as it is outside the grid
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None

   # A method for checking whether the cell with the given row and col indexes
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   def settle_above_merges(self, merge_rows):
 
    H = self.grid_height
    for col, mrow in merge_rows.items():
        if mrow < 0:
            continue
       
        buf = [self.tile_matrix[r][col]
               for r in range(mrow+1, H)
               if self.tile_matrix[r][col] is not None]
       
        for r in range(mrow+1, H):
            self.tile_matrix[r][col] = None
       
        for i, tile in enumerate(buf):
            self.tile_matrix[mrow+1 + i][col] = tile


   # A method that locks the tiles of a landed tetromino on the grid checking
   # if the game is over due to having any tile above the topmost grid row.
   # (This method returns True when the game is over and False otherwise.)
   def update_grid(self, tiles_to_lock, blc_position):
    self.current_tetromino = None
    total_gain = 0
    n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
    for col in range(n_cols):
        for row in range(n_rows):
            t = tiles_to_lock[row][col]
            if t:
                x = blc_position.x + col
                y = blc_position.y + (n_rows - 1) - row
                if self.is_inside(y, x):
                    self.tile_matrix[y][x] = t
                else:
                    self.game_over = True
    if self.game_over:
        return True, 0

    clear_gain = self.clear_full_rows()
    total_gain += clear_gain
    while True:
        gain, merge_rows = self.merge_tiles_lowest()
        if gain == 0:
            break
        
        total_gain += gain
       
       
        self.settle_above_merges(merge_rows)

        while True:
            labels, num_labels = self.connected_blocks_labeling(self.tile_matrix, self.grid_width, self.grid_height)
            free_tiles = [[False for _ in range(self.grid_width)] for _ in range(self.grid_height)]
            free_tiles, num_free = self.get_free_tiles(self.grid_height, self.grid_width, labels, free_tiles)
            if num_free == 0:
                break
            self.down_free_tiles(free_tiles)

       

    return self.game_over, total_gain

   def does_tetromino_collide(self, tetromino):
    for i in range(len(tetromino.tile_matrix)):
        for j in range(len(tetromino.tile_matrix[i])):
            tile = tetromino.tile_matrix[i][j]
            if tile is not None:
                x = tetromino.bottom_left_cell.x + j
                y = tetromino.bottom_left_cell.y + i

                if not self.is_inside(y, x):
                    return True

                if self.tile_matrix[y][x] is not None:
                    return True
    return False
   
   def clear_full_rows(self):
      
        score_gain = 0
        new_rows = []

       
        for row in range(self.grid_height):
            row_tiles = list(self.tile_matrix[row])
            if all(tile is not None for tile in row_tiles):
                for tile in row_tiles:
                    score_gain += tile.number
            else:
                new_rows.append(row_tiles)
       
        num_cleared = self.grid_height - len(new_rows)
        for _ in range(num_cleared):
            new_rows.append([None] * self.grid_width)

        for r in range(self.grid_height):
            self.tile_matrix[r] = new_rows[r]

        return score_gain

   def merge_tiles_lowest(self):
   
    gained = 0
    merge_rows = {col: self.grid_height for col in range(self.grid_width)}

    for col in range(self.grid_width):
        merged = True
        while merged:
            merged = False
            for row in range(self.grid_height - 1):
                bot = self.tile_matrix[row][col]
                top = self.tile_matrix[row + 1][col]
                if bot and top and bot.number == top.number:
                    bot.number *= 2
                    self.tile_matrix[row + 1][col] = None
                    gained += bot.number
                    
                    merge_rows[col] = min(merge_rows[col], row)
                    merged = True
                    break
  
    for col in list(merge_rows):
        if merge_rows[col] == self.grid_height:
            merge_rows[col] = -1
    return gained, merge_rows
   
   def get_free_tiles(self, grid_h, grid_w, labels, free_tiles):
        total = 0
        label_record = []
        for i in range(grid_h):
            for j in range(grid_w):
                if labels[i, j] != 0 and labels[i, j] != 1:
                    if i == 0:
                        label_record.append(labels[i, j])
                    if not label_record.count(labels[i, j]):
                        free_tiles[i][j] = True
                        total += 1
        return free_tiles, total

   def down_free_tiles(self, free_tiles):
        for r in range(self.grid_height):
            for c in range(self.grid_width):
                if free_tiles[r][c]:
                    new_tile = copy.deepcopy(self.tile_matrix[r][c])
                    self.tile_matrix[r - 1][c] = new_tile
                    dx, dy = 0, -1
                    self.tile_matrix[r - 1][c].move(dx, dy)
                    self.tile_matrix[r][c] = None

   def connected_blocks_labeling(self, grid, grid_w, grid_h):
        labels = np.zeros([grid_h, grid_w], dtype=int)
        label_roots = []
        label_id = 1

        for row in range(grid_h):
            for col in range(grid_w):
                if grid[row, col] is None:
                    continue

                neighbors = self.find_neighbor_labels(labels, (col, row))
                if len(neighbors) == 0:
                    labels[row, col] = label_id
                    label_roots.append(label_id)
                    label_id += 1
                else:
                    labels[row, col] = min(neighbors)
                    if len(neighbors) > 1:
                        merge_set = set()
                        for lbl in neighbors:
                            merge_set.add(label_roots[lbl - 1])
                        self.merge_label_groups(label_roots, merge_set)

        self.normalize_label_indices(label_roots)

        for row in range(grid_h):
            for col in range(grid_w):
                if grid[row, col] is None:
                    continue
                labels[row, col] = label_roots[labels[row, col] - 1]

        return labels, len(set(label_roots))

   def find_neighbor_labels(self, label_array, coords):
        x, y = coords
        neighbor_set = set()

        if y > 0:
            upper_lbl = label_array[y - 1, x]
            if upper_lbl != 0:
                neighbor_set.add(upper_lbl)

        if x > 0:
            left_lbl = label_array[y, x - 1]
            if left_lbl != 0:
                neighbor_set.add(left_lbl)

        return neighbor_set

   def normalize_label_indices(self, label_roots):
        unique_roots = sorted(set(label_roots))
        new_map = np.zeros(max(label_roots) + 1, dtype=int)
        new_val = 1

        for lbl in unique_roots:
            new_map[lbl] = new_val
            new_val += 1

        for i in range(len(label_roots)):
            label_roots[i] = new_map[label_roots[i]]

   def merge_label_groups(self, label_list, merge_targets):
        smallest = min(merge_targets)
        for i in range(len(label_list)):
            if label_list[i] in merge_targets:
                label_list[i] = smallest
   
  

   def draw_panel(self):
  
    if self.score_flash_timer > 0:
        stddraw.setPenColor(Color(0, 255, 0))  
    else:
        stddraw.setPenColor(Color(255, 255, 255))
    stddraw.setFontSize(40)
    stddraw.text(self.panel_x + self.panel_w / 2, self.panel_h - 1, f"SCORE: {self.score}")


    mw, mh = 6, 3
    mx = self.panel_x + (self.panel_w - mw) / 2
    my = self.panel_h - 6.5  
    stddraw.setPenColor(Color(25, 200, 150))
    stddraw.filledRectangle(mx, my, mw, mh)
    stddraw.setPenColor(Color(255, 255, 255))
    stddraw.setFontSize(24)
    stddraw.text(mx + mw / 2, my + mh / 2, "MENU")

   
    stddraw.setPenColor(Color(255, 255, 255))
    stddraw.setFontSize(20)
    stddraw.text(self.panel_x + 2, 6, "NEXT TETROMINO:")

 
    if self.next_tetromino:
        mat = self.next_tetromino.get_min_bounded_tile_matrix(False)
        rows, cols = mat.shape

        center_x = self.panel_x + self.panel_w / 2
        base_y = 2  

        for r in range(rows):
            for c in range(cols):
                tile = mat[r][c]
                if tile:
                    offset_x = center_x - cols / 2
                    pos = Point(offset_x + c, base_y + (rows - 1 - r))
                    tile.draw(pos)