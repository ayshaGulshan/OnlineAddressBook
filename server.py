"""
This script contains code for server creates a socket for communicating with the client with multithreading capabilities
Developed by 
"""
# Importing required libraries
import socket
import json
import threading
import re

# Server configuration and global variables
SERVER_PORT = 2223
ADDRESS_BOOK_FILE = 'data.json'
clients = {}  
users = {  
    "root": "root05",
    "john": "john06",
    "david": "david07",
    "mary": "mary08"  
}
logged_in_users = {}  
shutdown_flag = False
clients = {}  


def main():
    """Main function to initialise socket object and start listening 
    """
    #Defining global variable
    global shutdown_flag

    # Create a socket object and bind it to the server port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind(('0.0.0.0', SERVER_PORT))
    server_socket.listen(5) # Start listening for connections
    print(f"Server listening on port {SERVER_PORT}...")

    try:
        while not shutdown_flag:
            
            # Check shutdown flag to stop accepting new connections
            server_socket.settimeout(1.0)  # Set timeout to periodically check the shutdown flag
            try:
                # Accept a new connection
                client_socket, client_address = server_socket.accept()
                print(f"Accepted connection from {client_address}")

                # Add the client to the clients dictionary
                clients[client_socket] = client_address

                # start a handler thread
                threading.Thread(target=handle_client, args=(client_socket,)).start()
            except socket.timeout:
                continue  # Timeout to allow shutdown flag check

    finally:
        server_socket.close()

def broadcast_shutdown():
    """Broadcast shutdown message to all clients and initiate server shutdown
    """
    global shutdown_flag
    shutdown_message = "210 the server is about to shutdown ......"

    # Set shutdown flag to True to notify all client threads
    shutdown_flag = True

    # Notify all connected clients and close their connections
    for client_socket, client_address in list(clients.items()):
        try:
            # checking if the current user is root
            if client_socket in logged_in_users and logged_in_users[client_socket][0] == "root":
                shutdown_message = shutdown_message + "_root"
            
            client_socket.send(shutdown_message.encode())
            client_socket.close()
        except socket.error as e:
            print(f"Error sending shutdown message to client {client_address}: {e}")

    # Clear the clients dictionary
    clients.clear()


def handle_client(client_socket):
    """Handle each client connection, keeping it open for broadcasts.
    """
    global shutdown_flag
    try:
        while not shutdown_flag:  # Exit loop if shutdown is initiated
            client_data = client_socket.recv(1024).decode().strip()
            if not client_data:
                break
            print(f"Received command: {client_data}")
            response = handle_command_operations(client_data, client_socket)

            # Send response to the specific client
            if not shutdown_flag:
                client_socket.send(response.encode())
            else:
                break  # Exit if shutdown has been triggered

    except Exception as e:
        pass

    finally:
        # Ensure the client is removed from logged-in users and clients upon disconnect
        logout_client(client_socket)

        if client_socket in clients:
            del clients[client_socket]
        client_socket.close()

def handle_command_operations(command, client_socket):
    """Processes and executes client commands, handling authentication and command validation.
    """
    global clients, logged_in_users
    command_parts = command.split()
    cmd = command_parts[0]

    # Commands allowed without login
    anonymous_commands = {"LIST", "WHO", "LOOK", "QUIT"}

    if cmd in anonymous_commands:
        # Execute without requiring login
        return execute_command(cmd, command_parts, client_socket)
    elif cmd == "LOGIN" and len(command_parts) == 3:
        return login_client(client_socket, command_parts[1], command_parts[2])
    elif cmd == "LOGOUT" and len(command_parts) == 1:
        return logout_client(client_socket)
    else:
        # Check if the client is logged in for restricted commands
        if client_socket in logged_in_users:
            return execute_command(cmd, command_parts, client_socket)
        else:
            if cmd == "LOGIN" and not len(command_parts) == 3:
                return "300 Invalid command"
            if cmd == "LOGOUT" and not len(command_parts) == 1:
                return "300 Invalid command"
            return "401 You are not currently logged in, login first"
        
    

def execute_command(cmd, command_parts, client_socket):
    """Executes a command based on the command type
    """
    address_data = load_record_read()

    if cmd == "WHO" and len(command_parts)==1:
        return list_active_users()
    elif cmd == "LOOK" and len(command_parts) == 3:
        return look_up_record(load_record_read(), command_parts[1], " ".join(command_parts[2:]))
    elif cmd == "LIST" and len(command_parts) == 1:
        return list_records(address_data)
    elif cmd == "ADD" and len(command_parts) == 4:
        return add_record(address_data, command_parts[1:])
    elif cmd == "DELETE" and len(command_parts) == 2:
        return delete_record(address_data, command_parts[1])
    elif cmd == "UPDATE" and len(command_parts) == 4:
        return update_record(load_record_read(), command_parts[1], command_parts[2], " ".join(command_parts[3:]))
    elif cmd == "SHUTDOWN" and len(command_parts)==1:
        try:
            # Ensure only root user can execute the SHUTDOWN command
            if logged_in_users[client_socket][0] == 'root':
                broadcast_shutdown()
                return "200 OK"
            else:
                return "402 User not allowed to execute this command"
        except socket.error as socket_error:
            print("ERROR Unable to shutdown")
            return "ERROR Unable to shutdown"
    elif cmd == "QUIT" and len(command_parts) == 1:
        if client_socket in logged_in_users:
            message = logout_client(client_socket)
            if message ==  "200 OK - Logged out":
                print("Logging out")
            else:
                return "Unable to quit"
        return "200 OK"
    else:
        return "300 Invalid command"

