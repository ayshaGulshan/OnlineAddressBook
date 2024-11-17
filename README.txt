                                            README for Multiple Client-Server Program
Project Overview
----------------

This program implements an online, multithreaded address book application that allows multiple clients to interact with a server simultaneously 
Supporting ten commands: LOGIN, LOGOUT, WHO, LOOK, UPDATE, ADD, DELETE, LIST, QUIT, and SHUTDOWN. 
The server listens for incoming connections, handles commands from clients, and processes them accordingly. 
The client connects to the server and sends commands as per user input. 
Both client and server handle errors and ensure proper termination of connections.


Technologies Used
-----------------

Language: Python 3
Networking: Socket programming (TCP)
Data Storage: JSON file for storing address book records


Commands Implemented
--------------------

LOGIN <item1> <item2>: Allows the client to login to server
LOGOUT: Allows the client to logout from the server
WHO: To list all active users
LOOK <item1> <item2>: To look up an item in the book
UPDATE <item1> <item2> <item3>: To update an existing record in the book and display the updated record
ADD <item1> <item2> <item3>: Adds a record in the address book.
DELETE <item>: Deletes a specified record from the address book.
LIST: Lists all records stored in the address book.
SHUTDOWN: Shuts down the server after closing all open connections and files.
QUIT: Closes the connection for the client, but keeps the server running.


Error Handling
--------------

The server handles invalid or malformed commands without crashing.
When the user tries to login and if the UserId and Password don't match with each other, the server responds with an error message "410 Wrong UserID or Password", and the connection remains active.
When the user tries to search an item and if there is no match, the server responds with an error message “404 Your search did not match any records” and the connection remains active.
When the user tries to update an item and if the ID don't match, the server responds with an error message "403 The Record ID does not exist" and the connection remains active.
If the user tries to perform ADD OR DELETE function without logging in, the server responds with an error message "401 You are not currently logged in, login first" and the connection remains active.
If the user other than the root user tries to SHUTDOWN the server, the server responds with an error message "402 User not allowed to execute this command" and the connection remains active.
If an invalid command is sent, the server responds with an error message "300 Invalid command", and the connection remains active.
Also if the user enters more than 8 characters for first name and last name and phone number not equal to 12 characters, the server responds with an error message "Unable to add, invalid data"
If the server encounters an error during operation, it logs the error and continues to run, unless a critical error occurs that requires a shutdown.
Clients that disconnect unexpectedly will not crash the server, which will continue to allow new clients to connect.


Running the Program

Prerequisites
-------------

Make sure you have the following before running the application:

1. Python installed on your system.
2. Both the client and server Python files (`client.py` and `server.py`).
3. A JSON file `data.json` created in the same directory where the server is running.
4. Ensure both the client and server can communicate on the same network.

Compilation and Execution
-------------------------

This project does not require compilation, but it needs to be executed in a Python environment.

Running the Server

To run the server, navigate to the directory containing the scripts (server.py & client.py) and run:
python3 server.py
You will see the below text in the terminal
Server listening on port <port number>...
The server will start and wait for clients to connect.


Running the Client

To run the client, navigate to the directory containing the client script and run:
python3 client.py <IP address>
python3 client.py 127.0.0.1
You will see the below text in the terminal
Connected to <IP address> on port <port number>
C:
You will see the below text in the Server terminal
Accepted connection from ('127.0.0.1', 64597)


