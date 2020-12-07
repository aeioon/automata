import sys
import re
import copy

class MTMC():

	def __init__(self, states=set({}), initial="", accepting=set({}), inputAlphabet=set({}), tapeAlphabet=set({}), transitions=set({}), file=None):

		self.states=states
		self.initial= initial
		self.accepting= accepting
		self.inputAlphabet=inputAlphabet
		self.tapeAlphabet=tapeAlphabet
		self.transitions = transitions
		self.tapes = []

		#El numero de :s antes de ? indica el numero de cintas.

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
		number_of_tapes = 0
		for line in self.transitions:
			chars = re.split(':|\\?|;', line) 
			number_args = int((len(chars)-2)/3)
			transition_list[tuple([chars[i] for i in range(0, number_args+1)])] = [ chars[i] for i in range(number_args+1, 3*number_args+2)]
		self.tapes = [[] for i in range(number_args)]
		return transition_list

	def displace(self, transition):
		if transition[1] == '<':
			return -1
		elif transition[1] == '>':
			return 1
		else:
			return 0

	def process_string(self, string, details=False):
		transitions = self.get_transition_set()
		tapes = self.tapes
		current_state = self.initial
		pointers = [0 for i in range(0, len(tapes))]

		for char in string:
			tapes[0].append(char)
		for tape in tapes:
			tape.append("!")
			tape.append("!")
		
		while(len(tapes[0]) != None and current_state not in self.accepting):

			temps = copy.deepcopy(tapes)
			for i in range(0, len(temps)):
				temps[i].insert(pointers[i], "*")

			if details: print("({}, {}, {})".format(current_state, ''.join(temps[0]), ''.join(temps[1])), "->", end='')
			for tape in tapes:
				if(tape[-1]!="!"):
					tape.append("!")
			pair = tuple([current_state]) + tuple([tapes[tape][pointers[tape]]for tape in range(0, len(tapes))])
			transition = transitions.get(pair)
			if transitions.get(pair) == None:

				print("Rejected")
				return False

			for tape in range(0, len(tapes)):
				position = 2*tape+1
				current_index = pointers[tape]
				next_index = current_index+self.displace([transition[position], transition[position+1]])
				tapes[tape][current_index]= transition[position]
				pointers[tape] = next_index
				current_state = transition[0]

		if details: print("({}, {}, {})".format(current_state, ''.join(temps[0]).rstrip("!"), ''.join(temps[1]).rstrip("!")), "->", end='')
		print("Accepted")
		return True

	def process_string_with_details(self, string):

		return self.process_string(string, details=True)

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
	print("Error: Ingresa un archivo mttm de la siguiente forma")
	print("python mtmc.py archivo.mttm")
else:

	mtmc = MTMC.from_file_name(file=sys.argv[1])
	while(True):
		cadena = input("Ingresa una cadena\n")
		print(mtmc.process_string_with_details(cadena))



