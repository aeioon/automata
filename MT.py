'''Clase MT para representar Máquinas de Turing en su Modelo Estándar: 

Atributos:
Conjunto de Estados: Q
Estado Inicial: q0
Conjunto de Estados de Aceptación: F
Alfabeto de Entrada: Sigma
Alfabeto de Cinta: Gamma
Función de Transición: delta
Cinta
Métodos:
Constructor(estados, estadoInicial, estadosAceptacion, alfabetoEntrada, alfabetoCinta,Delta)  de la clase para inicializar los atributos. Recuerde que en la MT creada, todos los estados deben ser accesibles.
Constructor(nombreArchivo): de la clase para inicializar los atributos a partir de un archivo cuya extensión es .tm y cuyo formato está especificado en el archivo adjunto MT.pdf. Recuerde que, en la MT creada, todos los estados deben ser accesibles.
Booleano procesarCadena(cadena): procesa la cadena y retorna verdadero si es aceptada y falso si es rechazada por la MT.
Booleano procesarCadenaConDetalles(cadena): realiza lo mismo que el método anterior aparte imprime los detalles del procesamiento con el formato que se indica en el archivo MT.pdf.
String procesarFunción(cadena): procesa la cadena y retorna la cadena que queda escrita sobre la cinta al final (última configuración instantánea).
procesarListaCadenas(listaCadenas,nombreArchivo, imprimirPantalla): procesa cada cadenas con detalles pero los resultados deben ser impresos en un archivo cuyo nombre es nombreArchivo; si este es inválido se asigna un nombre por defecto.  Además, todo esto debe ser impreso en pantalla de acuerdo al valor del Booleano imprimirPantalla. Los campos deben estar separados por tabulación y son: 
cadena, 
última configuración instantánea
‘yes’ o ‘no’ dependiendo de si la cadena es aceptada o no.
toString(): Representar la MT con el formato de los archivos de entrada de MT (MT.pdf) de manera que se pueda imprimir fácilmente.
Pruebas: Cree archivos con varios ejemplos para pruebas. Cree una clase donde pruebe e ilustre toda la funcionalidad de este módulo.
'''
import sys
import re
class MT():

	def __init__(self, file):
		
		self.states=set({})
		self.initial=""
		self.accepting=set({})
		self.inputAlphabet=set({})
		self.tapeAlphabet=set({})
		self.transitions = set({})

		lines = open(file).readlines()
		
		currentReading = ""
		for line in lines:
			line = line.rstrip("\n")
			if(line.startswith("#")):
				currentReading = line
			if (line!="" and line != currentReading):
				afdAtr = currentReading.lstrip("#")
				if(currentReading!="#initial"):
					getattr(self, afdAtr).add(line)
				else:
					self.initial = line

	def getTransitionSet(self):
		transitionList = {}
		for line in self.transitions:
			chars = re.split(':|\\?', line)
			transitionList[(chars[0], chars[1])] = (chars[2], chars[3], chars[4])
		return transitionList

	def displace(self, transition):
		if transition[2] == '<':
			return -1
		elif transition[2] == '>':
			return 1
		else:
			return 0

	def processString(self, string):
		transitions = self.getTransitionSet()
		tape = []
		currentState = self.initial
		tape.append(currentState)
		currentIndex = 0
		for char in string:
			tape.append(char)
		tape.append('!')
		print("Cadena ingresada: ", string)
		while(tape[currentIndex] != None and currentState not in self.accepting):	
			Pair = (tape[currentIndex], tape[currentIndex+1])
			if transitions.get(Pair) == None:
				#M se detiene en un estado que no es de aceptacion, 
				#lambda(q, s) no está definida
				print("La transicion Lambda", Pair," no existe")
				return False
			transition = transitions.get(Pair)
			nextIndex = currentIndex+self.displace(transition)
			tape[currentIndex+1]= transition[1]
			tape[currentIndex] = tape[nextIndex]
			tape[nextIndex] = transition[0]
			currentIndex = nextIndex
			currentState = tape[currentIndex]
			
		print("Aceptada")
		return True

	def processStringWithDetails(self, string):
		transitions = self.getTransitionSet()
		tape = []
		currentState = self.initial
		tape.append(currentState)
		currentIndex = 0
		for char in string:
			tape.append(char)
		tape.append('!')
		print("Cadena ingresada: ", string)
		while(tape[currentIndex] != None and currentState not in self.accepting):	
			print(''.join(tape), "->", end='')
			Pair = (tape[currentIndex], tape[currentIndex+1])
			if transitions.get(Pair) == None:
				#M se detiene en un estado que no es de aceptacion, 
				#lambda(q, s) no está definida
				print("La transicion Lambda", Pair," no existe")
				return False
			transition = transitions.get(Pair)
			nextIndex = currentIndex+self.displace(transition)
			tape[currentIndex+1]= transition[1]
			tape[currentIndex] = tape[nextIndex]
			tape[nextIndex] = transition[0]
			currentIndex = nextIndex
			currentState = tape[currentIndex]
			
		print("Aceptada")
		return True

	def processFunction(self, string):
		#Retorna ultima configuración instantanea
		transitions = self.getTransitionSet()
		tape = []
		currentState = self.initial
		tape.append(currentState)
		currentIndex = 0
		for char in string:
			tape.append(char)
		tape.append('!')
		print("Cadena ingresada: ", string)
		while(tape[currentIndex] != None and currentState not in self.accepting):	
			Pair = (tape[currentIndex], tape[currentIndex+1])
			if transitions.get(Pair) == None:
				#M se detiene en un estado que no es de aceptacion, 
				#lambda(q, s) no está definida
				print("La transicion Lambda", Pair," no existe")
				return lastString

			transition = transitions.get(Pair)
			nextIndex = currentIndex+self.displace(transition)
			tape[currentIndex+1]= transition[1]
			tape[currentIndex] = tape[nextIndex]
			tape[nextIndex] = transition[0]
			currentIndex = nextIndex
			currentState = tape[currentIndex]
			lastString = ''.join(tape)

		return lastString




if(len(sys.argv)<2):
	print("Error: Ingresa un archivo dfa de la siguiente forma")
	print("python TM.py archivo.tm")
else:

	mt = MT(file=sys.argv[1])

	while(True):
		cadena = input("Ingresa una cadena\n")
		print(mt.processStringWithDetails(cadena))



