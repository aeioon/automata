'''

'''
import re
import sys


class AFD:

	#Constructor
	def __init__(self, alphabet=set({}), states=set({}), initial="", accepting=set({}), transitions=set({}), file=None):
		self.alphabet = alphabet
		self.states = states
		self.initial = initial
		self.accepting = accepting
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

					if(currently_reading == "#alphabet"):
						if("-" in line):
							for char in range(ord(line[0]), ord(line[2])+1):
								getattr(self, automata_attribute).add(chr(char))

					if(currently_reading == "#initial"):
						self.initial = line
					else:
						getattr(self, automata_attribute).add(line)
				

	#Constructor de archivo
	@classmethod
	def from_file_name(cls, file):
		return cls(file=file)

	#Conjunto de transiciones
	def get_transition_set(self):
		transition_list = {}
		for line in self.transitions:
			#Separa las transiciones en
			#estado inicial, simbolo, estado final
			#Posiblemente deba ser modelado como una clase propia.
			chars = re.split(':|>', line)
			transition_list[(chars[0], chars[1])] = (chars[2])

		return transition_list

	def process_string(self, string, details=False):
		transitions = self.get_transition_set()
		current_state = self.initial
		current_string = string
		for char in string:
			if(char=="!"):
				current_state = current_state
			elif(char not in self.alphabet):
				print("No existe el simbolo en el alfabeto de la cinta")
				return False
			else:
				if details: print("({},{})->".format(current_state, current_string), end = '')
				current_state = transitions[(current_state, char)]
				current_string = current_string[1:]
			
		if details: print("({},{})->".format(current_state, '$'), end = '')

		if(current_state in self.accepting):
			if details: print("Accepted")
			return True
		else:
			if details: print("Rejected")
			return False

	def process_string_with_details(self, string):
		return self.process_string(string, details=True)

	def process_list_strings(self, string_list, filename, printScreen=False):

		with open("{}.txt".format(filename), "w") as writer:
			sys.stdout = writer
			for string in string_list:
				self.process_string_with_details(string)
		if(printScreen==True):
			with open("{}.txt".format(filename), "r") as reader:
				sys.stdout = sys.__stdout__
				for line in reader.readlines():
					print(line)



if __name__ == "__main__":	
	if(len(sys.argv)<2):
		print("Error: Ingresa un archivo dfa de la siguiente forma")
		print("python dfa.py archivo.dfa")
	else:
		afd = AFD(file=sys.argv[1])
		while(True):
			cadena = input("Ingresa una cadena\n")
			afd.process_string_with_details(cadena)
	main()