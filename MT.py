import sys
import re
class MT():

	def __init__(self, states=set({}), initial="", accepting=set({}), inputAlphabet=set({}), tapeAlphabet=set({}), transitions=set({}), file=None):

		self.states=states
		self.initial= initial
		self.accepting= accepting
		self.inputAlphabet=inputAlphabet
		self.tapeAlphabet=tapeAlphabet
		self.transitions = transitions

		if(file!= None):

			lines = open(file).readlines()
			
			currently_reading = ""
			for line in lines:

				line = line.rstrip("\n")

				if(line.startswith("#")):
					currently_reading = line

				if (line!="" and line != currently_reading):
					automata_attribute = currently_reading.lstrip("#")

					if(currently_reading in ["#inputAlphabet", "#tapeAlphabet"]):
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
			chars = re.split(':|\\?', line)
			transition_list[(chars[0], chars[1])] = (chars[2], chars[3], chars[4])
		return transition_list

	def displace(self, transition):
		if transition[2] == '<':
			return -1
		elif transition[2] == '>':
			return 1
		else:
			return 0

	def process_string(self, string, details=False):
		transitions = self.get_transition_set()
		tape = []
		current_state = self.initial
		tape.append(current_state)
		current_index = 0
		for char in string:
			tape.append(char)
		tape.append('!')

		print("Cadena ingresada: ", string)
		while(tape[current_index] != None and current_state not in self.accepting):	
			if details: print(''.join(tape), "->", end='')
			pair = (tape[current_index], tape[current_index+1])
			if transitions.get(pair) == None:
				#M se detiene en un estado que no es de aceptacion, 
				#lambda(q, s) no está definida
				print("Rejected")
				return False
			transition = transitions.get(pair)
			next_index = current_index+self.displace(transition)
			tape[current_index+1]= transition[1]
			tape[current_index] = tape[next_index]
			tape[next_index] = transition[0]
			current_index = next_index
			current_state = tape[current_index]
		if details: print(''.join(tape), "->", end='')	
		print("Accepted")
		return True

	def process_string_with_details(self, string):
		return self.process_string(string, details=True)

	def process_function(self, string):
		#Retorna ultima configuración instantanea
		transitions = self.get_transition_set()
		tape = []
		current_state = self.initial
		tape.append(current_state)
		current_index = 0
		for char in string:
			tape.append(char)
		tape.append('!')
		print("Cadena ingresada: ", string)
		while(tape[current_index] != None and current_state not in self.accepting):	
			pair = (tape[current_index], tape[current_index+1])
			if transitions.get(pair) == None:
				print("La transicion delta", pair," no existe")
				return last_string

			transition = transitions.get(pair)
			next_index = current_index+self.displace(transition)
			tape[current_index+1]= transition[1]
			tape[current_index] = tape[next_index]
			tape[next_index] = transition[0]
			current_index = next_index
			current_state = tape[current_index]
			last_string = ''.join(tape)

		return last_string

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
		attributes = ["states", "initial", "accepting", "inputAlphabet", "tapeAlphabet", "transitions"]
		to_string = ""
		for attribute in attributes:
			to_string = to_string + "\n#" + attribute
			for item in getattr(self, attribute):
				to_string = to_string + "\n" + item

		return to_string

if(len(sys.argv)<2):
	print("Error: Ingresa un archivo dfa de la siguiente forma")
	print("python TM.py archivo.tm")
else:


	mt1 = MT.from_file_name(file=sys.argv[1])

	mt2 = MT({'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'}, 'q0', {'q6'}, {'a', 'b'}, {'a', 'b'},  {"q0:a?q1:!:>","q0:b?q3:!:>","q0:!?q6:!:-","q1:a?q1:a:>","q1:b?q1:b:>","q1:!?q2:!:<",
"q2:a?q5:!:<","q3:a?q3:a:>","q3:b?q3:b:>","q3:!?q4:!:<","q4:b?q5:!:<","q5:a?q5:a:<","q5:b?q5:b:<","q5:!?q0:!:>"})

	while(True):
		cadena = input("Ingresa una cadena\n")
		print(mt1.process_string_with_details(cadena))
		print(mt1.process_function(cadena))



