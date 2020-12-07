'''
Este archivo muestra algunas propiedades de nuestro MT, sin necesidad de ingresar un archivo en el argv.
Como se describe en el README, se puede ejecutar el MT.py directamente pero sera necesario que proporcione un archivo .tm en su terminal en la forma
python/python3 mt.py archivo.mt
'''

import sys
sys.path.insert(1, '../')

from mt import MT

#Construimos un MT sin necesidad de archivo, este es el mismo mt encontrado en turing1.mt, el cual describe los palindromos pares formados por aes y bes

mt = MT({'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'}, "q0", {'q6'}, {'a', 'b'}, {"a", "b"}, {"q0:a?q1:!:>","q0:b?q3:!:>","q0:!?q6:!:-","q1:a?q1:a:>","q1:b?q1:b:>","q1:!?q2:!:<","q2:a?q5:!:<","q3:a?q3:a:>","q3:b?q3:b:>","q3:!?q4:!:<","q4:b?q5:!:<","q5:a?q5:a:<","q5:b?q5:b:<","q5:!?q0:!:>"})

#Deberia aceptar los primeros 3, rechazar los ultimos 3.

test1 = "baab"
test2 = "aaaabbaaaa"
test3 = "abba"
test4 = "baaab" #palindromo impar
test5 = "bbabb" #impar
test6 = "bbaab" #no un palindromo

test_array = [test1, test2, test3, test4, test5, test6]
###Imprimimos los procesos y la ultima confuracion instantanea
for test in test_array:
	print(mt.process_string_with_details(test))
	print(mt.process_function(test))

print("Imprimimos los atributos del AFPD")
print(mt)

print("Luego procesamos estas cadenas en test_array y las imprimimos en un archivo usando process_string_list.")
mt.process_string_list(test_array, "mt_string_list")

