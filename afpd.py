import re
import sys
import itertools
from afd import AFD

class AFPD:

	#Constructor
	def __init__(self, states=set({}), initial="", accepting=set({}), tapeAlphabet=set({}), stackAlphabet=set({}), transitions=set({}), file=None):
		self.states=states
		self.initial= initial
		self.accepting=accepting
		self.tapeAlphabet=tapeAlphabet
		self.stackAlphabet=stackAlphabet
		self.transitions=transitions
		self.stack=[]

		if(file!= None):

			lines = open(file).readlines()
			
			currently_reading = ""
			for line in lines:

				line = line.rstrip("\n")

				if(line.startswith("#")):
					currently_reading = line

				if (line!="" and line != currently_reading):
					automata_attribute = currently_reading.lstrip("#")

					if(currently_reading in ["#tapeAlphabet", "#stackAlphabet"]):
						if("-" in line):
							for char in range(ord(line[0]), ord(line[2])+1):
								getattr(self, automata_attribute).add(chr(char))

					elif(currently_reading == "#initial"):
						self.initial = line
					else:
						getattr(self, automata_attribute).add(line)

	@classmethod
	def from_file_name(cls, file):
		return cls(file=file)

	def get_transition_set(self):
		transition_list = {}
		for line in self.transitions:
			chars = re.split(':|>', line)
			transition_list[(chars[0], chars[1])] = (chars[2], chars[3], chars[4])

		return transition_list

	def process_string(self, string, details=False):

		print("Se procesa la cadena: ", string)
		current_string = "$" + string
		current_state = self.initial
		transition_list = self.get_transition_set()
		while(current_string[0] != None):
			char = current_string[0]
			pair = (current_state, char)
			transition = transition_list.get(pair)

			#La transicion quizas sea mejor como clase.
			#No imprime las descripciones instantaneas cuando la transicion no existe. Si la transicion existe pero comienza con lambda se quita el lambda
			if transition != None:
				if details: print("({}, {}, {})->".format(current_state, current_string.lstrip("$"), ''.join(self.stack)), end='')
			
			#Si se da el caso en el que la longitud sea 1 con $ pero ni el stack este vacio ni el estado sea de acpetacion se devuelve falso
			if(current_string[0] == "$" and len(current_string)==1):
				if(len(self.stack) == 0 and current_state in self.accepting):
					if details: print("({}, {})->".format(current_state, current_string), ''.join(self.stack), end='')
					self.stack = []
					if details: print("Accepted")
					return True
				elif(len(self.stack) != 0 or current_state not in self.accepting):
					self.stack = []
					print()
					if details: print("Rejected")
					return False
			
			#Si la transicion es lambda, es posible que no este definida una transicion, en tal caso se elimina $ y sigue
			if transition == None:
				current_string = current_string[1:]
			else:
				
				#Caso 1: Delta(q, a, lambda) = (q, b)
				#Se añade b sin importar el tope
				if(transition[0]=='$' and transition[2]!='$'):
					self.stack.append(transition[2])
				#Caso 2: Delta(q0, a, A) = (q1, B)
				#Se reemplaza A por B, el stack debe no estar vacio
				elif(len(self.stack) != 0 and transition[0]==self.stack[-1] and transition[2]!='$'):
					self.stack.pop()
					self.stack.append(transition[2])
				#Caso 3: Delta(q, a , A) = (q', lambda)
				#Se borra a del tope
				elif(transition[2]=='$'):
					if(len(self.stack)!=0):
						self.stack.pop()
					else:
						self.stack = []
						if details: print("Rejected")
						return False # no hay tope
				#Caso 4: No se altera la pila

				current_state = transition[1]
				current_string = current_string[1:]
				current_string = '$' + current_string  

		self.stack = []
		return False
	
	def process_string_with_details(self, string):
		return self.process_string(string, True)

	def find_cartesian_product_afd(self, afd):
		afpd_transitions = self.get_transition_set()
		afd_transitions = afd.get_transition_set()
		states_product = itertools.product(afd.states, afpd.states)
		initial_state_product = (afd.initial, afpd.initial)
		accepting_product = itertools.product(afd.accepting, afpd.accepting)

		if(afd.alphabet != afpd.tapeAlphabet):
			print("No tienen el mismo alfabeto")
			return False
		else:
			print("Mismo alfabeto")

		for pair in afpd_transitions :
			print(pair)
		for pair in afd_transitions :
			print(pair)

		return True

	def process_string_list(self, string_list, filename, printScreen=False):

		with open("{}.txt".format(filename), "w") as writer:
			sys.stdout = writer
			for string in string_list:
				self.process_string_with_details(string)
		if(printScreen==True):
			with open("{}.txt".format(filename), "r") as reader:
				sys.stdout = sys.__stdout__
				for line in reader.readlines():
					print(line)


	def __str__(self):
		attributes = ["states", "initial", "accepting", "tapeAlphabet", "stackAlphabet", "transitions"]
		to_string = ""
		for attribute in attributes:
			to_string = to_string + "\n#" + attribute
			for item in getattr(self, attribute):
				to_string = to_string + "\n" + item

		return to_string

		
if __name__ == "__main__":	
	if(len(sys.argv)<2):
		print("Error: Ingresa un archivo dfa de la siguiente forma")
		print("python dfa.py archivo.afpd archivo.pda")
	else:
		afpd = AFPD.from_file_name(file=sys.argv[1])
		while(True):
			cadena = input("Ingresa una cadena afpd\n")
			print(afpd.process_string_with_details(cadena))
	main()