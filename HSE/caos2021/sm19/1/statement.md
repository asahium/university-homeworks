|                      |       |
|----------------------|-------|
| **Time limit:**      | `1 s` |
| **Real time limit:** | `5 s` |
| **Memory limit:**    | `64M` |


### Problem sm19-1: test-exam/0x01

В аргументах командной строки задаются val1 и val2: два 32-битных знаковых целых числа, записанных в
девятеричной системе счисления.

На стандартный поток вывода напечатайте два булевских значения (0 или 1), каждое на отдельной
строке:

* первое булевское значение равно 1, если сложение (val1 + val2) по правилам Си приводит к undefined behavior, и 0 в противном случае 
* второе булевское значение равно 1, если деление (val1 / val2) по правилам Си приводит к undefined behavior, и 0 в противном случае 

Например, если программа называется solution, при ее запуске с аргументами:

    
    
    ./solution 1000000000 1000000001

должно быть выведено

    
    
    0
    0
