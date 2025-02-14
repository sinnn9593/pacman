import pygame
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pygame")

from entities import PacMan, Ghost, Dots
from utils import Maze

# ゲームの初期設定
pygame.init()

# 画面サイズや迷路の設定
WIDTH, HEIGHT = 600,800
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


# 迷路のインスタンスを作成
maze = Maze(WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE, BLOCK_SIZE)
# 迷路、プレイヤー、ゴースト、ドットの設定
pacman = PacMan(100, 100, BLOCK_SIZE)
ghosts = [Ghost(BLOCK_SIZE, WIDTH, HEIGHT, ai_type="chaser",color = "red",maze = maze),
          Ghost(BLOCK_SIZE, WIDTH, HEIGHT, ai_type="random",color = "blue",maze = maze),
          Ghost(BLOCK_SIZE, WIDTH, HEIGHT, ai_type="random",color = "pink",maze = maze),
          Ghost(BLOCK_SIZE, WIDTH, HEIGHT, ai_type="random",color = "pink",maze = maze),
          Ghost(BLOCK_SIZE, WIDTH, HEIGHT, ai_type="random",color = "red",maze = maze),
          Ghost(BLOCK_SIZE, WIDTH, HEIGHT, ai_type="random",color = "orange",maze = maze),]
dots = Dots(WIDTH, HEIGHT, BLOCK_SIZE)

# ゲームループ
running = True
while running:
    screen.fill((0, 0, 0))  # 画面を黒で塗りつぶし

    pacman.handle_keys()
    pacman.move(WIDTH, HEIGHT, maze)

    for ghost in ghosts:
        ghost.move(pacman, maze)

        # 衝突判定（Pac-ManとGhostの座標が重なった場合）
        if abs(pacman.x - ghost.x) < BLOCK_SIZE // 2 and abs(pacman.y - ghost.y) < BLOCK_SIZE // 2:
            print("Game Over!")  # ゲームオーバー処理（ここで終了処理を追加）
            running = False

    pacman.eat_dot(dots.positions)

    # 描画
    maze.draw(screen)
    dots.draw(screen)
    pacman.draw(screen)
    for ghost in ghosts:
        ghost.draw(screen)


    pygame.display.flip()  # 画面を更新

    # ゲーム終了処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(30)  # フレームレートを30に設定

pygame.quit()
