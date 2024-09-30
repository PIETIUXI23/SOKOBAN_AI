import subprocess
import numpy as np
import os
from colorama import Fore
from colorama import Style
from copy import deepcopy
import pygame
from pygame.constants import KEYDOWN
from support_function import *

''' TIME OUT FOR ALL ALGORITHM : 30 MIN ~ 1800 SECONDS '''
TIME_OUT = 1800
''' GET THE TESTCASES AND CHECKPOINTS PATH FOLDERS '''
current_dir = os.path.dirname(os.path.abspath(__file__))
path_board = os.path.join(current_dir, '..', 'Testcases')
path_checkpoint = os.path.join(current_dir, '..', 'Checkpoints')

''' TRAVERSE TESTCASE FILES AND RETURN A SET OF BOARD '''
def get_boards():
    os.chdir(path_board)
    list_boards = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_board}/{file}"
            board = get_board(file_path)
            # print(file)
            list_boards.append(board)
    return list_boards

''' TRAVERSE CHECKPOINT FILES AND RETURN A SET OF CHECKPOINT '''
def get_check_points():
    os.chdir(path_checkpoint)
    list_check_point = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_checkpoint}/{file}"
            check_point = get_pair(file_path)
            list_check_point.append(check_point)
    return list_check_point

''' FORMAT THE INPUT TESTCASE TXT FILE '''
def format_row(row):
    for i in range(len(row)):
        if row[i] == '1':
            row[i] = '#'
        elif row[i] == 'p':
            row[i] = '@'
        elif row[i] == 'b':
            row[i] = '$'
        elif row[i] == 'c':
            row[i] = '%'

''' FORMAT THE INPUT CHECKPOINT TXT FILE '''
def format_check_points(check_points):
    result = []
    for check_point in check_points:
        result.append((check_point[0], check_point[1]))
    return result

''' READ A SINGLE TESTCASE TXT FILE '''
def get_board(path):
    result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
    for row in result:
        format_row(row)
    return result

''' READ A SINGLE CHECKPOINT TXT FILE '''
def get_pair(path):
    result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
    return result

'''
//========================//
//      DECLARE AND       //
//  INITIALIZE MAPS AND   //
//      CHECK POINTS      //
//========================//
'''
maps = get_boards()
check_points = get_check_points()


'''
//========================//
//         PYGAME         //
//     INITIALIZATIONS    //
//                        //
//========================//
'''
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Sokoban')
clock = pygame.time.Clock()
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
'''
GET SOME ASSETS
'''
assets_path = os.getcwd() + "\\..\\Assets"
os.chdir(assets_path)
player = pygame.image.load(os.getcwd() + '\\player.png')
wall = pygame.image.load(os.getcwd() + '\\wall.png')
box = pygame.image.load(os.getcwd() + '\\box.png')
point = pygame.image.load(os.getcwd() + '\\point.png')
space = pygame.image.load(os.getcwd() + '\\space.png')
arrow_left = pygame.image.load(os.getcwd() + '\\arrow_left.png')
arrow_right = pygame.image.load(os.getcwd() + '\\arrow_right.png')
init_background = pygame.image.load(os.getcwd() + '\\init_background.png')
loading_background = pygame.image.load(os.getcwd() + '\\loading_background.png')
notfound_background = pygame.image.load(os.getcwd() + '\\notfound_background.png')
found_background = pygame.image.load(os.getcwd() + '\\found_background.png')

# Vẽ bàn cờ lên màn hình
def renderMap(board):
    width = len(board[0])
    height = len(board)
    indent = (640 - width * 32) / 2.0
    for i in range(height):
        for j in range(width):
            screen.blit(space, (j * 32 + indent, i * 32 + 250))
            if board[i][j] == '#':
                screen.blit(wall, (j * 32 + indent, i * 32 + 250))
            if board[i][j] == '$':
                screen.blit(box, (j * 32 + indent, i * 32 + 250))
            if board[i][j] == '%':
                screen.blit(point, (j * 32 + indent, i * 32 + 250))
            if board[i][j] == '@':
                screen.blit(player, (j * 32 + indent, i * 32 + 250))

# Khởi tạo biến cho trạng thái trò chơi và số bàn cờ
mapNumber = 0
sceneState = "init"

