Installing PostgreSQL from source code:

`tar xzf /home/student/postgresql-13.6.tar.gz` - unpack the source code

`ls -ld /home/student/postgresql-13.6` - check the directory

`cd /home/student/postgresql-13.6` - go to the directory

`./configure --help` - check the configuration options

`./configure --prefix=/home/student/pgsql13 --with-pgport=5432` - configure the source code

`make` - compile the source code

`make install` - install the source code

Cluster creation:

`mkdir /home/student/pgsql13/data` - create a new directory for the cluster

`export PGDATA=/home/student/pgsql13/data` - set the PGDATA environment variable

`export PATH=/home/student/pgsql13/bin:$PATH` - set the PATH environment variable

Server Management:

` initdb -U postgres -k -D /home/student/pgsql13/data` - create a new cluster

`pg_ctl -D /home/student/pgsql13/data1 -l /home/student/logfile start` - start the server

`psql -U postgres -p 5432 -c 'SELECT now();'` - connect to the server and execute a query

```bash
              now              
-------------------------------
 2023-11-23 17:42:36.388934+03
(1 row)
```


Optional (if port is busy):

`sudo lsof -i :5432` - find PID

`sudo kill -9 <PID>` - kill process

## (20 points) Practice "Installation and server managment"

### Enabling checksum calculation in a cluster.
1. Stop the server.
2. Verify that checksums are being calculated in the cluster.
3. Enable checksum calculation.
4. Start the server

### Solution
   
![](pictures/hw1-1.png)

1. Stop the server

    `pg_ctl -D /home/student/pgsql13/data1 -l /home/student/logfile stop`

![](pictures/hw1-2.png)

2. Verify that checksums are being calculated in the cluster.

    `pg_checksums -D /home/student/pgsql13/data1 -d`

![](pictures/hw1-3.png)

3. Enable checksum calculation.

    `pg_checksums -D /home/student/pgsql13/data1 -e`

![](pictures/hw1-4.png)

4. Start the server

    `pg_ctl -D /home/student/pgsql13/data1 -l /home/student/logfile start`
![](pictures/hw1-5.png)
## (10 points) Practice+ (optional)

1. Install PostgreSQL from source code as it is
2. Create a database cluster, start the server.
3. Verify that the server is running.
4. Stop the server.

### Solution

I swear I did it, but I forgot to take a screenshot and cache of my terminal was full. I made it by given instructions in presentation. As proof i done first task in this homework and it's screenshot is above.

## (30 points) Practice "PSQL"

1. Run psql and check the information about the current connection.
2. Print all rows of the pg_tables table.
3. Set the "less -XS" command for page-by-page view and once again output all rows of pg_tables.
4. The default prompt shows the database name. Customize the prompt to additionally information about the user is displayed: role@database=#
5. Configure psql so that all commands display the duration of execution. Make sure that this setting is preserved when you run it again

### Solution

1. Run psql and check the information about the current connection.

    `psql -U postgres -p 5432 -c 'SELECT now();'`

![](pictures/hw1-6.png)

2. Print all rows of the pg_tables table.

    `psql -U postgres -p 5432 -c 'SELECT * FROM pg_tables;'`

![](pictures/hw1-7.png)

On the screenshot above you can see not all rows of pg_tables table, because of my terminal.

3. Set the "less -XS" command for page-by-page view and once again output all rows of pg_tables.

    `psql -U postgres -p 5432 -c 'SELECT * FROM pg_tables;' | less -XS`

Done and screenshot is the same as in previous task.

4. The default prompt shows the database name. Customize the prompt to additionally information about the user is displayed: role@database=#

    `export PS1='%n@%d=# '` - set the PS1 environment variable

    





## (10 points) Practice+(optional)


## (20 points) Practice "Configuration"


## (10 points) Practice+ (optional)





