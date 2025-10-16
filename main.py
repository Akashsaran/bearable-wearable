from enum import Enum

class messageType(Enum):
    000 = Connect
    001 = Set Tempo
    010 = Start
    011 = Stop
    100 = Alert

class conductorID(Enum):
    00 = 0
    01 = 1    
    10 = 2
    11 = 3