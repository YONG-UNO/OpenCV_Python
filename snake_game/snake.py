# # 贪吃蛇类
# from constants import *
#
#
# class Snake:
#     def __init__(self):
#         # 初始化蛇的位置和方向
#         self.segments = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
#         self.direction = RIGHT
#         self.next_direction = RIGHT
#         self.grow_pending = False
#
#     def update_direction(self):
#         """更新蛇的移动方向"""
#         self.direction = self.next_direction
#
#     def set_next_direction(self, new_direction):
#         """设置下一个移动方向（防止180度掉头）"""
#         # 确保不能直接反向移动
#         if (new_direction[0] != -self.direction[0] or
#                 new_direction[1] != -self.direction[1]):
#             self.next_direction = new_direction
#
#     def move(self):
#         """移动蛇的位置"""
#         head_x, head_y = self.segments[0]
#         new_head = (head_x + self.direction[0], head_y + self.direction[1])
#
#         # 在头部添加新的位置
#         self.segments.insert(0, new_head)
#
#         # 如果不需要生长，就移除尾部
#         if not self.grow_pending:
#             self.segments.pop()
#         else:
#             self.grow_pending = False
#
#     def grow(self):
#         """让蛇生长（吃到食物后调用）"""
#         self.grow_pending = True
#
#     def check_collision(self):
#         """检查是否发生碰撞（撞墙或撞自己）"""
#         head = self.segments[0]
#
#         # 检查是否撞墙
#         if (head[0] < 0 or head[0] >= GRID_WIDTH or
#                 head[1] < 0 or head[1] >= GRID_HEIGHT):
#             return True
#
#         # 检查是否撞到自己
#         if head in self.segments[1:]:
#             return True
#
#         return False
#
#     def get_head_position(self):
#         """返回蛇头位置"""
#         return self.segments[0]
#
#     def get_segments(self):
#         """返回所有身体片段"""
#         return self.segments

# SNAKE CLASS

from constants import *

class Snake:
    def __init__(self):
        # initialize the position and direction of the snake
        self.segments = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]   # initial body, head only, located in the center of the grid
        self.direction = RIGHT                                   # initial direction of movement
        self.grow_pending = False                               # grow pending(set to True after eating food)

    # direction control method
    '''
    1. avoid turn off result to die
    2. use set_next_direction to record next direction when user input new_direction, 
       come into force when use update_direction
    '''
    def update_direction(self):
        """update the movement direction of the snake(use before every movement)"""
        self.direction = self.next_direction

    def set_next_direction(self, new_direction):
        """set next direction(avoid 180 turn-off)"""
        if (new_direction[0] != -self.direction[0] or
            new_direction[1] != -self.direction[1]):
            self.next_direction = new_direction

    # logic of moving and growing
    def move(self):
        """move the snake (called once per game frame)"""
        head_x, head_y = self.segments[0] # capture the current position of the snake
        # compute new coordination of the snake-head (current-position + offset of direction)
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        self.segments.insert(0, new_head)   # inserting new position on head, snake moves forwards

        # if don't eat, remove the tail, keep the length the same, otherwise keep the tail, add one length
        if not self.grow_pending:
            self.segments.pop()
        else:
            self.grow_pending = False  # reset the grow_pending

    def gorw(self):
        """ called after eaten food, tagged the snake need to grow"""
        self.gorw_pending = True # keep the tail no change, to realize the length keep no change

    def check_collision(self):
        """check if crash itself or the wall"""
        head = self.segments[0] # capture the coordination of the snake-head

        # check crash wall:
        if(head[0] < 0 or head[0] >= GRID_WIDTH or
           head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True

        # check crash itself: whether the snake-head in itself(except the snake-head area)
        if head in self.segments[1:]:
            return True

        # if no crash the wall or itself
        return False

    # aiding method
    '''
    1. when Food class generate , will use get_segments() to capture the body-snake coordination to 
       avoid the food generate in the body-snake area
    2. to check the snake eaten the food, the get_head_position() will compare the coordination of snake-head to the food
    '''
    def get_head_position(self):
        """return the coordination of the snake-head (for external check if the food has been eaten)"""
        return self.segments[0]

    def get_segments(self):
        """return all coordination of the all body (for check if overlap when food generate)"""
