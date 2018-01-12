import socket
import sys
import json
import logging
import time
from config import ConfigXmlParser
from message import Message


module_logger = logging.getLogger("ShaftersburryApp.senderModule")

class MessageSender:
    """
        Class reponsible for manage the message sending to from py to unity
    """
    def __init__(self, xmlConfigFile:str):   
        self.config = ConfigXmlParser(xmlConfigFile)
        self.host = self.config.server_ip        
        self.port = int(self.config.server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print("Host: " + self.host)     
        print("Port: " + str(self.port))

    def send_message(self, message:Message, close_connection:bool=False, log_enable:bool=False):  
        """
            Send a message to respective socket 
            Arguments: 
                Args:
                    param1 (self): The instance.
                    param2 (str): The message reading.
                    param3 (bool): Flag to close the connection after sending
        """                     
      
        
        print("Socket conncted on " + self.host + ":" + str(self.port))       
        message = json.dumps(message.__dict__) + "<EOF>" 
        try:
            self.sock.sendall(str.encode(message))
            print("Message sent: " + message)     
            if (log_enable):
                logger = logging.getLogger("ShaftersburryApp.sender.send_message")
                logger.info("Message Sent:" + message)


        finally:
            if(close_connection):
                print("Closing socket")
                self.sock.close()
                print("Socket closed")

    def recv_message(self,expected_len:2):
        amount_received = 0
        amount_expected = expected_len
        received = ""
        while amount_received < amount_expected:
            data = self.sock.recv(16)
            received += data.decode("utf-8")
            amount_received += len(data)
            print ('received "%s"' % data)
        return received

    def close_socket(self):
         self.sock.close()


if __name__ == '__main__':
    MESSAGE_SENDER = MessageSender("config.xml")
    received = "" 
    msgCount = 0  
    while received != "QT":
        msgCount += 1
        MESSAGE = Message("Test", \
	                          "1",  \
	                          MESSAGE_SENDER.config.sensors[0].sensor_id, \
	                          MESSAGE_SENDER.config.sensors[0].sensor_type, \
	                          MESSAGE_SENDER.config.sensors[0].sensor_data_type, \
                          MESSAGE_SENDER.config.sensors[0].sensor_interval,msgCount)	
        MESSAGE_SENDER.send_message(MESSAGE)
        received = MESSAGE_SENDER.recv_message(2)
#look for response
  
        time.sleep(0.500)

    MESSAGE_SENDER.close_socket()

    
    


# # Set up device readings
# tempReading = {'machineId':'001','sensorId':'001','sensorType':'Temp','Values':'30.1'}
# message = json.dumps(tempReading)
# message = message + '<EOF>'
# print ('sending "%s"' % message)
# # Create a TCP/)IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect the socket to the port where the server is listening
# server_address = ('localhost', 8010)
# print ('connecting to %s port %s' % server_address)
# sock.connect(server_address)
# #After the connection is established, data can be sent through the socket with sendall() and received with recv(), just as in the server.

# try:
    
#     #build device data
#     tempReading['Values'] = '4.0'
#     message = json.dumps(tempReading)
#     message = message + '<EOF>'
#     # Send data
#     #message = 'This is the message.  It will be repeated.<EOF>'
#     print ('sending "%s"' % message)
#     # sock.sendall(message)   
#     sock.sendall(str.encode(message))

#     # Look for the response
#     amount_received = 0
#     amount_expected = len(message)
    
#     # while amount_received < amount_expected:
#     #     data = sock.recv(16)
#     #     amount_received += len(data)
#     #     print ('received "%s"' % data)

# finally:
#     print  ('closing socket')
#     sock.close()

