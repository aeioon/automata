import re
import sys

class AFPD:

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

	def get_transition_set(self):
		transition_list = {}
		for line in self.transitions:
			#Separa las transiciones en
			#estado origen, simbolo, simbolo reemplazado, estado final, simbolo que reemplaza
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

			#No imprime las descripciones instantaneas cuando la transicion no existe. Si la transicion existe pero comienza con lambda se quita el lambda
			if transition != None:
				print("({}, {})->".format(current_state, current_string.lstrip("$")), end='')
			#Si no existe la transicion entonces  la cambiamos. Si se da el caso en el que la longitud sea 1 con $ pero ni el stack este vacio ni el estado sea de acpetacion se devuelve falso
			if transition == None:
				
				if(current_string[0] == "$" and len(current_string)==1 and len(self.stack) == 0 and current_state in self.accepting):
					return True
				elif(current_string[0] == "$" and len(current_string)==1 and (len(self.stack) != 0 or current_state not in self.accepting)):
					self.stack = []
					return False
				else:
					current_string = current_string[1:]

			else:
				
				#Caso 1: Delta(q, a, lambda) = (q, b)
				#Se añade b sin importar el tope
				if(transition[0]=='$' and transition[2]!='$'):
					self.stack.append(transition[2])
					current_state = transition[1]
					current_string = current_string[1:]
				#Caso 2: Delta(q0, a, A) = (q1, B)
				#Se reemplaza A por B, el stack debe no estar vacio
				elif(len(self.stack) != 0 and transition[0]==self.stack[-1] and transition[2]!='$'):
					self.stack.pop()
					self.stack.append(transition[2])
					current_state = transition[1]
					current_string = current_string[1:]	
				#Caso 3: Delta(q, a , A) = (q', lambda)
				#Se borra a del tope
				elif(transition[2]=='$'):
					if(len(self.stack)!=0):
						self.stack.pop()
					else:
						self.stack = []
						return False # no hay tope
					current_state = transition[1]
					current_string = current_string[1:]
				#Caso 4: No se altera la pila
				elif(transition[0] == transition[2] == '$'):
					current_state = transition[1]
					current_string = current_string[1:]
				#Caso 5: Transicion lambda como en anb2n
				current_string = '$' + current_string  
		self.stack = []
	


	def process_string_with_details(self, string):
		self.process_string(string, details=True)

	def findCartesianProduct(afd):
		return True
		

if(len(sys.argv)<2):
	print("Error: Ingresa un archivo dfa de la siguiente forma")
	print("python dfa.py archivo.dfa")
else:
	afpd = AFPD.from_file_name(file=sys.argv[1])
	
	while(True):
		cadena = input("Ingresa una cadena\n")
		print(afpd.process_string(cadena))