def sokoban():
    running = True
    global mapNumber
    global sceneState
    global check_points

    while running:
        if sceneState == "init":
            screen.blit(init_background, (0, 0))
            current_map = deepcopy(maps[mapNumber])
            player_pos = find_position_player(current_map)
            check_points = format_check_points(get_check_points()[mapNumber])
            initGame(current_map)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if mapNumber < len(maps) - 1:
                            mapNumber += 1
                            current_map = deepcopy(maps[mapNumber])
                            player_pos = find_position_player(current_map)
                            check_points = format_check_points(get_check_points()[mapNumber])
                            initGame(current_map)
                    if event.key == pygame.K_LEFT:
                        if mapNumber > 0:
                            mapNumber -= 1
                            current_map = deepcopy(maps[mapNumber])
                            player_pos = find_position_player(current_map)
                            check_points = format_check_points(get_check_points()[mapNumber])
                            initGame(current_map)
                    if event.key == pygame.K_RETURN:
                        sceneState = "playing"
                        break

            pygame.display.flip()

        elif sceneState == "playing":
            screen.blit(found_background, (0, 0))
            renderMap(current_map)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    player_pos = find_position_player(current_map)
                    possible_moves = get_next_pos(current_map, player_pos)
                    new_pos = player_pos

                    if event.key == pygame.K_UP:
                        if (player_pos[0] - 1, player_pos[1]) in possible_moves and current_map[player_pos[0] - 1][player_pos[1]] != '#':
                            new_pos = (player_pos[0] - 1, player_pos[1])
                    elif event.key == pygame.K_DOWN:
                        if (player_pos[0] + 1, player_pos[1]) in possible_moves and current_map[player_pos[0] + 1][player_pos[1]] != '#':
                            new_pos = (player_pos[0] + 1, player_pos[1])
                    elif event.key == pygame.K_LEFT:
                        if (player_pos[0], player_pos[1] - 1) in possible_moves and current_map[player_pos[0]][player_pos[1] - 1] != '#':
                            new_pos = (player_pos[0], player_pos[1] - 1)
                    elif event.key == pygame.K_RIGHT:
                        if (player_pos[0], player_pos[1] + 1) in possible_moves and current_map[player_pos[0]][player_pos[1] + 1] != '#':
                            new_pos = (player_pos[0], player_pos[1] + 1)

                    if new_pos != player_pos:
                        new_board = move(current_map, new_pos, player_pos, check_points)

                        if check_win(new_board, check_points):
                            # Xử lý trạng thái kết thúc (chiến thắng)
                            sceneState = "win"
                            win_board = new_board
                        else:
                            current_map = new_board
                            renderMap(current_map)

            pygame.display.flip()

        elif sceneState == "win":
            screen.blit(found_background, (0, 0))

            font_1 = pygame.font.Font('D:\\Data_IT\\Code\\Sokoban_AI_Solver_Basic-main\\Assets\\gameFont.ttf', 30)
            text_1 = font_1.render('Congratulations! You won!', True, WHITE)
            text_rect_1 = text_1.get_rect(center=(320, 100))
            screen.blit(text_1, text_rect_1)

            font_2 = pygame.font.Font('D:\\Data_IT\\Code\\Sokoban_AI_Solver_Basic-main\\Assets\\gameFont.ttf', 20)
            text_2 = font_2.render('Press Enter to continue.', True, WHITE)
            text_rect_2 = text_2.get_rect(center=(320, 600))
            screen.blit(text_2, text_rect_2)

            renderMap(win_board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        sceneState = "init"
                        mapNumber = 0

            pygame.display.flip()

def initGame(map):
    titleSize = pygame.font.Font('D:\\Data_IT\\Code\\Sokoban_AI_Solver_Basic-main\\Assets\\gameFont.ttf', 60)
    titleText = titleSize.render('Among-koban', True, WHITE)
    titleRect = titleText.get_rect(center=(320, 80))
    screen.blit(titleText, titleRect)

    desSize = pygame.font.Font('D:\\Data_IT\\Code\\Sokoban_AI_Solver_Basic-main\\Assets\\gameFont.ttf', 20)
    desText = desSize.render('Now, select your map!!!', True, WHITE)
    desRect = desText.get_rect(center=(320, 140))
    screen.blit(desText, desRect)

    mapSize = pygame.font.Font('D:\\Data_IT\\Code\\Sokoban_AI_Solver_Basic-main\\Assets\\gameFont.ttf', 30)
    mapText = mapSize.render("Lv." + str(mapNumber + 1), True, WHITE)
    mapRect = mapText.get_rect(center=(320, 200))
    screen.blit(mapText, mapRect)

    screen.blit(arrow_left, (246, 188))
    screen.blit(arrow_right, (370, 188))

    renderMap(map)

def main():
    sokoban()

if __name__ == "__main__":
    main()
    pygame.quit()
    subprocess.run(["python", "D:\\Data_IT\\Code\\Sokoban_AI_Solver_Basic-main\\Sources\\main.py"])
