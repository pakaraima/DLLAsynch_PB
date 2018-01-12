import logging
import sender as SenderModule
from message import Message

def main():
    """
    The main entry point of the application
    """
    sender = SenderModule.MessageSender("config.xml")
    logger = logging.getLogger("ShaftersburryApp")
    logger.setLevel(logging.INFO)

    fh =  logging.FileHandler(sender.config.logging_path,sender.config.logging_mode)
    formatter = logging.Formatter('%(asctime)s - %(name)-36s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.info("Program Started")

    message = Message("Test", \
                    "1",  \
                    sender.config.sensors[0].sensor_id, \
                    sender.config.sensors[0].sensor_type, \
                    sender.config.sensors[0].sensor_data_type, \
                    sender.config.sensors[0].sensor_interval)
    sender.send_message(message, log_enable=True)

    logger.info("Program Finished!")



if __name__ == "__main__":
    main()
