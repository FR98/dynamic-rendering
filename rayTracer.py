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
1.  DR1
99. Exit
	""")

continuar = True

while continuar:
	menu()
	option = input('Ingresa un numero: ')

	if option == '1':
		examples.dr2()
	elif option == '99':
		continuar = False
		print('Bye Bye')
	else:
		print('Opcion incorrecta')
