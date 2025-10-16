import board
import fourwire
import adafruit_ili9341
import displayio

from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.circle import Circle as Circumference  # reuse for circle outline only

displayio.release_displays()
display_bus = fourwire.FourWire(board.SPI(), command=board.LCD_DC, chip_select=board.LCD_CS, reset=None)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

display.rotation = 180

my_group = displayio.Group()
display.root_group = my_group

# -------------------------------
# GLOBAL STYLE SETTINGS
# -------------------------------
current_fill = (255, 0, 0)      # default fill color (red)
current_outline = (0, 0, 0)     # default outline color (black)
current_stroke = 1              # default stroke width

# -------------------------------
# COLOR HELPER
# -------------------------------
def color(name):
    """Set the current drawing color by name.
       Example: color("red") will set fill to red for all next shapes."""
    global current_fill
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "gray": (128, 128, 128),
        "brown": (155, 40, 10)
    }
    if name in colors:
        current_fill = colors[name]

def outline(name):
    """Set the outline color for next shapes."""
    global current_outline
    color_map = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "white": (255, 255, 255),
        "black": (0, 0, 0)
    }
    if name in color_map:
        current_outline = color_map[name]

def stroke(width):
    """Set the stroke width for outlines."""
    global current_stroke
    current_stroke = width

# -------------------------------
# SHAPE HELPERS
# -------------------------------
def rectangle(x, y, w, h):
    """Draw a rectangle at (x,y) with width w and height h."""
    r = Rect(x, y, w, h, fill=current_fill, outline=current_outline, stroke=current_stroke)
    my_group.append(r)

def circle(x, y, radius):
    """Draw a filled circle with center (x,y) and given radius."""
    c = Circle(x, y, radius, fill=current_fill, outline=current_outline, stroke=current_stroke)
    my_group.append(c)

def triangle(x0, y0, x1, y1, x2, y2):
    """Draw a triangle with 3 points (no stroke support)."""
    t = Triangle(x0, y0, x1, y1, x2, y2, fill=current_fill, outline=current_outline)
    my_group.append(t)

def line(x0, y0, x1, y1):
    """Draw a straight line between two points (no stroke support)."""
    l = Line(x0, y0, x1, y1, color=current_fill)
    my_group.append(l)

def circle_outline(x, y, radius):
    """Draw only the circumference of a circle (no fill)."""
    c = Circle(x, y, radius, fill=None, outline=current_fill, stroke=current_stroke)
    my_group.append(c)

def roudrect(x, y, w, h):
    """Approximate ellipse using RoundRect with large corner radius."""
    e = RoundRect(x, y, w, h, min(w, h)//2, fill=current_fill, outline=current_outline, stroke=current_stroke)
    my_group.append(e)

# -------------------------------
# EXAMPLE USAGE
# -------------------------------
"""
# Set fill color to red
color("red")
rectangle(10, 10, 60, 40)

# Change fill to green and outline to blue
color("green")
outline("blue")
stroke(3)
circle(120, 80, 30)

# Draw a triangle in yellow
color("yellow")
triangle(50, 200, 150, 200, 100, 120)

# Draw a line in white
color("white")
stroke(3)
line(0, 0, 319, 239)

# Draw roudrect in cyan
color("cyan")
roudrect(0, 100, 80, 40)

# Draw circle outline only
color("magenta")
circle_outline(250, 180, 30)

# Set fill color to green
color("green")

# Draw multiple lines starting at (x,0) going to (319,239)
for x in range(0, 320, 10):   # x will take values 0,10,20,...,310
    line(x, 0, 319, 239)
    
# Set fill color to red
color("red")

# Draw multiple lines starting at (319,0) going to (x,239)
for x in range(0, 320, 10):   # x will take values 0,10,20,...,310
    line(319, 0, x, 239)
"""

# -------------------------------
# CLEAR SCREEN
# -------------------------------
# To clear the screen we simply create a new group and assign it
my_group = displayio.Group()
display.root_group = my_group

# -------------------------------
# DRAW A HOUSE
# -------------------------------

# House base (rectangle)
color("yellow")
outline("black")
stroke(2)
rectangle(60, 120, 120, 80)   # x=60,y=120,width=120,height=80

# Roof (triangle)
color("red")
triangle(60, 120, 180, 120, 120, 60)

# Chimney (small rectangle on the roof)
color("brown")
rectangle(150, 80, 20, 40)

# Smoke from chimney (several circles going up)
color("gray")
for i in range(5):
    circle(160, 60 - i*15, 8)

# Door
color("brown")
rectangle(100, 150, 30, 50)

# Windows
color("cyan")
rectangle(70, 130, 20, 20)
rectangle(150, 130, 20, 20)

# -------------------------------
# ROOF TILES (using for loop)
# -------------------------------
color("black")
for x in range(65, 175, 10):   # horizontal spacing
    line(x, 120, 120, 65)      # lines from roof base to top

# -------------------------------
# PATHWAY
# -------------------------------
color("gray")
for i in range(6):
    rectangle(110 - i*5, 200 + i*7, 40 + i*10, 7)

# -------------------------------
# TREE
# -------------------------------
# Tree trunk
color("brown")
rectangle(220, 150, 20, 50)

# Tree crown (several green circles)
color("green")
circle(230, 140, 20)
circle(210, 150, 20)
circle(250, 150, 20)
circle(230, 120, 20)

# -------------------------------
# FENCE (wooden, in front)
# -------------------------------
color("brown")
for x in range(0, 320, 20):
    rectangle(x, 210, 10, 30)   # vertical posts

# Horizontal bars of the fence
rectangle(0, 215, 320, 5)
rectangle(0, 230, 320, 5)