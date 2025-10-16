# GAME CONSTANTS SET

# screen set
'''
divide the window into a 20*15 grid,
and the position of the snake and food will
be calculated in "grid coordinates"
rather than pixel coordinates
'''
WIDTH, HEIGHT = 800, 600            # 游戏窗口的宽度/高度(piex)
GRID_SIZE = 40                      # 每个网格单元的大小(像素,即🐍身体,食物的单个方块的尺寸)
GRID_WIDTH = WIDTH // GRID_SIZE     # number of horizontal girds (800 // 40 = 20 column)
GRID_HEIGHT = HEIGHT // GRID_SIZE   # number of longitudinal grids (600 // 40 = 15 row)

# color definition (RGB, value 0-255)
'''
reference directly when drawing
elements in pygame
'''
BLACK = (0,0,0)         # for window backgrounds
WHITE = (255,255,255)   # for text, grid diagrams
RED   = (255,0,0)       # for food(eye-catching,separate form snake)
GREEN = (0,255,0)       # for snake body
BLUE  = (0,0,255)       # for buttons,titles and other auxiliary(fuzhu) elements
GRAY  = (40,40,40)      # for gird lines,borders

# direction constants (x/y-axis offset, step size in gird coordinates)
UP    =  (0,-1)   # (5,3) -> (5,2)
DOWN  =  (0,1)
LEFT  =  (-1,0)
RIGHT =  (1,0)

# game set
INITIAL_FPS             = 10   # initial game frame rate(refresh 10 times per second,or 10 squares per second,control the initial speed)
SCORE_PER_FOOD          = 10   # score for every food eaten
SPEED_INCREASE_INTERVAL = 50   # speed up every 50 point(such as 50 points after FPS from 10-11, more difficult)