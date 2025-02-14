from collections import deque
import random
import pygame

class Maze:
    def __init__(self, width_blocks, height_blocks, block_size):
        self.width_blocks = width_blocks
        self.height_blocks = height_blocks
        self.block_size = block_size
        self.maze = generate_maze(width_blocks, height_blocks)

    def is_wall(self, x, y):
        return self.maze[y][x] == 1  # 1は壁、0は通路

    def draw(self, screen):
        """迷路の壁を描画する"""
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 1:  # 1は壁
                    pygame.draw.rect(
                        screen, (0, 0, 255),  # 壁を青色で描画
                        (x * self.block_size, y * self.block_size, self.block_size, self.block_size)
                    )

def generate_maze(width, height):
    """深さ優先探索で迷路を生成"""
    maze = [[1 for _ in range(width)] for _ in range(height)]  # 初期状態は壁
    stack = [(1, 1)]  # 初期位置（1,1）からスタート
    maze[1][1] = 0  # スタート位置は通路

    while stack:
        x, y = stack[-1]
        neighbors = []

        for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == 1:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

def bfs(maze, start, goal, block_size):
    queue = deque([start])
    visited = set()
    came_from = {}
    came_from[start] = None

    while queue:
        current = queue.popleft()

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        for dx, dy in [(0, -block_size), (0, block_size), (-block_size, 0), (block_size, 0)]:
            neighbor = (x + dx, y + dy)
            if neighbor not in visited and not maze.is_wall(neighbor[0] // block_size, neighbor[1] // block_size):
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current

    return None
