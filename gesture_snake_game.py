import pygame
import random
import sys
from gesture_controller import GestureController


class SimpleSnakeGame:
    def __init__(self, gesture_controller=None):
        """
        简单贪吃蛇游戏
        Args:
            gesture_controller: 手势控制器（可选）
        """
        # 初始化pygame
        pygame.init()

        # 游戏设置
        self.WIDTH, self.HEIGHT = 800, 600
        self.GRID_SIZE = 20
        self.FPS = 10

        # 颜色定义
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.WHITE = (255, 255, 255)

        # 创建游戏窗口
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("手势控制贪吃蛇")
        self.clock = pygame.time.Clock()

        # 手势控制器
        self.gesture_controller = gesture_controller

        # 初始化游戏状态
        self.reset_game()

    def reset_game(self):
        """重置游戏状态"""
        # 蛇的初始位置和方向
        self.snake = [(self.WIDTH // 2, self.HEIGHT // 2)]
        self.direction = (self.GRID_SIZE, 0)  # 初始向右移动

        # 食物的初始位置
        self.food = self.generate_food()

        # 游戏状态
        self.score = 0
        self.game_over = False
        self.running = True

    def generate_food(self):
        """生成食物位置"""
        while True:
            food_pos = (
                random.randrange(0, self.WIDTH, self.GRID_SIZE),
                random.randrange(0, self.HEIGHT, self.GRID_SIZE)
            )
            # 确保食物不会出现在蛇身上
            if food_pos not in self.snake:
                return food_pos

    def handle_gesture_input(self):
        """处理手势输入"""
        if self.gesture_controller:
            # 持续更新手势检测
            success, img, command = self.gesture_controller.update()

            if success and command != 'unKnown':
                # 根据手势命令改变方向
                if command == 'up' and self.direction != (0, self.GRID_SIZE):
                    self.direction = (0, -self.GRID_SIZE)
                elif command == 'down' and self.direction != (0, -self.GRID_SIZE):
                    self.direction = (0, self.GRID_SIZE)
                elif command == 'left' and self.direction != (self.GRID_SIZE, 0):
                    self.direction = (-self.GRID_SIZE, 0)
                elif command == 'right' and self.direction != (-self.GRID_SIZE, 0):
                    self.direction = (self.GRID_SIZE, 0)

    def update(self):
        """更新游戏状态"""
        if self.game_over:
            return

        # 处理手势输入
        self.handle_gesture_input()

        # 移动蛇
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.snake.insert(0, new_head)

        # 检查是否吃到食物
        if self.snake[0] == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()  # 如果没有吃到食物，移除尾部

        # 检查碰撞
        head_x, head_y = self.snake[0]
        if (head_x < 0 or head_x >= self.WIDTH or
                head_y < 0 or head_y >= self.HEIGHT or
                self.snake[0] in self.snake[1:]):
            self.game_over = True

    def draw(self):
        """绘制游戏画面"""
        # 清屏
        self.screen.fill(self.BLACK)

        # 绘制食物
        pygame.draw.rect(self.screen, self.GREEN,
                         (self.food[0], self.food[1], self.GRID_SIZE, self.GRID_SIZE))

        # 绘制蛇
        for segment in self.snake:
            pygame.draw.rect(self.screen, self.RED,
                             (segment[0], segment[1], self.GRID_SIZE, self.GRID_SIZE))

        # 显示分数
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"得分: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))

        # 显示当前手势（如果有手势控制器）
        if self.gesture_controller:
            gesture_text = font.render(f"手势: {self.gesture_controller.current_command}",
                                       True, self.WHITE)
            self.screen.blit(gesture_text, (10, 50))

        # 游戏结束显示
        if self.game_over:
            game_over_font = pygame.font.SysFont(None, 72)
            game_over_text = game_over_font.render("游戏结束", True, self.RED)
            restart_text = font.render("按R键重新开始", True, self.WHITE)

            self.screen.blit(game_over_text,
                             (self.WIDTH // 2 - game_over_text.get_width() // 2,
                              self.HEIGHT // 2 - 50))
            self.screen.blit(restart_text,
                             (self.WIDTH // 2 - restart_text.get_width() // 2,
                              self.HEIGHT // 2 + 50))

    def run(self):
        """运行游戏主循环"""
        while self.running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    elif not self.game_over:
                        # 键盘控制（备用）
                        if event.key == pygame.K_UP and self.direction != (0, self.GRID_SIZE):
                            self.direction = (0, -self.GRID_SIZE)
                        elif event.key == pygame.K_DOWN and self.direction != (0, -self.GRID_SIZE):
                            self.direction = (0, self.GRID_SIZE)
                        elif event.key == pygame.K_LEFT and self.direction != (self.GRID_SIZE, 0):
                            self.direction = (-self.GRID_SIZE, 0)
                        elif event.key == pygame.K_RIGHT and self.direction != (-self.GRID_SIZE, 0):
                            self.direction = (self.GRID_SIZE, 0)

            # 更新游戏状态
            self.update()

            # 绘制游戏
            self.draw()

            # 更新显示
            pygame.display.flip()
            self.clock.tick(self.FPS)

        # 退出游戏
        pygame.quit()
        if self.gesture_controller:
            self.gesture_controller.release()
        sys.exit()


# 主函数
def main():
    # 创建手势控制器
    try:
        gesture_ctrl = GestureController(camera_index=2)
    except:
        gesture_ctrl = GestureController(camera_index=0)

    # 创建手势控制贪吃蛇游戏
    game = SimpleSnakeGame(gesture_controller=gesture_ctrl)

    # 运行游戏
    game.run()


if __name__ == "__main__":
    main()
