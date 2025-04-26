import lib.stddraw as stddraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles
from point import Point
import numpy as np
from lib.color import Color  # used for coloring the tiles

COLOR_PALETTE = {
    2:    Color(243, 255, 144),  
    4:    Color(220, 245, 120),  
    8:    Color(190, 235, 80),  
    16:   Color(155, 236, 0),   
    32:   Color(100, 200, 0),   
    64:   Color(60, 180, 0),    
    128: Color(223, 151, 85),  
    256: Color(250, 213, 154),  # FAD59A
    512: Color(233, 163, 25),   # E9A319
    1024: Color(223, 151, 85),  # DF9755
    2048: Color(255,143,135),  # A86523
}
# A class for modeling numbered tiles as in 2048
class Tile:
   # Class variables shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and font size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # A constructor that creates a tile with 2 as the number on it
   def __init__(self, position = Point(0, 0)):
      # set the number on this tile
      numbers = [2,4]
      self.number = int(np.random.choice(numbers,1))
      # set the colors of this tile
      self.background_color = Color(151, 178, 199)  # background (tile) color
      self.foreground_color = Color(0, 100, 200)  # foreground (number) color
      self.box_color = Color(0, 100, 200)  # box (boundary) color
      self.position = Point(position.x, position.y)
   # A method for drawing this tile at a given position with a given length
   def draw(self, pos):
    # Number'a göre renk seç
    color = COLOR_PALETTE.get(self.number, Color(255, 255, 255))  # Bulamazsa beyaz yapar

    stddraw.setPenColor(color)
    stddraw.filledSquare(pos.x, pos.y, 0.5)  # Blok çizimi

    # Sayı yaz
    stddraw.setPenColor(Color(0, 0, 0))  # Siyah yazı
    stddraw.setFontSize(18)
    stddraw.text(pos.x, pos.y, str(self.number))

   def move(self, dx, dy):
      self.position.translate(dx, dy)
