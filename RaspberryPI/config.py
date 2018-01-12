import xml.etree.ElementTree as ET
from sensor import Sensor
import sys

class ConfigXmlParser(object):

    def __init__(self, xml_file_name):
        self.doc  = ET.parse(xml_file_name)
        self.root = self.doc.getroot()
        self.mac_address = self.root.find("MacAddress").text.strip().rstrip('\n').lstrip('\n')
        self.server_ip = self.root.find("UnityIPAddress").text.strip().rstrip('\n').lstrip('\n')
        self.server_port = self.root.find("UnityPort").text.strip().rstrip('\n').lstrip('\n')
        self.logging = self.root.find("Logging")
        self.logging_activate = self.root.find("Logging/Activate").text.strip().rstrip('\n').lstrip('\n')
        self.logging_path = self.root.find("Logging/File").text.strip().rstrip('\n').lstrip('\n')
        self.logging_mode = self.root.find("Logging/Mode").text.strip().rstrip('\n').lstrip('\n')
        self.sensors = self.get_sensors()
        
    def get_sensors(self):  
        """
            Return the sensors listed on the config files
            Arguments: 
                Args:
                    param1 (self): The instance.                  
            Return:
                (array) Sensor
        """
        sensors = []
        
        for x in self.root.find("Sensors"):
            sensor = Sensor(x.find("SensorId").text.strip().rstrip('\n').lstrip('\n'), \
                            x.find("Type").text.strip().rstrip('\n').lstrip('\n'), \
                            x.find("DataType").text.strip().rstrip('\n').lstrip('\n') ,\
                            int(x.find("Interval").text))           
            sensors.append(sensor)
        return sensors


    def test(self):       
        for child in self.root:
            print (child.tag, child.text)    

def main():
    parser = ConfigXmlParser("config.xml")
    l = vars(parser)
    print (l)

    #print([x for x in parser.sensors][0][0].text.rstrip('\n'))
    # parser.test()

if __name__ == '__main__':
    main()