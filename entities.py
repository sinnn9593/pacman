import pygame
import random
import time
from utils import bfs, Maze  # Mazeクラスをインポート


YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


# 画像のロード
PACMAN_IMAGE = pygame.image.load('images/pac.png')
GHOST_IMAGE = {
    "red": pygame.image.load('images/red-ghost1.png'),
    "blue": pygame.image.load('images/blue-ghost1.png'),
    "pink": pygame.image.load('images/pink-ghost1.png'),
    "orange": pygame.image.load('images/orange-ghost1.png')
}


class PacMan:
    def __init__(self, x, y, block_size):
        self.x = x
        self.y = y
        self.block_size = block_size
        self.x_change = 0
        self.y_change = 0

        #画像
        # 画像をスケーリング
        self.image = pygame.image.load('images/pac.png')
        self.image = pygame.transform.scale(self.image,(self.block_size,self.block_size))
        self.original_image = self.image  # 元の画像を保持


    @property
    def position(self):
        """現在の座標を (x, y) のタプルとして返す"""
        return (self.x, self.y)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change = -self.block_size
            self.y_change = 0
            self.image = pygame.transform.rotate(self.original_image,180)
        elif keys[pygame.K_RIGHT]:
            self.x_change = self.block_size
            self.y_change = 0
            self.image = self.original_image
        elif keys[pygame.K_UP]:
            self.x_change = 0
            self.y_change = -self.block_size
            self.image = pygame.transform.rotate(self.original_image,90)
        elif keys[pygame.K_DOWN]:
            self.x_change = 0
            self.y_change = self.block_size
            self.image = pygame.transform.rotate(self.original_image,270)

    def move(self, width, height, maze):
        next_x = self.x + self.x_change
        next_y = self.y + self.y_change
        # 壁の衝突判定
        if not maze.is_wall(next_x // self.block_size, next_y // self.block_size):
            self.x = next_x
            self.y = next_y

        # 画面外に出ないようにする
        self.x = max(0, min(self.x, width - self.block_size))
        self.y = max(0, min(self.y, height - self.block_size))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  # 画像を描画

    def eat_dot(self, dots):
        """ パックマンがドットを食べたかを判定し、食べた場合はドットをリストから削除 """
        for dot in dots[::-1]:  # リストを逆順で走査
            dot_x, dot_y = dot
            if abs(self.x - dot_x) < self.block_size // 2 and abs(self.y - dot_y) < self.block_size // 2:
                dots.remove(dot)
                return True  # ドットを1つ食べたらTrueを返す
        return False

class Ghost:
    def __init__(self, block_size, width, height, ai_type="chaser",color = "red",maze=None):
        self.x = block_size  # 初期位置を迷路内の適当な通路に設定（調整可）
        self.y = block_size
        self.block_size = block_size
        self.width = width
        self.height = height
        self.directions = ["LEFT", "RIGHT", "UP", "DOWN"]
        self.color =color  # 赤色のゴースト
        self.ai_type = ai_type
        self.maze = maze  # mazeを受け取る
        self.speed = 1
        self.last_bfs_time = time.time()  # ここで初期化
        self.last_move_time = pygame.time.get_ticks()  # 最後の移動時間
        self.move_interval = 900 # 移動間隔（ミリ秒

        self.image = pygame.transform.scale(GHOST_IMAGE[self.color], (self.block_size, self.block_size))


        # ランダムに迷路内の通路の位置を選ぶ
        self.x, self.y = self.random_position()

    @property
    def position(self):
        """現在の座標を (x, y) のタプルとして返す"""
        return (self.x, self.y)

    def random_position(self):
        """ランダムに通路の位置を選ぶ"""
        while True:
        # x, yはblock_sizeの倍数でランダムに生成
            x = random.randint(0, (self.width // self.block_size) - 1) * self.block_size
            y = random.randint(0, (self.height // self.block_size) - 1) * self.block_size

        # maze内の(x, y)が通路かどうかをチェック
            if not self.maze.is_wall(x // self.block_size, y // self.block_size):
                 return x, y

    def can_move(self, maze, next_x, next_y):
        """次の位置が迷路の通路であればTrueを返す"""
        col = next_x // self.block_size
        row = next_y // self.block_size
        if 0 <= row < len(maze.maze) and 0 <= col < len(maze.maze[0]):
            return maze.maze[row][col] == 0  # 0は通路、1は壁
        return False

    def move(self, pacman, maze):
        """ ゴーストが迷路内の通路だけをランダムに移動する """
        current_time = pygame.time.get_ticks()
        valid_directions = []

        if current_time - self.last_move_time >= self.move_interval:
            for direction in self.directions:
                next_x, next_y = self.x, self.y
                if direction == "LEFT":
                    next_x -= self.block_size
                elif direction == "RIGHT":
                    next_x += self.block_size
                elif direction == "UP":
                    next_y -= self.block_size
                elif direction == "DOWN":
                    next_y += self.block_size

            # 次の位置が通路なら移動可能方向に追加
                if self.can_move(maze, next_x, next_y):
                    valid_directions.append(direction)



        # 移動可能な方向があればランダムに1つ選んで移動
        if valid_directions:
            chosen_direction = random.choice(valid_directions)
            if chosen_direction == "LEFT":
                self.x -= self.block_size
            elif chosen_direction == "RIGHT":
                self.x += self.block_size
            elif chosen_direction == "UP":
                self.y -= self.block_size
            elif chosen_direction == "DOWN":
                self.y += self.block_size

        self.last_move_time = current_time

        """AIの種類に応じてゴーストを移動させる"""
        if self.ai_type == "chaser":
            self.chase(pacman, maze)
        elif self.ai_type == "random":
            self.random_move(maze)
        elif self.ai_type == "ambusher":
            self.ambush(pacman, maze)

    def chase(self, pacman, maze):
        current_time = time.time()
        """BFSでプレイヤーを追跡"""
        if current_time - self.last_bfs_time >= 10:  # 10秒ごとに再計算
            # パックマンとの距離が一定以内か確認
            distance = abs(self.x - pacman.x) + abs(self.y - pacman.y)
            if distance < 100:  # 距離が一定以内なら追跡
                start = (self.x, self.y)
                goal = (pacman.x, pacman.y)
                path = bfs(maze, start, goal, self.block_size)

                if path:  # 経路が見つかった場合
                    next_x, next_y = path[1]  # 次のステップを取得
                    self.x = next_x * self.block_size
                    self.y = next_y * self.block_size

            self.last_bfs_time = current_time

    def random_move(self, maze):
        """ランダムな方向に移動する"""
        directions = [(0, -self.block_size), (0, self.block_size), (-self.block_size, 0), (self.block_size, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            next_x = self.x + dx
            next_y = self.y + dy
            if not maze.is_wall(next_x // self.block_size, next_y // self.block_size):
                self.x, self.y = next_x, next_y
                break

    def ambush(self, pacman, maze):
        """プレイヤーの進行方向を予測してその先を目標地点とする"""
        target_x, target_y = pacman.x + pacman.x_change * 4, pacman.y + pacman.y_change * 4
        start = (self.x, self.y)
        goal = (target_x, target_y)
        path = bfs(maze, start, goal, self.block_size)

        if path:
            next_x, next_y = path[0]
            self.x, self.y = next_x, next_y

    #def draw(self, screen):
        """ ゴーストを描画 """
        #pygame.draw.rect(screen, self.color, (self.x, self.y, self.block_size, self.block_size))
    def draw(self, screen):
        """ ゴーストを画像で描画 """
        screen.blit(self.image, (self.x, self.y))



class Dots:
    def __init__(self, width, height, block_size):
        self.block_size = block_size
        self.positions = [[x * block_size, y * block_size] for x in range(width // block_size) for y in range(height // block_size) if random.random() > 0.1]  # ランダム配置

    def draw(self, screen):
        for dot in self.positions:
            pygame.draw.circle(screen, WHITE, (dot[0] + self.block_size // 2, dot[1] + self.block_size // 2), 3)
