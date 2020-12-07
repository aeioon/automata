'''
Este archivo muestra teste algunas propiedades de nuestro AFPD, sin necesidad de ingresar un archivo en el argv.
Como se describe en el README, se puede ejecutar el AFPD.py directamente pero sera necesario que proporcione un archivo .dpda en su terminal en la forma
python/python3 afd.py archivo.pda
'''

import sys
sys.path.insert(1, '../')

from afpd import AFPD

#Construimos un AFPD sin necesidad de archivo, este es el mismo afpd encontrado en adfFile.dfa, el cual describe el a^n b^n, se puede ejecutar desde archivo
#con python afpd.py afpdFile.dpda

afpd = AFPD({'q0', 'q1', 'q2'}, "q0", {'q0','q1'}, {'a', 'b'}, {"A"},{"q0:a:$>q0:A","q0:b:A>q1:$","q1:b:A>q1:$","q1:a:$>q2:$","q2:a:$>q2:$","q2:b:$>q2:$"})

#Deberia aceptar los primeros 3, rechazar los ultimos 3.

test1 = "aaaabbbb"
test2 = "ab"
test3 = ""
test4 = "aaabb"
test5 = "aabbb"
test6 = "aba"

test_array = [test1, test2, test3, test4, test5, test6]

for test in test_array:
	print(afpd.process_string_with_details(test))

print("Imprimimos los atributos del AFPD")
print(afpd)

print("Luego procesamos estas cadenas en test_array y las imprimimos en un archivo usando process_string_list.")
afpd.process_string_list(test_array, "afpd_string_list")

