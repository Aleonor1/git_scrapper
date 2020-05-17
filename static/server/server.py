import echo_util
import threading
import compareAction
import time
from myapp.views import views

HOST = echo_util.HOST
PORT = echo_util.PORT

def Diff(li1, li2):
    return set(li1-li2)

def handle_client(sock, addr):
    """ Receive data from the client via sock and echo it back """
    msg = echo_util.recv_msg(sock) # Blocks until received
    i = 0
    while True:
            print('{}: {}'.format(addr, msg))
            print('msg=',msg)
            array1 = compareAction.newSearch(msg)
            views.sendMail("sarma")
            print(type(array1))
            time.sleep(600) #reprezinta timpul intre cele doua verificari - 600 secunde adica o ora
            array2 = compareAction.newSearch(msg)
            print(Diff(array2,array1))

listen_sock = echo_util.create_listen_socket(HOST, PORT)
addr = listen_sock.getsockname()
print('Listening on {}'.format(addr))
while True:
    client_sock, addr = listen_sock.accept()
    thread = threading.Thread(target = handle_client, args = [client_sock, addr], daemon=True)
    thread.start()
    print('Connection from {}'.format(addr))

def printToFile(li1):
    f = open("demofile2.txt", "a")
    #print (len(li1))
    if len(li1)>0:
        f.write(', '.join(li1))
