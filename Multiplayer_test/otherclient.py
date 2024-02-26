import socket
import os

"""
message = 'This is our message. It will be sent all at once'
def send_data(message):
    #try:

    # Send data
    print('sending : '+message)
    sent = sock.sendto(bytes(message, 'utf-8'), server_address)

    # Receive response
    print('waiting to receive')
    data, server = sock.recvfrom(4096)
    print('received {!r}'.format(data))

    #inally:
        #print('closing socket')
        #sock.close()
"""
os.system('cls' if os.name == 'nt' else 'clear')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)

def send_data(message):
    print('sending : '+message)
    sent = sock.sendto(bytes(message, 'utf-8'), server_address)

    print('waiting to receive')
    data = sock.recvfrom(4096)[0]
    print('received :{!r}'.format(data.decode()))




while True:
    send_data("next")