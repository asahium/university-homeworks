|                      |       |
|----------------------|-------|
| **Time limit:**      | `2 s` |
| **Real time limit:** | `5 s` |
| **Memory limit:**    | `64M` |


### Problem sm10-1: unix/filesystem/traverse-2

В аргументах командной строки передается путь к каталогу. Этот каталог является корнем поддерева
файловой системы.

Обойдите рекурсивно все подкаталоги и на стандартный поток вывода напечатайте команды 'cd', с
помощью которых можно обойти все подкаталоги и вернуться в исходный каталог. Каждая команда cd может
переходить на один каталог вверх/вниз по иерархии.

В одном каталоге подкаталоги должны просматриваться в лексикографическом порядке без учета регистра
букв. Сравнение без учета регистра букв выполняется функцией strcasecmp. Каталог, который нельзя
открыть на чтение с помощью opendir, должен быть пропущен, то есть в него не нужно входить и из него
не нужно выходить. Переходить по символическим ссылкам не нужно, даже если они указывают на
директории.

Список файлов в директории может изменяться между любыми двумя вызовами `opendir` / `rewinddir` для
этой директории. Гарантируется корректность любого списка поддиректорий, полученного полным проходом
по директории с помощью `readdir`.

Никакого экранирования спецсимволов не требуется. Гарантируется, что в одном каталоге не
присутствуют каталоги, отличающиеся только регистром букв. Обрабатывать пути длиннее чем
`PATH_MAX-1` не требуется.

Не используйте `scandir`, `ftw` и аналогичные функции. Не используйте `chdir`, `fchdir`, `telldir`,
`seekdir`, а также `getpwd` и аналогичные. Можно использовать `opendir`, `readdir`, `closedir` и
`*stat`.

Например, для такого дерева директорий:

    
    
    /data
    |-a
      |-b
        |-c
        |-d
    

При запуске программы с аргументом `/data` вывод должен быть таким:

    
    
    cd a
    cd b
    cd c
    cd ..
    cd d
    cd ..
    cd ..
    cd ..
    
