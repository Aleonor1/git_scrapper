#!/usr/bin/python
import sys, socket
import echo_util
import threading
import time

HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = echo_util.PORT

def function():
    count = 0;
    while count<5:
        time.sleep(1)
        count+=1
    print("SARMALEEEEE")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("here")
except ConnectionError:
    print('Socket error on connection')
    sys.exit(1)

print('\nConnected to {}:{}'.format(HOST, PORT))
print("Type message, enter to send, 'q' to quit")

while True:
    msg = input()
    if msg == 'q': break
    try:
        echo_util.send_msg(sock, msg) # Blocks until sent
        print('Sent message: {}'.format(msg))
        msg = echo_util.recv_msg(sock)
            # Block until
            # received complete
            # message
        print('Received echo: ' + msg)
        #aici apel multi thread thread.start_new_thread(function())
    except ConnectionError:
        print('Socket error during communication')
        sock.close()
    print('Closed connection to server\n')
    break

print("Closing connection")
sock.close()