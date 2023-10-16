import pygame
import sys
import numpy as np
import tensorflow as tf
import cv2
from keras.preprocessing import image
class Rect:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

def menu():
	#bảng vẽ
	pygame.draw.rect(screen, board.color, (board.x, board.y, board.w, board.h))
	#kết quả
	result = font.render(f"Prediction = {pred}", True, (20, 20, 20))
	screen.blit(result, (550, 110))
	#nút dự đoán
	pygame.draw.rect(screen, button.color, (605 - 25, 310, pred_bt_pos[2] + 50, pred_bt_pos[3]))
	screen.blit(pred_bt_text, (605, 310))
	
	#vẽ nút xoá
	pygame.draw.rect(screen, button.color, (605 - 25, 410, clear_text_pos[2] + 50, clear_text_pos[3]))
	screen.blit(clear, (605, 410))
	
	#vẽ toạ độ chuột
	mouse_x, mouse_y = pygame.mouse.get_pos()
	if 15 < mouse_x < 515 and 15 < mouse_y < 590:
		text_mouse = font_mouse.render(f"({mouse_x}, {mouse_y})", True, (255,255,255))
		screen.blit(text_mouse, (mouse_x+15, mouse_y-5))

def draw_painting(paints):
	for i in range(len(paints)):
		pygame.draw.circle(screen, (255,255,255), paints[i], 10)

def result():
	color_image = cv2.imread('screenshot.png')
	gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
	resized_image = cv2.resize(gray_image, (28, 28))
	img = image.img_to_array(resized_image)
	img = np.expand_dims(img, axis=0)
	img = img / 255
	model = tf.keras.models.load_model(r"CNN.h5")
	predictions = model.predict(img)
	predicted_class = np.argmax(predictions, axis=1)
	return predicted_class[0]

pygame.init()
running = True
w, h = 850, 530
screen = pygame.display.set_mode((w, h))
black = (255,255,255)
background_color = (230, 190, 85)
font_mouse = pygame.font.Font(None, 18)
font = pygame.font.Font(None, 50)
pred_bt_text = font.render("Predict", True, black)
pred_bt_pos = pred_bt_text.get_rect()

clear = font.render("Clear", True, black)
clear_text_pos = clear.get_rect()

board = Rect(15,15,500,500,(30, 30, 30))
button = Rect(520,300,275,50,(30, 30, 30))
pred_board = Rect(530,15,250,250,(30, 30, 30))
capture = pygame.Rect(15, 15, 500, 500)
pred = "Nan"
painting = []
while running:
	pygame.time.Clock().tick(380)
	screen.fill(background_color)
	menu()
	mouse = pygame.mouse.get_pos()
	clicked = pygame.mouse.get_pressed()[0]
	
	if 15 < mouse[0] < 515 and 15 < mouse[1] < 515 and clicked:
		painting.append(mouse)
	draw_painting(painting)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if 605 - 25 < mouse[0] < 605 - 25 + pred_bt_pos[2] and 310 < mouse[1] < 310 + pred_bt_pos[3]:
					sub = screen.subsurface(capture)
					pygame.image.save(sub, 'screenshot.png')
					if len(painting) == 0:
						pred = "Nan"
					else:
						pred = result()
				if 605 - 25 < mouse[0] < 605 - 25 + pred_bt_pos[2] and 410 < mouse[1] < 410 + pred_bt_pos[3]:
					painting = []
					pred = "Nan"
	# Cập nhật màn hình
	pygame.display.flip()