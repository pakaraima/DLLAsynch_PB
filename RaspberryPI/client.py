import socket
import sys
import json
import datetime
import time


# Set up device readings
tempReading = {'Date':'','MsgId':'001','machineId':'001','sensorId':'001','sensorType':'Temp','Values':'30.1'}
message = json.dumps(tempReading)
message = message + '<EOF>'
#message = 'This is a test' + '<EOF>'
print >>sys.stderr, 'sending "%s"' % message
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.24', 11000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
#After the connection is established, data can be sent through the socket with sendall() and received with recv(), just as in the server.
try:
    
    #build device data
    msgCnt = 0
    while True:
       datetimeS = str(datetime.datetime.now()) 
       print ("DateTime",datetimeS) 
       tempReading['Date'] = str(datetime.datetime.now())
       tempReading['MsgId'] = str(msgCnt) 
       msgCnt += 1
       tempReading['Values'] = '4.0';
       message = json.dumps(tempReading)
       message = message + '<EOF>'
    #   message = 'This is a test' + '<EOF>'
    # Send data
    #message = 'This is the message.  It will be repeated.<EOF>'
       print >>sys.stderr, 'sending "%s"' % message
       sock.sendall(message)
       time.sleep(2)

    # Look for the response
       amount_received = 0
       amount_expected = len('OK')
    
       while amount_received < amount_expected:
          data = sock.recv(16)
          amount_received += len(data)
          print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

