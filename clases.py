import pygame, random
from pygame.locals import *
from PIL import Image
from colisiones import *

class Player (pygame.sprite.Sprite) :

	posIN = (125, 300)

	def __init__ (self, ruta) :

		pygame.sprite.Sprite.__init__(self)

		self.status = 0

		self.ruta = [["Imagenes/Bird1.png", "Imagenes/Bird12.png"], ["Imagenes/Bird2.png", "Imagenes/Bird22.png"], ["Imagenes/Bird3.png", "Imagenes/Bird32.png"], ["Imagenes/Bird4.png", "Imagenes/Bird42.png"]]
		self.Imag = []
		self.Img = []
		self.Pix = []

		for r in self.ruta :
			self.Imag.append([pygame.image.load(r[0]), pygame.image.load(r[1])])
			i = Image.open(r[0])
			j = Image.open(r[1])
			self.Img.append([i, j])
			self.Pix.append([i.load(), j.load()])


		self.color = random.randint(0,len(self.ruta) - 1)

		self.Imagen = self.Imag[self.color][self.status]
		self.img = self.Img[self.color][self.status]
		self.pixel = self.Pix[self.color][self.status]

		self.rect = self.Imagen.get_rect()
		self.rect.center = self.posIN

		self.movy = 0

		self.gravedad = 3
		self.salto = -30

		self.listaTuberias = []
		self.Vida = True
		self.puntos = 0

		self.listaFranjas = []
		self.listaNubes = []
		self.distanciaNubes = 250
		self.velocidadNubes = 1

		self.distancia = 250
		self.velocidad = 5

		self.dcambio = 1
		self.auxcambio = 0

	def SumarTuberia (self) :

		tub = Tuberias("Imagenes/Tuberias.png")
		self.listaTuberias.append(tub)

	def SumarFranja (self, left, top) :

		fran = Franja(left, top)
		self.listaFranjas.append(fran)

	def SumarNube (self) :

		nub = Nubes()
		self.listaNubes.append(nub)

	def saltar (self) :
		
		self.movy += self.salto
		self.rect.centery += self.movy

	def caer (self) :

		self.movy += self.gravedad
		self.rect.centery += self.movy

		if self.movy >= 0 :
			self.status = 0
		else :
			self.status = 1
		self.act()

	def Color (self) :

		self.color = random.randint(0,len(self.ruta) - 1)
		self.act()

	def anim (self, time) :

		if time != self.auxcambio :

			if time % self.dcambio == 0 :

				if self.status == 0 :
					self.status = 1
				else :
					self.status = 0

				self.act()

				self.auxcambio = time

	def CambiarStatus (self) :

		if self.status == 0 :
			self.status = 1
		else :
			self.status = 0

		self.act()

	def act (self) :

		self.Imagen = self.Imag[self.color][self.status]
		self.img = self.Img[self.color][self.status]
		self.pixel = self.Pix[self.color][self.status]

	def dibujar (self, ventana) :

		ventana.blit(self.Imagen, self.rect)

class Tuberias (pygame.sprite.Sprite) :

	def __init__ (self, ruta) :

		pygame.sprite.Sprite.__init__(self)

		self.ruta = ruta
		self.Imagen = pygame.image.load(self.ruta)

		self.img = Image.open(ruta)
		self.pixel = self.img.load()

		numero = random.randint(100, 450)

		self.rect = self.Imagen.get_rect()
		self.rect.centerx = 600
		self.rect.centery = numero

		self.pasado = False

	def mover (self, velocidad) :

		self.rect.centerx -= velocidad

	def dibujar (self, ventana) :

		ventana.blit(self.Imagen, self.rect)

class Franja (pygame.sprite.Sprite) :

	def __init__ (self, left, top) :

		pygame.sprite.Sprite.__init__(self)

		self.Imagen = pygame.image.load("Imagenes/Franja.png")

		self.rect = self.Imagen.get_rect()
		self.rect.left = left
		self.rect.top = top

		self.remplazado = False

	def mover (self, velocidad) :

		self.rect.left -= velocidad

	def dibujar (self, ventana) :

		ventana.blit(self.Imagen, self.rect)

class Nubes (pygame.sprite.Sprite) :

	def __init__ (self) :

		pygame.sprite.Sprite.__init__(self)

		ruta = ["Imagenes/nube1.png", "Imagenes/nube2.png", "Imagenes/nube3.png", "Imagenes/nube4.png"]

		numero = random.randint(0,len(ruta) - 1)

		self.Imagen = pygame.image.load(ruta[numero])

		numero = random.randint(75, 350)

		self.rect = self.Imagen.get_rect()
		self.rect.centerx = 600
		self.rect.centery = numero

	def mover (self, velocidad) :

		self.rect.left -= velocidad

	def dibujar (self, ventana) :

		ventana.blit(self.Imagen, self.rect)

class Boton (pygame.sprite.Sprite) :

	def __init__ (self, ruta, pos) :

		pygame.sprite.Sprite.__init__(self)

		self.Imagen = pygame.image.load(ruta)

		self.rect = self.Imagen.get_rect()
		self.rect.center = pos

	def pulsar (self, pos) :

		return COL_Punto_Recuadro(pos, self.rect)

	def dibujar (self, ventana) :

		ventana.blit(self.Imagen, self.rect)
