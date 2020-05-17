import socket

HOST = ''
PORT = 4041
MSG_DELIM = b'\0'
RCV_BYTES = 4096

def create_listen_socket(host, port):
    """ Setup the sockets our server will receive connection
    requests on """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)
    return sock

def recv_msg(sock):
    """ Wait for data to arrive on the socket, then parse into
    messages using MSG_DELIM as message delimiter """
    data = bytearray()
    msg = ''

    # Repeatedly read RCV_BYTES bytes off the socket, storing the bytes
    # in data until we see a delimiter
    while not msg:
        recvd = sock.recv(RCV_BYTES)
        if not recvd:
        # Socket has been closed prematurely
            raise ConnectionError()
        data = data + recvd

        if MSG_DELIM in recvd:
            # we know from our protocol rules that we only send
            # one message per connection, so MSG_DELIM will always be
            # the last character
            msg = data.rstrip(MSG_DELIM)

    msg = msg.decode('utf-8') 
    return msg

def prep_msg(msg):
    """ Prepare a string to be sent as a message """
    msg += MSG_DELIM.decode('utf-8')
    return msg.encode('utf-8')

def send_msg(sock, msg):
    """ Send a string over a socket, preparing it first """
    data = prep_msg(msg)
    sock.sendall(data)