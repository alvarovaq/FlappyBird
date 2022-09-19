import pygame
from pygame.locals import *
from PIL import Image

def COL_Punto_Recuadro (posPunt, rect) :

	if posPunt[0] >= rect.left and posPunt[0] <= rect.right :
		if posPunt[1] >= rect.top and posPunt[1] <= rect.bottom :
			return True

	return False

def COL_Punto_Imagen (posPunt, img, pixel, rect) :

	size = img.size

	x = posPunt[0] - rect.left
	y = posPunt[1] - rect.top

	if x < size[0] and x >= 0 :
		if y < size[1] and y >= 0 :
			if pixel[x,y] != (0,0,0,0) :
				return True

	return False

def COL_Imagen_Recuadro (img, pixel, rect, rect2) :

	size = img.size

	for i in range(size[0]) :
		for j in range(size[1]) :
			if pixel[i,j] != (0,0,0,0) :
				if COL_Punto_Recuadro((i + rect.left, j + rect.top), rect2) :
					return True

	return False

def COL_Imagen_Imagen (img1, pixel1, rect1, img2, pixel2, rect2) :

	size = img1.size

	for i in range(size[0]) :
		for j in range(size[1]) :
			if pixel1[i,j] != (0,0,0,0) :
				if COL_Punto_Imagen((i + rect1.left, j + rect1.top), img2, pixel2, rect2) :
					return True

	return False



