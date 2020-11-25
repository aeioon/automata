'''Atributos:
Conjunto de Estados: Q
Estado Inicial: q0
Conjunto de Estados de Aceptación: F
Alfabeto de Cinta: Sigma
Alfabeto de Pila: Gamma
Función de Transición: Delta
Métodos:
Constructor(estados, estadoInicial, estadosAceptacion, alfabetoCinta, alfabetoPila,Delta)  de la clase para inicializar los atributos . Recuerde que en los autómatas creados, todos los estados deben ser accesibles.
Constructor(nombreArchivo): de la clase para inicializar los atributos a partir de un archivo cuya extensión es .dpda y cuyo formato está especificado en el archivo adjunto AFPD.pdf. Recuerde que, en los autómatas creados, todos los estados deben ser accesibles.
modificarPIla(pila,operación,parametro): Para ejecutar los cambios en la pila realizados por las transiciones, incluyendo los básicos así como la inserción/reemplazamiento de cadenas en el tope de la pila vistos en clase.
Booleano procesarCadena(cadena): procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por el autómata.
Booleano procesarCadenaConDetalles(cadena): realiza lo mismo que el método anterior aparte imprime los detalles del procesamiento con el formato que se indica en el archivo AFPD.pdf.
procesarListaCadenas(listaCadenas,nombreArchivo, imprimirPantalla): procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo; si este es inválido se asigna un nombre por defecto.  Además, todo esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla. Los campos deben estar separados por tabulación y son: 
cadena, 
procesamiento (con el formato del archivo AFPD.pdf).
‘yes’ o ‘no’ dependiendo de si la cadena es aceptada o no.
hallarProductoCartesianoConAFD(afd): debe calcular y retornar el producto cartesiano con un AFD dado como parámetro.
toString(): Representar el AFPD con el formato de los archivos de entrada de AFPD (AFPD.pdf) de manera que se pueda imprimir fácilmente.
Pruebas: Cree archivos con varios ejemplos para pruebas. Cree una clase donde pruebe e ilustre toda la funcionalidad de este módulo.
'''
import sys
import re
import pdb; pdb.set_trace()

class AFPD:

	def __init__(self, file):
		self.states=set({})
		self.initial=""
		self.accepting=set({})
		self.tapeAlphabet=set({})
		self.stackAlphabet=set({})
		self.transitions=set({})
		self.stack = []

		lines = open(file).readlines()
		
		currentReading = ""
		for line in lines:
			line = line.rstrip("\n")
			if(line.startswith("#")):
				print("Leyendo ", line);
				currentReading = line
			if (line!="" and line != currentReading):
				afdAtr = currentReading.lstrip("#")
				if(currentReading!="#initial"):
					getattr(self, afdAtr).add(line)
				else:
					self.initial = line

	def processString(self, string):
		print("Se procesa la cadena ", string)
		currentString = string
		currentState = self.initial
		for char in string:
			print(currentState, char, len(self.stack))
			transition = listT[(currentState, char)]
			print
			# Luego la veriicacion de temas de la pila
			# varias partes de aca pasan a modifyStack

			#Caso 1: Delta(q, a, lambda) = (q, b)
			#Se añade b sin importar el tope
			if(transition[0]=='$' and transition[2]!='$'):
				self.stack.append(transition[2])
				currentState = transition[1]
			#Caso 2: Delta(q0, a, A) = (q1, B)
			#Se reemplaza A por B, el stack debe no estar vacio
			elif(len(self.stack) != 0 and transition[0]==self.stack[-1] and transition[2]!='$'):
				self.stack.pop()
				self.stack.append(transition[2])
				currentState = transition[1]	
			#Caso 3: Delta(q, a , A) = (q', lambda)
			#Se borra a del tope
			elif(transition[2]=='$'):
				if(len(self.stack)!=0):
					self.stack.pop()
				else:
					return False # no hay tope
				currentState = transition[1]
			#Caso 4: No se altera la pila
			elif(transition[0] == transition[2] == '$'):
				currentState = transition[1]
			#Caso 5: Transicion lambda como en anb2n


		if((currentState in self.accepting) and len(self.stack) == 0):
			return True
		else:
			return False


afpd = AFPD(sys.argv[1])
transitions = afpd.transitions

def getTransitionsArr(afpd):
	TransitionList = {}
	for line in afpd.transitions:
		#Separa las transiciones en
		#estado origen, simbolo, simbolo reemplazado, estado final, simbolo que reemplaza
		chars = re.split(':|>', line)
		TransitionList[(chars[0], chars[1])] = (chars[2], chars[3], chars[4])

	return TransitionList

listT = getTransitionsArr(afpd)

while(True):
	cadena = input("Ingresa una cadena\n")
	print(afpd.processString(cadena))