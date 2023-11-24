## (25 points) Practice "Isolation and multiversionality"

1. Create a table with a single row.

    Start the first transaction at the Read Committed and query the table.
    
    In the second session, delete the row and commit the changes.
    
    How many rows will the first transaction see by executing the same query again? Check.
    
    Complete the first transaction.
2. Do the same thing again, but now have the transaction running at isolation level Repeatable Read:
    
    `BEGIN ISOLATION LEVEL REPEATABLE READ;`

    Explain the differences.

### Solution

1. `psql -U postgres -p 5432` - first session

    ```
    => CREATE TABLE test_table (id serial PRIMARY KEY, value numeric);
    CREATE TABLE
    => INSERT INTO test_table(value) SELECT random() FROM generate_series(1, 1);
    INSERT 0 1
    => SELECT * FROM test_table;
     id |       value
    ----+-------------------
      1 | 0.596793548583895
    => BEGIN;
    BEGIN
    => COMMIT;
    COMMIT
    ```

    `psql -U postgres -p 5432` - second session

    ```
    => DELETE FROM test_table;
    DELETE 1
    => COMMIT;
    COMMIT
    ```

    `psql -U postgres -p 5432` - first session (continue)

    ```
    => SELECT * FROM test_table;
     id |       value
    ----+-------------------
    (0 rows)
    ```

    So, we can see that the first transaction see 1 row, because it started before the second transaction, and the second transaction deleted the row.

2. `psql -U postgres -p 5432` - first session

    ```
    => BEGIN ISOLATION LEVEL REPEATABLE READ;
    BEGIN
    => SELECT * FROM test_table;
     id |       value
    ----+-------------------
      1 | 0.596793548583895
    ```

    `psql -U postgres -p 5432` - second session

    ```
    => DELETE FROM test_table;
    DELETE 1
    => COMMIT;
    COMMIT
    ```

    `psql -U postgres -p 5432` - first session (continue)

    ```
    => SELECT * FROM test_table;
     id |       value
    ----+-------------------
      1 | 0.596793548583895
    ```

    So, we can see that the first transaction see 1 row, because it started before the second transaction, and the second transaction deleted the row. But when we use `BEGIN ISOLATION LEVEL REPEATABLE READ;` we can see the row in first transaction, because we use Repeatable Read isolation level.

## (25 points) Practice+ "Isolation and multiversionality"(optional)

1. Start a transaction and create a new table with a single row. Without terminating the transaction, open a second session and query the table in it. Check to see what the transaction in the second session sees

    Commit the transaction in the first session and run the table query in the second session.
2. Repeat task 1, but rollback rather than commit the transaction in the first session. What has changed?
3. In the first session, start the transaction and run a query on the table you created earlier. Will you be able to delete this table in the second session while the transaction is still in progress?
    
    Check

### Solution

1. First transaction at the Read Committed and query the table:

    Unfortunatelly, i don't have screenshot, but i can show you my terminal:
    
    `psql -U postgres -p 5432` - first session

    ```
    => BEGIN; - we start transaction
    BEGIN
    => CREATE TABLE test_table (id serial PRIMARY KEY, value numeric);
    CREATE TABLE
    => INSERT INTO test_table(value) SELECT random() FROM generate_series(1, 1);
    INSERT 0 1
    => SELECT * FROM test_table;
     id |       value
    ----+-------------------
      1 | 0.596793548583895
    ```

    `psql -U postgres -p 5432` - second session

    ```
    => SELECT * FROM test_table;
    ERROR:  relation "test_table" does not exist
    LINE 1: SELECT * FROM t1;
                            ^
    ```
    
    So we cannot see the table in second session

    `psql -U postgres -p 5432` - first session

    ```
    => SELECT * FROM test_table;
     id |       value
    ----+-------------------
      1 | 0.596793548583895
    => COMMIT;
    COMMIT
    ```

2. `psql -U postgres -p 5432` - first session

    ```
    => BEGIN ISOLATION LEVEL REPEATABLE READ;
    BEGIN
    => CREATE TABLE test_table (id serial PRIMARY KEY, value numeric);
    CREATE TABLE
    => INSERT INTO test_table(value) SELECT random() FROM generate_series(1, 1);
    INSERT 0 1
    ```

    `psql -U postgres -p 5432` - second session

    ```
    => SELECT * FROM test_table;
    ERROR:  relation "test_table" does not exist
    LINE 1: SELECT * FROM t1;
                            ^
    ```

    So we cannot see the table in second session, and if we ROLLBACK; in first session, we rollback all changes, so we cannot see the table in first session too

    `psql -U postgres -p 5432` - first session (continue)

    ```
    => ROLLBACK;
    ROLLBACK
    => SELECT * FROM test_table;
    ERROR:  relation "test_table" does not exist
    LINE 1: SELECT * FROM t1;
                            ^
    ```

    As we can see, we can see the table in second session, but we cannot see the row in second session.

3. `psql -U postgres -p 5432` - first session

    ```
    => BEGIN;
    BEGIN
    => SELECT * FROM test_table;
     id |       value
    ----+-------------------
      1 | 0.596793548583895
    => DELETE FROM test_table;
    DELETE 1
    ```

    `psql -U postgres -p 5432` - second session

    ```
    => DROP TABLE test_table;
    ERROR:  cannot drop table test_table because other objects depend on it
    ```

    So we cannot delete the table in second session while the transaction is still in progress. But when we commit the transaction in first session, we can delete the table in second session.


## (25 points) Practice "Pereodic tasks"

1. disable the auto-cleaning process and make sure it is not running.
2. In the new database, create a table with a single numeric column and an index on that table. Insert into the table 100,000 random numbers.
3. Change half of the rows of the table several times, controlling the size of the table and index at each step.
4. Perform a complete cleanup.
5. Repeat step 4, calling after each change a after each change. Compare the results.
6. Enable the auto-cleaning process.

### Solution

* in new session `psql -U postgres -p 5432`

    ![](pictures/hw2-6.png)

    ```
    ALTER SYSTEM SET autovacuum = 'off';

    CREATE TABLE test_table9 (id serial PRIMARY KEY, value numeric);

    CREATE INDEX idx_value ON test_table9(value);

    INSERT INTO test_table9(value) SELECT random() FROM generate_series(1, 100000);

    UPDATE test_table9 SET value = random() WHERE id % 2 = 0;

    VACUUM FULL test_table9;

    VACUUM FULL ANALYZE test_table9;

    ALTER SYSTEM SET autovacuum = 'on';
    ```
    
    So, we can see that the size of the table and index is the same, because we disabled the auto-cleaning process.

## (25 points) Practice "Buffer cache"

1. Use the operating system to find the processes responsible for the buffer cache and the WAL log, responsible for the buffer cache and WAL log.
2. Stop PostgreSQL in fast mode; start it again. Review the server's message log.
3. Now stop in immediate mode and start it again. Review the server message log and compare with the previous one.


### Solution

1. `locate postmaster.pid` - find the processes responsible for the buffer cache and the WAL log

    ![](pictures/hw2-8.png)

    `sudo ps -o pid,command --ppid 2722` - find the processes responsible for the buffer cache and the WAL log

    ![](pictures/hw2-9.png)

    So, we can see that the processes responsible for the buffer cache and the WAL log are checkpointer, background writer, walwriter.  