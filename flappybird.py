import pygame, sys, time
from pygame.locals import *
from clases import *
from colisiones import *

#Variables globales
ANCHO, ALTO = (500, 650)
altsuelo = 550

def Reiniciar (jugador) :

	for lista in jugador.listaTuberias :
		jugador.listaTuberias.clear()
		jugador.listaFranjas.clear()
		jugador.listaNubes.clear()

	jugador.SumarTuberia()
	jugador.SumarFranja(0, altsuelo)
	jugador.SumarNube()

	jugador.movy = 0
	jugador.rect.center = jugador.posIN
	jugador.puntos = 0
	jugador.saltar()

	jugador.Color()

	return jugador

def FlappyBird () :

	ventana = pygame.display.set_mode((ANCHO, ALTO))
	pygame.display.set_caption("Flappy Bird")

	pygame.display.init()
	pygame.display.update()
	pygame.font.init()

	Fondo = Color(143,242,245)
	ColSuelo = Color(137, 120, 67)

	pygame.mixer.init()

	SonidoPremio = pygame.mixer.Sound("Sonidos/Premio.wav")
	SonidoMuerte = pygame.mixer.Sound("Sonidos/Muerte.wav")
	SonidoAleteo = pygame.mixer.Sound("Sonidos/Aleteo.wav")

	status = 0

	fuente = pygame.font.SysFont("impact", 70)

	jugador = Player("Imagenes/Bird1.png")
	Suelo = pygame.Rect((0,altsuelo), (ANCHO, ALTO - altsuelo))
	Edific = pygame.image.load("Imagenes/Edificios.png")
	Edificios = Edific.get_rect()
	Edificios.left = 0
	Edificios.bottom = ALTO - 100
	jugador.SumarTuberia()
	jugador.SumarFranja(0,altsuelo)
	jugador.SumarNube()
	mano = pygame.image.load("Imagenes/Mano.png")
	man = mano.get_rect()
	man.center = (ANCHO / 2, ALTO / 3)
	play = Boton("Imagenes/Jugar.png", (ANCHO / 2, ALTO / 3 + 40))
	exit = Boton("Imagenes/Salir.png", (ANCHO / 2, ALTO / 2))

	jugador.Vida = False

	Fin = False
	reloj = pygame.time.Clock()

	while not Fin :

		reloj.tick(20)

		tiempo = int(pygame.time.get_ticks() / 1000)

		for event in pygame.event.get() :
			type = event.type
			if type == pygame.QUIT :
				Fin = True
			if type == pygame.MOUSEBUTTONDOWN :
				if event.button == 1 :
					if jugador.Vida :
						jugador.saltar()
						SonidoAleteo.play()
					if status == 0 :
						status = 1
						jugador.Vida = True
						jugador.movy = 0
						jugador.saltar()
					elif status == 2 :
						if play.pulsar(pygame.mouse.get_pos()) :
							status = 0
							jugador = Reiniciar(jugador)
						if exit.pulsar(pygame.mouse.get_pos()) :
							Fin = True

		#Actualizar
		if status == 1 :

			jugador.caer()
			if len(jugador.listaTuberias) > 0 :
				for lista in jugador.listaTuberias :
					lista.mover(jugador.velocidad)
			if len(jugador.listaFranjas) > 0 :
				for lista in jugador.listaFranjas :
					lista.mover(jugador.velocidad)
			if len(jugador.listaNubes) > 0 :
				for lista in jugador.listaNubes :
					lista.mover(jugador.velocidadNubes) 

		elif status == 0 :

			if len(jugador.listaFranjas) > 0 :
				for lista in jugador.listaFranjas :
					lista.mover(jugador.velocidad)

			jugador.anim(tiempo)

		#dibujar
		ventana.fill(Fondo)
		ventana.blit(Edific, Edificios)
		if len(jugador.listaNubes) > 0 :
			for lista in jugador.listaNubes :
				lista.dibujar(ventana)
		if len(jugador.listaTuberias) > 0 :
			for lista in jugador.listaTuberias :
				lista.dibujar(ventana)
		pygame.draw.rect(ventana, ColSuelo, Suelo)
		if len(jugador.listaFranjas) > 0 :
			for lista in jugador.listaFranjas :
				lista.dibujar(ventana)
		jugador.dibujar(ventana)
		if status == 0 :
			ventana.blit(mano, man)
		if status == 2 :
			play.dibujar(ventana)
			exit.dibujar(ventana)
			pygame.draw.line(ventana, Color(240,188,16), (50,50), (ANCHO - 50, 50), 5)
			pygame.draw.line(ventana, Color(240,188,16), (50,400), (ANCHO - 50, 400), 5)
			pygame.draw.line(ventana, Color(240,188,16), (50,50), (50, 400), 5)
			pygame.draw.line(ventana, Color(240,188,16), (ANCHO - 50, 50), (ANCHO - 50, 400), 5)
		if status == 1 or status == 2 :
			puntos = str(jugador.puntos)
			ventana.blit(fuente.render(puntos, False, (240, 188, 16)), (ANCHO / 2 - 25, ALTO / 8))


		pygame.display.update()

		if status == 1 :

			if COL_Imagen_Recuadro(jugador.img, jugador.pixel, jugador.rect, Suelo) :
				jugador.Vida = False
				status = 2
				SonidoMuerte.play()
				time.sleep(0.2)
			if len(jugador.listaTuberias) > 0 :
				for lista in jugador.listaTuberias :
					if COL_Imagen_Imagen(jugador.img, jugador.pixel, jugador.rect, lista.img, lista.pixel, lista.rect) :
						jugador.Vida = False
						status = 2
						SonidoMuerte.play()
						time.sleep(0.2)
					if jugador.rect.right > lista.rect.left and jugador.rect.left < lista.rect.left :
						if jugador.rect.bottom <= 0 :
							jugador.Vida = False 
							status = 2
							SonidoMuerte.play()
							time.sleep(0.2)
			if len(jugador.listaTuberias) > 0 :
				if jugador.listaTuberias[len(jugador.listaTuberias) - 1].rect.centerx <= jugador.distancia :
					jugador.SumarTuberia()
				for lista in jugador.listaTuberias :
					if lista.rect.right < 0 :
						jugador.listaTuberias.remove(lista)
					if lista.rect.right <= jugador.rect.left :
						if not lista.pasado :
							lista.pasado = True
							jugador.puntos += 1
							SonidoPremio.play()
			if len(jugador.listaFranjas) > 0 :
				for lista in jugador.listaFranjas :
					if not lista.remplazado :
						if lista.rect.right < ANCHO + 100 :
							lista.remplazado = True
							jugador.SumarFranja(lista.rect.right, altsuelo)
					if lista.rect.right < -100 :
						jugador.listaFranjas.remove(lista)
			if len(jugador.listaNubes) > 0 :
				if jugador.listaNubes[len(jugador.listaNubes) - 1].rect.centerx <= jugador.distanciaNubes :
					jugador.SumarNube()
				for lista in jugador.listaNubes :
					if lista.rect.right < 0 :
						jugador.listaNubes.remove(lista)

		elif status == 0 :

			if len(jugador.listaFranjas) > 0 :
				for lista in jugador.listaFranjas :
					if not lista.remplazado :
						if lista.rect.right < ANCHO + 100 :
							lista.remplazado = True
							jugador.SumarFranja(lista.rect.right, altsuelo)
					if lista.rect.right < -100 :
						jugador.listaFranjas.remove(lista)

if __name__ == '__main__' :
	FlappyBird()
	pygame.quit()
	sys.exit()