import os
import pygame
import subprocess


# Khởi tạo Pygame
pygame.init()

# Tạo cửa sổ có kích thước 640x640 và đặt tọa độ (0, 0) ở giữa màn hình
screen = pygame.display.set_mode((640, 640))
screen_rect = screen.get_rect()
screen_rect.center = pygame.display.get_surface().get_rect().center

# Tải background
current_dir = os.path.dirname(os.path.abspath(__file__))
background_image = pygame.image.load(os.path.join(current_dir, 'D:\\Data_IT\\Code\\Sokoban_AI_Solver_Basic-main\\Assets\\start_back.png'))

# Tạo font cho các nút
font = pygame.font.Font(None, 60)

# Tạo các nút
player_mode_button = font.render('PLAYER SOLO', True, (255, 255, 255))
ai_mode_button = font.render('AI SOLVER', True, (255, 255, 255))
player_mode_rect = player_mode_button.get_rect()
ai_mode_rect = ai_mode_button.get_rect()

# Đặt vị trí các nút
player_mode_rect.midtop = (338, 267)
ai_mode_rect.midtop = (screen_rect.midtop[0]+20, screen_rect.midtop[1] + 425)

# Vòng lặp sự kiện
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra vị trí chuột khi nhấn
            mouse_pos = pygame.mouse.get_pos()
            if player_mode_rect.collidepoint(mouse_pos):
                pygame.quit()
                subprocess.run(["python", "D:\\Data_IT\\Code\\Sokoban_AI_Solver_Basic-main\\Sources\\human.py"])
                break
                # Thêm mã xử lý player_mode ở đây
            elif ai_mode_rect.collidepoint(mouse_pos):
                pygame.quit()
                subprocess.run(["python", "D:\\Data_IT\\Code\\Sokoban_AI_Solver_Basic-main\\Sources\\ai.py"])
                break
    # Vẽ nền và các nút lên màn hình
    screen.blit(background_image, (0, 0))
    screen.blit(player_mode_button, player_mode_rect)
    screen.blit(ai_mode_button, ai_mode_rect)
    pygame.display.flip()
    
pygame.quit()

