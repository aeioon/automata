'''
Este archivo muestra algunas propiedades de nuestro MTMC, sin necesidad de ingresar un archivo en el argv.
Como se describe en el README, se puede ejecutar el mtmc.py directamente pero sera necesario que proporcione un archivo .mttm en su terminal en la forma
python/python3 mtmc.py archivo.mttm
'''

import sys
sys.path.insert(1, '../')

from mtmc import MTMC

#Construimos un MTMC sin necesidad de archivo, este es el mismo mt encontrado en turing_multitape1.mttm, el cual describe L(M) = {a^nb^nc^n: n>=0}



mtmc = MTMC({'q0', 'q1', 'q2', 'q3', 'q4'}, "q0", {'q4'}, {"a","b"}, {"a", "b", "X"}, {"q0:a:!?q1:a;>:X;>","q1:a:!?q1:a;>:X;>","q1:b:!?q2:b;-:!;<","q2:b:X?q2:b;>:X;<","q2:c:!?q3:c;-:!;>","q3:c:X?q3:c;>:X;>","q3:!:!?q4:!;-:!;-","q0:!:!?q4:!;-:!;-"})

#Deberia aceptar los primeros 3, rechazar los ultimos 3.

test1 = "aabbcc"
test2 = "aaabbbccc"
test3 = "aaaaabbbbbccccc"
test4 = "aaabbbcc" #menos cs que otros
test5 = "aaabbccc" #menos bs
test6 = "aabbbccc" #menos as

test_array = [test1, test2, test3, test4, test5, test6]

###Imprimimos los procesos y la ultima confuracion instantanea

for test in test_array:
	print("Proceso sin detalles: ", mtmc.process_string(test))

for test in test_array:
	print("Proceso con detalles: ", mtmc.process_string_with_details(test))

print("Imprimimos los atributos del AFPD")
print(mtmc)

print("Luego procesamos estas cadenas en test_array y las imprimimos en un archivo usando process_string_list.")
mtmc.process_string_list(test_array, "mtmc_string_list")

