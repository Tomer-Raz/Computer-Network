import socket
import threading


HOST="127.0.0.1"
PORT=12345

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(f'{message}')
            else:
                print('Connection break')
                break
        except ConnectionRefusedError:
            print("Connection failed")
            break


def start_client():
    client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print(f"connected to server in :{HOST} : {PORT}")
    except:
        print("Connection failed")
        return
    name = input("Enter your name: ")
    client_socket.send(name.encode('utf-8'))

  
#Starting a second thread. 
    recieve_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    recieve_thread.daemon = True
    recieve_thread.start()

    print("Start chating.Enter your messange and press Enter")
    print("To exit from chat, enter 'exit' ")
  #main loop
  #loop for send massenges
    while True:
        msg = input()
        if (msg.lower() == 'exit'):
            client_socket.close()
            break
        client_socket.send(msg.encode('utf-8'))
    
     


if __name__ == '__main__':
    start_client()
