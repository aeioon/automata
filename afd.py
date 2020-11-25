import re
import sys

class AFD:

	def __init__(self, file):
		self.alphabet=set({})
		self.states=set({})
		self.initial=""
		self.accepting=set({})
		self.transitions=set({})

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
			#Separa las transiciones en
			#estado inicial, simbolo, estado final
			#Posiblemente deba ser modelado como una clase propia.
			chars = re.split(':|>', line)
			transitionList[(chars[0], chars[1])] = (chars[2])

		return transitionList

	def processString(self, string):
		transitions = self.getTransitionSet()
		currentState = self.initial
		for char in string:
			if(char=="!"):
				currentState = currentState
			elif(char not in self.alphabet):
				print("No existe el simbolo en el alfabeto de la cinta")
				return False
			else:
				currentState = transitions[(currentState, char)]
		if(currentState in self.accepting):
			return True
		else:
			return False

	def processStringWithDetails(self, string):
		transitions = self.getTransitionSet()
		currentState = self.initial
		currentString = string
		for char in string:
			if(char=="!"):
				currentState = currentState
			elif(char not in self.alphabet):
				print("No existe el simbolo en el alfabeto de la cinta")
				return False
			else:
				print("({},{})->".format(currentState, currentString), end = '')
				currentState = transitions[(currentState, char)]
				currentString = currentString[1:]
			
		print("({},{})->".format(currentState, '$'), end = '')
		if(currentState in self.accepting):
			print("Accepted")
			return True
		else:
			print("Rejected")
			return False


	def processListStrings(self, stringList, fileName, printScreen):

		with open("{}.txt".format(fileName), "w") as writer:
			sys.stdout = writer
			for string in stringList:
				self.processStringWithDetails(string)
		if(printScreen==True):
			with open("{}.txt".format(fileName), "r") as reader:
				sys.stdout = sys.__stdout__
				for line in reader.readlines():
					print(line)
		

if(len(sys.argv)<2):
	print("Error: Ingresa un archivo dfa de la siguiente forma")
	print("python dfa.py archivo.dfa")
else:

	afd = AFD(file=sys.argv[1])
	
	while(True):
		cadena = input("Ingresa una cadena\n")
		print(afd.processStringWithDetails(cadena))
	''' Test processListStrings
	listaCadenas = ["bbbbb", "babab", "bbbbb", "aaaaa"]
	afd.processListStrings(listaCadenas, "archivo1", True)
	'''

