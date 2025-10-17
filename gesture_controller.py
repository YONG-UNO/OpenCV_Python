import cv2
import mediapipe as mp
import time
import math


class GestureController:
    def __init__(self, camera_index=0):
        """
        手势控制器类
        Args:
            camera_index: 摄像头索引，默认0
        """
        # 初始化摄像头
        self.cap = cv2.VideoCapture(camera_index)

        # 初始化MediaPipe手势识别
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,  # 只检测一只手
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

        # 手势命令映射
        self.command_dict = {
            'up': 'up',
            'down': 'down',
            'left': 'left',
            'right': 'right',
            'unKnown': 'unKnown'
        }

        # 手势状态
        self.current_command = 'unKnown'
        self.frame_count = 0
        self.command_history = []
        self.stable_frames = 5  # 连续5帧相同才认为手势稳定

        # 时间记录
        self.p_time = 0
        self.c_time = 0

        # 大拇指方向检测相关
        self.thumb_direction = 'none'

    def detect_thumb_direction(self, landmarks):
        """
        检测大拇指方向
        Args:
            landmarks: 手部关键点列表
        Returns:
            thumb_direction: 大拇指方向 ('up', 'down', 'left', 'right', 'none')
        """
        # 大拇指关键点索引
        thumb_tip = landmarks[4]  # 大拇指指尖
        thumb_ip = landmarks[3]  # 大拇指第二关节
        thumb_mcp = landmarks[2]  # 大拇指根部
        wrist = landmarks[0]  # 手腕

        # 计算大拇指向量
        thumb_vector = (thumb_tip.x - thumb_ip.x, thumb_tip.y - thumb_ip.y)

        # 计算手腕到手掌中心的向量（用于确定手掌方向）
        palm_vector = (landmarks[9].x - wrist.x, landmarks[9].y - wrist.y)

        # 计算大拇指与手掌的夹角
        dot_product = thumb_vector[0] * palm_vector[0] + thumb_vector[1] * palm_vector[1]
        thumb_magnitude = math.sqrt(thumb_vector[0] ** 2 + thumb_vector[1] ** 2)
        palm_magnitude = math.sqrt(palm_vector[0] ** 2 + palm_vector[1] ** 2)

        if thumb_magnitude == 0 or palm_magnitude == 0:
            return 'none'

        cos_angle = dot_product / (thumb_magnitude * palm_magnitude)
        angle = math.acos(max(min(cos_angle, 1), -1)) * 180 / math.pi

        # 根据夹角判断大拇指方向
        if angle < 45:
            return 'up' if thumb_vector[1] < 0 else 'down'
        else:
            return 'left' if thumb_vector[0] < 0 else 'right'

    def detect_finger_direction(self, landmarks):
        """
        检测手指伸展方向（基于距离手腕最远的手指）
        Args:
            landmarks: 手部关键点列表
        Returns:
            direction: 手指方向
        """
        wrist = landmarks[0]
        distances = {}

        # 检测各个指尖与手腕的距离
        finger_tips = {
            4: 'thumb',  # 大拇指
            8: 'index',  # 食指
            12: 'middle',  # 中指
            16: 'ring',  # 无名指
            20: 'pinky'  # 小指
        }

        for tip_id, finger_name in finger_tips.items():
            tip = landmarks[tip_id]
            distance = math.sqrt(
                (tip.x - wrist.x) ** 2 +
                (tip.y - wrist.y) ** 2 +
                (tip.z - wrist.z) ** 2
            )
            distances[finger_name] = distance

        # 找到距离最远的手指
        if distances:
            max_finger = max(distances, key=distances.get)
            if distances[max_finger] > 0.1:  # 阈值
                return max_finger
        return 'none'

    def get_gesture_command(self, landmarks):
        """
        综合手指伸展和大拇指方向获取手势命令
        Args:
            landmarks: 手部关键点列表
        Returns:
            command: 手势命令
        """
        # 检测大拇指方向
        thumb_dir = self.detect_thumb_direction(landmarks)

        # 检测手指伸展
        finger_dir = self.detect_finger_direction(landmarks)

        # 手势优先级：大拇指方向 > 手指伸展
        if thumb_dir != 'none':
            # 大拇指方向映射到命令
            if thumb_dir == 'up':
                return 'up'
            elif thumb_dir == 'down':
                return 'down'
            elif thumb_dir == 'left':
                return 'left'
            elif thumb_dir == 'right':
                return 'right'

        # 如果没有检测到大拇指方向，使用手指伸展
        if finger_dir != 'none':
            if finger_dir == 'index':
                return 'up'
            elif finger_dir == 'middle':
                return 'down'
            elif finger_dir == 'ring':
                return 'left'
            elif finger_dir == 'pinky':
                return 'right'
            elif finger_dir == 'thumb':
                return 'up'  # 大拇指伸展也认为是向上

        return 'unKnown'

    def update(self):
        """
        更新手势检测状态
        Returns:
            success: 是否成功读取帧
            img: 处理后的图像
            command: 当前手势命令
        """
        success, img = self.cap.read()
        if not success:
            return False, None, 'unKnown'

        # 转换颜色空间
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        command = 'unKnown'

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 绘制手部关键点和连线
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # 获取手势命令
                command = self.get_gesture_command(hand_landmarks.landmark)

                # 在图像上显示检测到的手势
                cv2.putText(img, f"Gesture: {command}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        # 计算并显示帧率
        self.c_time = time.time()
        fps = 1 / (self.c_time - self.p_time) if self.p_time > 0 else 0
        self.p_time = self.c_time

        cv2.putText(img, f"FPS: {int(fps)}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        # 手势稳定性检测
        self.frame_count += 1
        self.command_history.append(command)

        if self.frame_count >= self.stable_frames:
            # 检查最近几帧的手势是否一致
            if len(set(self.command_history)) == 1:  # 所有手势相同
                self.current_command = command
            else:
                self.current_command = 'unKnown'

            # 重置计数
            self.frame_count = 0
            self.command_history = []

        return True, img, self.current_command

    def get_command_code(self):
        """
        获取当前手势对应的命令代码
        Returns:
            command_code: 命令代码字符串
        """
        return self.command_dict.get(self.current_command, '-1')

    def release(self):
        """释放资源"""
        self.cap.release()
        cv2.destroyAllWindows()


# 手势控制贪吃蛇游戏
class GestureSnakeGame:
    def __init__(self, gesture_controller):
        """
        手势控制贪吃蛇游戏
        Args:
            gesture_controller: 手势控制器实例
        """
        self.gesture_controller = gesture_controller
        self.running = True

    def run(self):
        """运行手势控制演示"""
        print("手势控制贪吃蛇演示")
        print("手势说明:")
        print("- 大拇指向上: 向上移动")
        print("- 大拇指向下: 向下移动")
        print("- 大拇指向左: 向左移动")
        print("- 大拇指向右: 向右移动")
        print("- 或使用手指伸展控制方向")
        print("- 按Q键退出")

        while self.running:
            # 更新手势检测
            success, img, command = self.gesture_controller.update()

            if not success:
                break

            # 显示图像
            cv2.imshow("Gesture Control Snake", img)

            # 获取命令代码
            command_code = self.gesture_controller.get_command_code()
            print(f"当前命令: {command}, 代码: {command_code}")

            # 检查退出键
            key = cv2.waitKey(1)
            if key == ord('q') or key == 113:  # Q键或q键
                self.running = False

        # 释放资源
        self.gesture_controller.release()


# 使用示例
if __name__ == "__main__":
    # 创建手势控制器（如果摄像头2不可用，可以改为0）
    try:
        gesture_ctrl = GestureController(camera_index=0)
    except:
        gesture_ctrl = GestureController(camera_index=0)

    # 创建手势控制游戏
    game = GestureSnakeGame(gesture_ctrl)

    # 运行游戏
    game.run()