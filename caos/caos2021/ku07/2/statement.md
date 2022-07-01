|                      |       |
|----------------------|-------|
| **Time limit:**      | `1 s` |
| **Real time limit:** | `1 s` |
| **Memory limit:**    | `8M`  |


### Problem ku07-2: kr07-2 (дореш)

Напишите программу `socket_echo PORT_NO`, которая слушает указанный порт по протоколу TCP и отдаёт
клиенту то же, что получил от него. В случае, если клиент ничего не передал, следует ему передать
сообщение "Empty message #{MESS_NO}\n", где MESS_NO - номер пустого сообщения. Нумерация начинается
с единицы при старте программы. Нумеруются только пустые сообщения. После отдачи результата клиенту
закройте соединение.

Все запросы следует обрабатывать последовательно. Новые процессы создавать НЕ НУЖНО.

Сообщения бинарные, размер сообщений не ограничен.

Гарантируется, что указанный порт всегда доступен. Используйте опции SO_REUSEADDR и SO_REUSEPORT.

Вас убьют SIGTERM-ом, завершайтесь успешно.

### Examples

#### Input

    
    
    ./socket_echo "$SOCKET_NO" &
    echo -ne "Hello world\n" | nc -N localhost "$SOCKET_NO"
    kill "$(ps -C "./socket_echo" h | cut -f 2 -d " ")"

#### Output

    
    
    Hello world
    

#### Input

    
    
    ./socket_echo "$SOCKET_NO" &
    echo -n "" | nc -N localhost "$SOCKET_NO"
    echo -ne "test\n" | nc -N localhost "$SOCKET_NO"
    echo -n "" | nc -N localhost "$SOCKET_NO"
    kill "$(ps -C "./socket_echo" h | cut -f 2 -d " ")"

#### Output

    
    
    Empty message #1
    test
    Empty message #2
    

