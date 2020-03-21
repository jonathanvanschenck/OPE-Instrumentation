import serial
import visa
import re

class Serial(serial.Serial):
    TERM = b''
    BUFFER_SIZE = 1000
    
    def __init__(self,*args,**kwargs):
        serial.Serial.__init__(self,*args,**kwargs)
        
        
    def query(self,msg):
        """Send query and away response
        Paramters
        ---------
        msg : str
        """
        self.write(msg.encode() + self.TERM)
        rmsg = self.read(self.BUFFER_SIZE)
        return rmsg.strip(self.TERM).decode()
    
    def shutdown(self):
        self.close()
