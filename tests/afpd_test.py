'''
Este archivo muestra teste algunas propiedades de nuestro AFD, sin necesidad de ingresar un archivo en el argv.
Como se describe en el README, se puede ejecutar el AFD.py directamente pero sera necesario que proporcione un archivo .dfa en su terminal en la forma
python/python3 afd.py archivo.dfa
'''

import sys
sys.path.insert(1, '../')

from afpd import afpd

#Construimos un AFD sin necesidad de archivo, este es el mismo afd encontrado en adfFile.dfa, el cual describe (ab U b)*

afd = AFD({'a', 'b'}, {'q0', 'q1', 'q2'}, 'q0', {'q0'}, {'q0:a>q1','q0:b>q0','q1:a>q2','q1:b>q0','q2:a>q2','q2:b>q2'})

#Deberia aceptar los primeros 3, rechazar los ultimos 2.


test1 = "bbabababbb"
test2 = "bbbbbbbbbb"
test3 = "bbbbbabbbbbbababbbb"
test4 = "ababba"
test5 = "aaaaaaaa"

test_array = [test1, test2, test3, test4, test5]

for test in test_array:
	print(afd.process_string_with_details(test))

print("Imprimimos los atributos del AFD")
print(afd)

print("Luego procesamos estas cadenas en test_array y las imprimimos en un archivo usando process_string_list.")
afd.process_string_list(test_array, "afd_string_list")

