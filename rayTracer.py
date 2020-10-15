"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

import utils.examples as examples

def menu():
	print("""
	Menu:
1.  DR
2.  Proyecto
99. Exit
	""")

continuar = True

while continuar:
	menu()
	option = input('Ingresa un numero: ')

	if option == '1':
		examples.dr()
	elif option == '2':
		examples.proyecto()
	elif option == '99':
		continuar = False
		print('Bye Bye')
	else:
		print('Opcion incorrecta')