To execute ADD command(Make sure you're logged in)

In the Client terminal, enter the below text
C: ADD <first-name> <last-name> <phone-number>
Once the record is added, the server will send the below message
S: 200 OK
The new record Id is <id>
If the command is not in the specified format, server will take it as a invalid command
Max of only 20 records can be added. If you try to add more than 20, it will show "The Address book is full with 20 records, so unable to add record" message 


To execute LIST command

In the Client terminal, enter the below text
C: LIST
Once the command is received by the server, it will send the list to the client as below
S 200 OK
The list of records in the book is:
<id> <first-name> <last-name> <phone-number>
If the command is not in the specified format, server will take it as a invalid command


To execute DELETE command(Make sure you're logged in)

In the Client terminal, enter the below text
C: DELETE <id>
Once the command is received by the server, it will delete the record based on the id sent by the client as below
S: 200 OK
If the command is not in the specified format, server will take it as a invalid command
If you try to delete a record that does not exists, it will show "No such record exist" message
If you try to delete a record from an empty address book, it will show "Address book is empty, deletion not possible" message


To execute SHUTDOWN command(Note: Only root user can perform this function)

In the client terminal, login as root user and enter the below text
C: SHUTDOWN
Once the command is received by the server, it will terminate both the server and all clients
S: 200 OK
At the windows of other client it will display the below message
S: 210 the server is about to shutdown ......


To execute QUIT command

In the Client terminal, enter the below text
C: QUIT
Once the command is received by the server, it will terminate client
S: 200 OK


To execute LOGIN command

In the Client terminal, enter the below text
C: LOGIN <UserId> <Password>
Once the command is received by the server, it will check if the UserID and Password are correct and match each other
If the UserID and Password are correct and match each other, the server will send the below message
S: 200 OK
If the UserID and Password are incorrect and don't match each other, the server will send the below message
S: 410 Wrong UserID or Password
If the command is not in the specified format, server will take it as a invalid command


To execute LOGOUT command

In the Client terminal, enter the below text
C: LOGOUT
Once the command is received by the server, the server will send the below message
S: 200 OK
If the user tries to perform LOGOUT function without logging in, the server will send the below message
S: 400 You are not logged in
If the command is not in the specified format, server will take it as a invalid command


To execute WHO command

In the Client terminal, enter the below text
C: WHO
Once the command is received by the server, it will send the list of active users to the client as below
S: 200 OK
The list of the active users:
<UserId> <Ip-Address> 
If the command is not in the specified format, server will take it as a invalid command


To execute UPDATE command(Make sure you're logged in)

In the Client terminal, enter the below text
C: UPDATE <Id> 1 <first-name> (or) UPDATE <Id> 2 <last-name> (or) UPDATE <Id> 3 <phone-number>
Once the command is received by the server, it will update the record and send to the client as below
S: 200 OK
Record <Id> updated
<Id> <first-name>> <last-name> <phone-number>
If the user tries to update an item and if the ID don't match, the server sends the below message to the client
S: 403 The Record ID does not exist 
If the command is not in the specified format, server will take it as a invalid command


To execute LOOK command(Make sure you're logged in)

In the Client terminal, enter the below text
C: LOOK 1 <first-name> (or) LOOK 2 <last-name> (or) LOOK 3 <phone-number>
Once the command is received by the server, it will update the record and send to the client as below
S: 200 OK
Found <no of matches> match
<Id> <first-name>> <last-name> <phone-number>
If the user tries to look an item and if the items don't match, the server sends the below message to the client
S: 404 Your search did not match any records
If the command is not in the specified format, server will take it as a invalid command


Output
------

LOGIN - SUCCESS
----------------
C: LOGIN mary mary08
S: 200 OK

LOGIN - INVALID USER
---------------------
C: LOGIN aysha aysha123
S: 410 Wrong UserID or Password
------------------------------------------------------------------------------------------------

-----------
LOGOUT - SUCCESS
-----------------
C: LOGOUT
S: 200 OK

LOGOUT - WHEN NOT LOGGED IN
------------------------------
C: LOGOUT
S: 400 You are not logged in
------------------------------------------------------------------------------------------------

-----------
WHO - SUCCESS WITH LOGIN
------------------------
C: WHO
S: 200 OK
The list of the active users:
mary     127.0.0.1
root     141.215.69.184

WHO - WITHOUT LOGGED IN USERS
-----------------------------
C: WHO
S: 200 OK
No active users at the moment.
------------------------------------------------------------------------------------------------

-----------
LOOK - SUCCESS WITH LOGIN
------------------------
C: LOOK 1 Aysha
S: 200 OK
Found 2 matches
1002     Aysha Gulshan   345-754-6779
1003     Aysha Devika    455-783-4792

C: LOOK 2 Devika
S: 200 OK
Found 1 match
1003 Aysha Devika 455-783-4792

C: LOOK 3 455-783-4792
S: 200 OK
Found 1 match
1003 Aysha Devika 455-783-4792

LOOK- WRONG RECORD
-------------------

C: LOOK 1 Ayzin
S: 404 Your search did not match any records

LOOK - WITHOUT LOGIN
-----------------------------
C: LOOK 1 Aysha
S: 200 OK
Found 2 matches
1002     Aysha Gulshan   345-754-6779
1003     Aysha Devika    455-783-4792
------------------------------------------------------------------------------------------------

-------------
UPDATE - WITHOUT LOGIN
------------------------
C: UPDATE 1002 1 Ayzin
S: 401 You are not currently logged in, login first

UPDATE - WITH LOGIN
--------------------
C: UPDATE 1002 2 Thasneem
S: 200 OK
Record 1002 updated
1002 Aysha Thasneem 345-754-6779

UPDATE - WRONG ID 
------------------------
C: UPDATE 1005 2 Aysha
S: 403 The Record ID does not exist
------------------------------------------------------------------------------------------------

---------------
ADD - WITHOUT LOGIN
------------------------
C: ADD abc def 678-908-9087
S: 401 You are not currently logged in, login first

ADD - WITH LOGIN
--------------------
C: ADD Aysha Devika 455-783-4792
S: 200 OK 
The new record Id is 1003
------------------------------------------------------------------------------------------------

-----------
LIST - SUCCESS WITH LOGIN
--------------------------
C: LIST
S: 200 OK
The list of records in the book:
1001     Devika Shaj     123-456-7890
1002     Aysha Gulshan   345-754-6779
1003     Aysha Devika    455-783-4792


LIST - WITHOUT LOGGED IN 
------------------------
C: LIST
S: 200 OK
The list of records in the book:
1001     Devika Shaj     123-456-7890
1002     Aysha Gulshan   345-754-6779
1003     Aysha Devika    455-783-4792

LIST- WHEN EMPTY
----------------
C: LIST
S: 200 OK
Address book is empty
------------------------------------------------------------------------------------------------

-------------
DELETE - WITHOUT LOGIN
------------------------
C: DELETE 1001
S: 401 You are not currently logged in, login first

DELETE - WITH LOGIN
--------------------
C: DELETE 1003
S: 200 OK

DELETE - WRONG ID 
------------------------
C: DELETE 1
S: No such record exists
------------------------------------------------------------------------------------------------------

SHUTDOWN - WITH LOGIN
------------------------
OTHER USER
---------
C: SHUTDOWN
S: 402 User not allowed to execute this command

ROOT USER
----------------
C: SHUTDOWN
S: 200 OK

Other user terminal
-------------------
C:
S: 210 the server is about to shutdown ......

SHUTDOWN - WITHOUT LOGIN
--------------------------------
C: SHUTDOWN
S: 401 You are not currently logged in, login first
----------------------------------------------------------------------------------------------------

QUIT - WITH AND WITHOUT LOGIN
----------------------------
C: QUIT
200 OK
----------------------------------------------------------------------------------------------------------

Output for Invalid command
--------------------------
C: DELETE
S: 300 invalid command




