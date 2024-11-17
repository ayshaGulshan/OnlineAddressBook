"""
This script contains code for client connecting to the server using socket
The client sends commands to the server and server send back the result to client
"""
# Importing required libraries
import socket
import sys
import threading
import time, os
import queue

# Server port
SERVER_PORT = 2223

# Defining queue to handle communication from thread to host
data_queue = queue.Queue()

def listen_for_messages(client_socket):
    """Continuously listen for incoming messages from the server.
    """
    while True:
        data = "thread"
        data_queue.put(data)  # Put data in the queue
        time.sleep(0.1)
        try:
            # Receive messages from the server
            response = client_socket.recv(1024).decode()
            if response:
                
                # If server is shutting down, exit the listener
                if response.strip() == "210 the server is about to shutdown ......_root": # checking for root user
                    print(f"S: 200 OK\n", end="")
                    data = "shutdown"
                    data_queue.put(data) 
                    time.sleep(0.1)
                    os._exit(1)
        
                elif response.strip() == "210 the server is about to shutdown ......":
                    print(f"\nS: 210 the server is about to shutdown ......\n", end="")
                    data = "shutdown"
                    data_queue.put(data) 
                    time.sleep(0.1)
                    os._exit(1)
                   
                print(f"S: {response}\n", end="")
            else:
                print("\nServer connection closed. Exiting client.")
                client_socket.close()
                break
        except Exception as e:
            print(f"\nError receiving message: {e}")
            client_socket.close()
            break

def main():
    if len(sys.argv) < 2:
        print("Usage: client <Server IP Address>")
        sys.exit(1)
    server_ip = sys.argv[1]
    
    try:
        # Connect to the server
        client_socket = socket.create_connection((server_ip, SERVER_PORT))
        print(f"Connected to {server_ip} on port {SERVER_PORT}")

        # Start the listener thread
        listener_thread = threading.Thread(target=listen_for_messages, args=(client_socket,))
        listener_thread.daemon = True  # Ensure listener thread exits when main program exits
        listener_thread.start()

        while True:
            
            data = data_queue.get(timeout=0.5)
            if data == "shutdown":
                client_socket.close()
                break
            
            user_input = input("\nC: ")
            client_socket.send(user_input.encode())

            # If the user sent QUIT, close the connection and exits
            if user_input.strip().upper() == "QUIT":
                print("200 OK")
                break

    except Exception as e:
        pass

if __name__ == "__main__":
    main()
