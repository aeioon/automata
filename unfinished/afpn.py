import re
import sys
import itertools
import random
import pdb

class AFPN:

	def __init__(self, states=set({}), initial="", accepting=set({}), tapeAlphabet=set({}), stackAlphabet=set({}), transitions=set({}), file=None):
		self.states=states
		self.initial= initial
		self.accepting=accepting
		self.tapeAlphabet=tapeAlphabet
		self.stackAlphabet=stackAlphabet
		self.transitions=transitions
		self.stack = []
		self.aceptada = False;
		if(file!= None):

			lines = open(file).readlines()
			
			currentReading = ""
			for line in lines:
				line = line.rstrip("\n")
				if(line.startswith("#")):
					currentReading = line
				if (line!="" and line != currentReading):
					afpdAtr = currentReading.lstrip("#")
					if(currentReading!="#initial"):
						getattr(self, afpdAtr).add(line)
					else:
						self.initial = line

	@classmethod
	def from_file_name(cls, file):
		return cls(file=file)


	class Transition:
		def __init__(self, state, stack_symbol):
			self.state = state
			self.stack_symbol = stack_symbol

	#Definitivamente necesita su propia clase
	def get_transition_set(self):
		transition_list = {}
		for line in self.transitions:

			transition_set = re.split('>|;', line)
			conjunto_transiciones = transition_set[1:]
			pair_set = set({})
			temp_pair = re.split(':', transition_set[0])
			for element in conjunto_transiciones:
				temp_set = re.split(':', element)
				pair = (temp_set[0], temp_set[1])
				pair_set.add(pair)
			transition_list[(temp_pair[0], temp_pair[1], temp_pair[2])] = pair_set
		return transition_list

	def is_posible(self, char, state, top, transition):
		#transition es estado nuevo, simbolo de pila nuevo
		if(len(self.stack)==0 and transition[1]=='$' and char=='$'):
			return False
		else:
			return True

	def process_string(self, string, state, previous_string=None, previous_state=None, viewed=set({})):

		transition_list = self.get_transition_set()
		print(previous_string, previous_state)
		current_string = string
		current_state = state
		current_stack_top = "$" if len(self.stack)== 0 else self.stack[-1]
		if(len(current_string) == 0):
			if(state in self.accepting and len(self.stack)==0):
				return True
			else:
				current_char="$"
		if(len(current_string) != 0):
			current_char = current_string[0]

		
		#Pair sin lambda
		pair = (current_state, current_char, current_stack_top)
		print(pair, "no l")
		#Transiciones sin lambda
		current_transition_set = transition_list.get(pair)
		print(current_transition_set, "set no l")
		#Luego, si el set de transiciones esta vacio sin lambda y el caracter no es lambda, 
		#probamos por el caracter siguiente current_string abbcc = $abbcc

		if(current_transition_set == None and current_char != "$"):

			current_string = "$" + current_string
			pair = (current_state, "$", current_stack_top)
			print(pair, "l")
			current_transition_set = transition_list.get(pair)
			print(current_transition_set, "set con l")
			if(current_transition_set==None):
				pair = (current_state, "$", "$")
				current_transition_set = transition_list.get(pair)

		#failed pairs
		
		#Pero si sigue estando vacio, nos toca echar para atras
		if(current_transition_set == None):
			if(pair in transition_list):
				transition_list.pop(pair)
			return self.process_string(previous_string, previous_state)


		#Si existen transiciones en el conjunto seguimos; elegimos uno aleatoriamente

		print(current_string, self.stack)

		current_transition = random.choice(tuple(current_transition_set))

		if(len(self.stack)!= 0 and pair[2]==current_transition[1]):
			pass
		elif(len(self.stack)!=0 and current_transition[1]=="$"):
			self.stack.pop()
		elif(current_transition[1]!="$"):
			self.stack.append(current_transition[1])
			print("Transicion escogida", current_transition)

		#Luego las operaciones posibles, luego se pasan a otra funcion
		return self.process_string(current_string[1:], current_transition[0], string, state)
		
		#Luego de hacer el cambio en el stack, hacemos el cambio de estado. Si eventualmente da falso, los cambios en el stack deben echar pa
		#atras tambien, como?




		
if __name__ == "__main__":	
	if(len(sys.argv)<2):
		print("Error:")
	else:
		afpn = AFPN.from_file_name(file=sys.argv[1])
			
		while(True):
			cadena = input("Ingresa una cadena afpd\n")
			afpn.stack = []
			print(afpn.process_string(cadena, afpn.initial))
	main()