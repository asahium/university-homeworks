"""
Напишите программу, которая по данному числу N от 1 до 9 выводит на экран N пингвинов. Изображение одного пингвина имеет размер 5×9 символов, между двумя соседними пингвинами также имеется пустой (из пробелов) столбец. Разрешается вывести пустой столбец после последнего пингвина. Для упрощения рисования скопируйте пингвина из примера в среду разработки. 
"""



num = int(input())
str1 = '    _~_    '
str2 = '   (o o)   '
str3 = '  /  V  \  '
str4 = ' /(  _  )\ '
str5 = '   ^^ ^^   '
print(str1 * num)
print(str2 * num)
print(str3 * num)
print(str4 * num)
print(str5 * num)
