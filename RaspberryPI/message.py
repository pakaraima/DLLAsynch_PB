import uuid
import datetime
class Message:
    """
        Message class definitions to logging
    """
    def __init__(self, message_body:str, mac_address:str, sensor_id:str, sensor_type:str, sensor_data_type:str, interval:int, msg_count:int):
        self.message_id = uuid.uuid4().__str__()
        self.device_id = mac_address
        self.sensor_id = sensor_id   
        self.sensor_type = sensor_type
        self.sensor_data_type = sensor_data_type
        self.sensor_interval = interval     
        self.message = message_body
        self.time_stamp = datetime.datetime.utcnow().__str__()
        self.msg_count = msg_count

    def __str__(self):
        return "Message Id:" + self.message_id + \
               " Device Id: " + self.device_id +  \
               " Sensor Id: " + self.sensor_id +  \
               " Sensor Type: " + self.sensor_type +  \
               " Sensor Data Type: " + self.sensor_data_type +  \
               " Sensor Interval: " + str(self.sensor_interval) +  \
               " Message: " + self.message +      \
               " TimeStamp: " + self.time_stamp + \
               " MsgCount: " + str(self.msg_count)
    def __repr__(self):
        return self.__str__()

def main(message:Message):
   l = message.__dict__
#    print(l) 
   print(message.__str__())

if __name__ == '__main__':
    message = Message("Test", "123", "123","Pulse", "String", 30)
    main(message)

