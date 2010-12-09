#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

filas = 14
columnas = 10
# Guarda el color de cada celda de la grilla (0 = vacío)
grilla = [[0 for i in range(columnas)] for j in range(filas)]
colores_max = 5

# Duplas con las coordenadas de cada celda que pertenece a la pieza actual
pieza = []
colorPieza = 0

x_actual = y_actual = 0
rotx = roty = 0

actual = None

def mover(dx,dy):
	global pieza, x_actual, y_actual
	# Me fijo que haya lugar para mover la pieza y que no se salga del tablero
	piezaNueva = []
	for (x,y) in pieza:
		if y+dy == filas or x+dx == columnas or y+dy < 0 or x+dx < 0 or \
			(x+dx,y+dy) not in pieza and grilla[y+dy][x+dx] != 0:
			return True
		piezaNueva.append((x+dx,y+dy))
	# La muevo
	for (x,y) in pieza:
		if (x,y) not in piezaNueva:
			grilla[y][x] = 0
	for (x,y) in piezaNueva:
		grilla[y][x] = colorPieza
	pieza = piezaNueva
	x_actual += dx
	y_actual += dy
	return False

def rotar():
	global pieza,grilla
	# Calculo el centro de la pieza
	cx = x_actual + 0.5 * rotx
	cy = y_actual + 0.5 * roty
	print cx, cy
	# La transformación es (x,y) = (cx-y+cy,cy+x-cx)
	# Me fijo que haya lugar para rotar la pieza y que no se salga del tablero
	piezaNueva = []
	for (x,y) in pieza:
		(nx,ny) = (int(cx-y+cy),int(cy+x-cx))
		if ny >= filas or nx >= columnas or ny < 0 or nx < 0 or \
			(nx,ny) not in pieza and grilla[ny][nx] != 0:
			print "no rota (",x,y,")->(",nx,ny,")"
			return True
		piezaNueva.append((nx,ny))
	# La muevo
	for (x,y) in pieza:
		if (x,y) not in piezaNueva:
			grilla[y][x] = 0
	for (x,y) in piezaNueva:
		grilla[y][x] = colorPieza
	pieza = piezaNueva
	return False

def cargarPiezas(archivo):
	piezas= [[]]
	centros = []
	# Las piezas están en un archivo de texto, separadas por lineas vacías
	# TODO: calcular un centro de rotación si el archivo no lo especifica
	f = open(archivo,'r')
	nueva = None
	for linea in f:
		if linea.isspace():
			# Una línea en blanco comienza una pieza nueva
			piezas.append([])
			continue
		if linea[0] == "(":
			# Coordenadas del centro de rotación
			tmp = linea[1:-2].split(",")
			centros.append((int(tmp[0]),int(tmp[1])))
		else:
			piezas[-1].append([(0,1)[c != " "] for c in linea.rstrip()])

	# Ahora me aseguro que las filas de cada pieza tengan largo uniforme
	for pieza in piezas:
		ancho = max([len(fila) for fila in pieza])
		for fila in pieza:
			fila.extend([0]*(ancho-len(fila)))
	return (piezas,centros)

def piezaNueva():
	from random import random
	global pieza, grilla, colorPieza, y_actual, x_actual, rotx, roty
	# Selecciono una forma al azar
	n = int(random()*len(formas))
	nueva = formas[n]
	(rotx,roty) = centros[n]
	ancho = max([len(fila) for fila in nueva ])
	pieza = []
	# Posición inicial
	y_actual = 0
	x_actual = dx = int(random()*(columnas-ancho))
	# Traduzco de la grilla que describe la pieza al array de coordenadas
	for (y,fila) in enumerate(nueva):
		for (x,celda) in enumerate(fila):
			if celda != 0:
				pieza.append((x+dx,y))
	colorPieza = int(random()*colores_max)+1
	for (x,y) in pieza:
		if grilla[y][x] != 0:
			# No hay lugar para la pieza, perdiste.
			return True
	for (x,y) in pieza:
		grilla[y][x] = colorPieza

def mostrarGrilla():
	for fila in grilla:
		for celda in fila:
			sys.stdout.write('{0:d}'.format(celda))
		print

if __name__ == "__main__":
	(formas,centros) = cargarPiezas("piezas.txt")
	piezaNueva()
	while 1:
		# Hago caer la pieza, si da true no pudo caer
		if mover(0,1):
			print "Se trabó"
			# La pieza no puede caer más. 
			# Me fijo si completó una fila y agrego una pieza nueva
			pieza = []
			# Me fijo qué filas falta completar
			incompletas = []
			for fila in grilla:
				if min(fila) == 0:
					incompletas.append(fila)
			ncompletas = filas-len(incompletas)
			if ncompletas > 0:
				print ncompletas,"filas completas"
			# Esas filas son las únicas que van a quedar, todas al fondo
			grilla[ncompletas:] = incompletas
			# Lo demás queda vacío
			grilla[:ncompletas] = [[0 for i in range(columnas)]
				for j in range(ncompletas)]
			if piezaNueva():
				print "Perdiste"
				break
		mostrarGrilla()
		print
		entrada = raw_input(">")
		if entrada == "q":
			break
		elif entrada == "a":
			mover(-1,0)
		elif entrada == "d":
			mover(1,0)
		elif entrada == "w":
			rotar()

