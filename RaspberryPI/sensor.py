class Sensor:
    """
        Sensor class definitions
    """
    def __init__(self, sensor_id:str, sensor_type:str, sensor_data_type:str, sensor_interval:int):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.sensor_data_type = sensor_data_type
        self.sensor_interval = sensor_interval

def main(sensor:Sensor):
   l = sensor.__dict__
   print(l) 
#    print(sensor.__str__())

if __name__ == '__main__':
    sensor = Sensor("123","Pulse", "String", 30)
    main(sensor)