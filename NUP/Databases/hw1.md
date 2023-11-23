## (20 points) Practice "Installation and server managment"

### Enabling checksum calculation in a cluster.
1. stop the server.
2. Verify that checksums are being calculated in the cluster.
3. Enable checksum calculation.
4. Start the server

### Solution
    
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

`pg_ctl -D /home/student/pgsql13/data1 -l /home/student/logfile stop` - stop the server

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



1. Stop the server
```bash
sudo systemctl stop postgresql
```

2. Verify that checksums are being calculated in the cluster.
```bash
sudo -u postgres psql -c "SHOW data_checksums;"
```
Output:
```
data_checksums
-----------------
off
(1 row)
```

3. Enable checksum calculation.
```bash
sudo -u postgres psql -c "ALTER SYSTEM SET data_checksums TO on;"
```

4. Start the server
```bash
sudo systemctl start postgresql
```
 

## (10 points) Practice+ (optional)



## (30 points) Practice "PSQL"


## (10 points) Practice+(optional)


## (20 points) Practice "Configuration"


## (10 points) Practice+ (optional)





