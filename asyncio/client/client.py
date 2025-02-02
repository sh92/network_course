import asyncio
import sys
import time
import os
from calc_md5 import md5Check
from concurrent.futures import ProcessPoolExecutor
import socket

client_mtu='576'
arg_lens = len(sys.argv)
filePath = ''
if arg_lens <2: 
    print( '[filePath] [Client mtu] ')
    print( '[filePath] ')
    sys.exit()
elif arg_lens ==2:
  filePath = sys.argv[1]
else:
  filePath = sys.argv[1]
  client_mtu = sys.argv[2]

fileSize = os.path.getsize(filePath) 


buffer_size= int(client_mtu)

server_ip ='127.0.0.1'
server_port = 5555


@asyncio.coroutine
def tcp_echo_client(data,loop):
    reader, writer = yield from asyncio.open_connection(server_ip, server_port,loop=loop)
    while True:
        writer.write(data)
        d= yield from reader.read(100) 
        decoded_data = d.decode('utf-8')
        #print('Received: %r' % decoded_data)
        if(decoded_data == 'ok'):
             break
    writer.close()
    


def recv_message(message_socket):
     message = message_socket.recv(4096).decode()
     print( "Buffer size is ",message)
     buffer_size = int(message)

ip_address = '127.0.0.1'
port_number  = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip_address, port_number))
client_socket.send(str(client_mtu).encode())
recv_message(client_socket)
client_socket.close()



start_time = time.time()
loop = asyncio.get_event_loop()


remain=fileSize
with open(filePath, 'rb') as f:
     while True:
          if remain >= buffer_size:
             remain -=buffer_size
             data = f.read(buffer_size)
             loop.run_until_complete(tcp_echo_client(data,loop))
          else:
             data = f.read(remain)
             loop.run_until_complete(tcp_echo_client(data,loop))
             break


print('Close the socket')
loop.close()

end_time = time.time()
print("Time elapsed : ", end_time - start_time)

m = md5Check(filePath)
print("checksum: "+m.check_md5())