def list_active_users():
    """Return a list of active users with their UserIDs and IP addresses
    """
    if logged_in_users:
        response = "200 OK\nThe list of the active users:\n"

        for _, (user_id, ip_address) in logged_in_users.items():
            response += f"{user_id}\t {ip_address}\n"
        return response.strip()
    else:
        return "200 OK\nNo active users at the moment."


def login_client(client_socket, user_id, password):
    """Authenticate a client and store their UserID and IP address if successful
    """
    if user_id in users and users[user_id] == password:

        # Retrieve the client’s IP address from the socket
        client_ip = client_socket.getpeername()[0]
        logged_in_users[client_socket] = (user_id, client_ip)
        return "200 OK"
    return "410 Wrong UserID or Password"


def logout_client(client_socket):
    """Log out a client
    """
    if client_socket in logged_in_users:
        del logged_in_users[client_socket]
        return "200 OK"
    return "400 You are not logged in"

def list_clients():
    """List logged-in clients
    """
    if logged_in_users:
        return "200 OK - Logged in clients:\n" + "\n".join(logged_in_users.values())
    return "200 OK - No clients currently logged in"

def look_up_record(data, search_type, search_value):
    """Look up a record by first name, last name, or phone number
    """
    matches = []

    # Convert search_type to integer to decide the field to search
    search_type = int(search_type)
    
    for record in data:
        if search_type == 1 and record["first_name"] == search_value:
            matches.append(record)
        elif search_type == 2 and record["last_name"] == search_value:
            matches.append(record)
        elif search_type == 3 and record["phone_number"] == search_value:
            matches.append(record)

    if matches:
        response = f"200 OK\nFound {len(matches)} match{'es' if len(matches) > 1 else ''}\n"
        for match in matches:
            response += f"{match['id']} {match['first_name']} {match['last_name']} {match['phone_number']}\n"
        return response.strip()
    else:
        return "404 Your search did not match any records"

def add_record(data, record):
    """Fn to add a record to address book
    """
    try:
        if len(data) < 20:
            # Find the highest ID in the existing data
            max_id = max((int(item["id"]) for item in data), default=1000)
            new_id = str(max_id + 1)
            
            # Create a new record with the calculated ID
            if record[0].isalpha() and record[1].isalpha() and re.fullmatch(r'^\d+(-\d+)*$', record[2]) :
                if len(record[0])<= 8 and len(record[1])<=8 and len(record[2]) == 12: 
                    new_record = {"id": new_id, "first_name": record[0], "last_name": record[1], "phone_number": record[2]}
                    data.append(new_record)
                    save_address_book(data)
                    return f"200 OK \nThe new record Id is {new_id}"
                else:
                    return "Unable to add, invalid data"
            else:
                return "Unable to add, invalid data"
        return "Unable to add record. Address book is full with 20 records"
    except socket.error:
        return f"ERROR Unable to add"


def delete_record(data, record_id):
    """Fn to delete a record from address book
    """
    try:
        for record in data:
            if record["id"] == record_id:
                data.remove(record)
                save_address_book(data)
                return "200 OK"
        return "No such record exists"
    except socket.error:
        return f"ERROR Unable to delete"

def update_record(data, record_id, field_type, new_value):
    """Update an existing record by Record ID
    """
    # Find the record by ID
    for record in data:
        if record["id"] == record_id:
            # Update the appropriate field
            field_type = int(field_type)
            if field_type == 1:
                record["first_name"] = new_value
            elif field_type == 2:
                record["last_name"] = new_value
            elif field_type == 3:
                record["phone_number"] = new_value
            else:
                return "400 Invalid update field type"

            # Save the updated address book to file
            save_address_book(data)

            # Return the success response with the updated record
            response = f"200 OK\nRecord {record_id} updated\n"
            response += f"{record['id']} {record['first_name']} {record['last_name']} {record['phone_number']}"
            return response
    # If no record found with the given ID, return 403 error
    return "403 The Record ID does not exist"


def list_records(data):
    """Fn to list down all the records in the address book
    """
    try:
        if data:
            return "200 OK\nThe list of records in the book:\n" + \
                  "\n".join([f"{r['id']}\t {r['first_name']} {r['last_name']}\t {r['phone_number']}" for r in data])
        return "200 OK \nAddress book is empty"
    except:
        return "ERROR Unable to list"

def load_record_read():
    """Fn to read address book
    """
    try:
        with open(ADDRESS_BOOK_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
    except json.JSONDecodeError as e:
        print("ERROR File corrupted")
        return []

def save_address_book(data):
    """Fn to save to address book
    """
    try:
        with open(ADDRESS_BOOK_FILE, 'w') as file:
            json.dump(data, file)
    except FileNotFoundError:
        print("ERROR File not found")

if __name__ == "__main__":
    main()
