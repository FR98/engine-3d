"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from gl import Render
import utils.examples as examples

def menu():
	print("""
	Menu:
1.  Draw
2.  Draw Star
3.  Biplane OBJ
4.  Poligonos
5.  Load model con triangulos
6.  Dibujar ZBuffer
7.  Dibujar Modelo con textura
99.Exit
	""")

def menu_draw():
	print("""
	Menu:
1.  Set Window
2.  Set ViewPort
3.  Set colors
4.  Draw Pixel
5.  Draw Line
98.  Data
99.Finish
	""")

continuar = True

while continuar:
	menu()
	print("Tomar en cuenta que por ahora el window debe ser cuadrado")
	option = input('Ingresa un numero: ')

	if option == '1':
		finish = False
		render = Render.glInit(64, 64)

		while not finish:
			menu_draw()
			option2 = input('Ingresa un numero: ')

			if option2 == '1':
				w = int(input('Ingrese un ancho: '))
				h = int(input('Ingrese una altura: '))
				render.glCreateWindow(w, h)
			elif option2 == '2':
				x = int(input('Ingrese una posicion inicial x: '))
				y = int(input('Ingrese una posicion inicial y: '))
				w = int(input('Ingrese un ancho: '))
				h = int(input('Ingrese una altura: '))
				render.glViewPort(x, y, w, h)
			elif option2 == '3':
				window_color = input('Ingresa un color para el window: ')
				viewport_color = input('Ingresa un color para viewport: ')
				draw_color = input('Ingresa un color para dibujar: ')
			elif option2 == '4':
				# Pixel
				x = float(input('Ingrese una posicion x: '))
				y = float(input('Ingrese una posicion y: '))
				render.glVertex(x, y)
			elif option2 == '5':
				# Line
				x0 = float(input('Ingrese una posicion inicial x: '))
				y0 = float(input('Ingrese una posicion inicial y: '))
				x1 = float(input('Ingrese una posicion final x: '))
				y1 = float(input('Ingrese una posicion final y: '))
				render.glLine(x0, y0, x1, y1)
			elif option2 == '98':
				render.data()
			elif option2 == '99':
				render.glFinish()
				finish = True
			else:
				print('Opcion incorrecta')

	elif option == '2':
		w = int(input('Ingrese un ancho: '))
		h = int(input('Ingrese una altura: '))
		examples.star(w, h)
	elif option == '3':
		examples.biplane()
	elif option == '4':
		examples.poligonos()
	elif option == '5':
		examples.model_with_triangle()
	elif option == '6':
		examples.model_z_buffer()
	elif option == '7':
		examples.model_texture()
	elif option == '99':
		continuar = False
		print('Bye Bye')
	else:
		print('Opcion incorrecta')
