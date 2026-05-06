import serial
import time
from typing import Optional
from enum import Enum, auto
from dataclasses import dataclass
import mTimer
#600 0°
#1500 90°
#2400 180°
ServoNbPoint_0Deg = 600
ServoNbPoint_180Deg = 2400
i=0

class ServoUnit(Enum):
    Point = auto()
    Deg = auto()

class ServoId(Enum):
    P00 = 0     # rotation
    P01 = 1     # epaule
    P02 = 2     # bras
    P03 = 3     # poigné
    P04 = 4     # poigné rotation
    P05 = 5     # pince

@dataclass
class ServoMove:
    id: ServoId
    pos: float
    speed: int
    unit: ServoUnit = ServoUnit.Deg     # écriture de base en deg, spécifier si nécessaire l'unité en point

    @property
    def point(self) -> int:
        if self.unit == ServoUnit.Deg:
            return deg_to_point(self.pos)  
        return int(self.pos)

def deg_to_point(deg: float) -> int:
    return int( ServoNbPoint_0Deg + (deg / 180) * (ServoNbPoint_180Deg - ServoNbPoint_0Deg) )

def StrServoMove(*servos : ServoMove)->str:
    cmd = ""
    for s in servos:
        cmd += f"#{s.id.value}P{s.point}S{s.speed}"
    cmd += "\r"
    return(cmd)


def StrServoMoveBis(servos: list[ServoMove])->str:
    cmd = ""
    for s in servos:
        cmd += f"#{s.id.value}P{s.point}S{s.speed}"
    cmd += "\r"
    return(cmd)


def ScaleDegToServoPoint(deg: float) -> int: 
    deg = max(min(deg,180),0) 
    return int (ServoNbPoint_0Deg + (deg / 180) * (ServoNbPoint_180Deg - ServoNbPoint_0Deg))

class SSC32ComRS232:
    def __init__(self) -> None:
        self.ComSerie : serial.Serial | None = None
        pass

    def CommStart(self):
        self.ComSerie = serial.Serial('COM1', 115200, timeout=1)
        print("Start Communication")
        time.sleep(2)  # laisse le temps à la carte de démarrer

    def CommStop(self):
        print("Stop Communication")
        if self.ComSerie is not None:
            self.ComSerie.close()

    def MoveJ_Init(self):
        cmd = "#0P1800S250#1P1800S250#2P1700S250#3P600S250#4P1200S250#5P1000S250\r"
        if self.ComSerie is not None:
            self.ComSerie.write(cmd.encode())
            print("Commande Mvt1 envoyée au servos")

    def MoveJ(self,*servos : ServoMove):
        cmd = StrServoMove(*servos)
        if self.ComSerie is not None:
            self.ComSerie.write(cmd.encode())
            print("MoveJ")
            return(cmd)


    def MoveJb(self, servos: list[ServoMove]):
        cmd = ""
        for s in servos:
            cmd += f"#{s.id.value}P{s.pos}S{s.speed}"

 #   def RunSequence(self,moves: list[*servos : ServoMove]):
  #      for move in moves:






if __name__=="__main__":
    R1ComRS232 = SSC32ComRS232()
    R1ComRS232.CommStart()
    time.sleep(1)
    #R1ComRS232.MoveJ_Init()

    pose1 = (ServoMove(ServoId.P00,90,300),
            ServoMove(ServoId.P01,145,500),
            ServoMove(ServoId.P02,145,500),
            ServoMove(ServoId.P03,45,500),
            ServoMove(ServoId.P04,90,500),
            ServoMove(ServoId.P05,90,500))
    
    pose2 = (ServoMove(ServoId.P00,90,300),
            ServoMove(ServoId.P01,90,500),
            ServoMove(ServoId.P02,90,500),
            ServoMove(ServoId.P03,0,500),
            ServoMove(ServoId.P04,00,1000),
            ServoMove(ServoId.P05,20,1000))
    
    poses = [pose1,pose2,pose1,pose2]

    for pose in poses:          # NULLLLLLLLLLLLLLLLLLLLLLLLLL NULLLL
        step = 1
        match step:
            case 1: # commande de position
                R1ComRS232.MoveJ(*pose)
                step = 2
            case 2: # petite attente avant envoi question mouvement (20ms)
                tonStep2 = mTimer.TON(20)
                tonStep2.IN = True
                tonStep2.update()
                if tonStep2.DN:
                    step = 3    
            case 3: # commande Question mouvement en cours
                R1ComRS232.ComSerie.write(b"Q\r")
                step = 4
            case 4: # petite attente lecture reponse (20ms)
                tonStep2.reset()
                if tonStep2.DN:
                    step = 5  


      
    R1ComRS232.MoveJ(ServoMove(ServoId.P00,90,300),
                    ServoMove(ServoId.P01,145,500),
                    ServoMove(ServoId.P02,145,500),
                    ServoMove(ServoId.P03,45,500),
                    ServoMove(ServoId.P04,90,500),
                    ServoMove(ServoId.P05,90,500))
    
  
    
    while i<1000:
        R1ComRS232.MoveJ(*Pose1)
        time.sleep(3)
        
        R1ComRS232.MoveJ(*Pose2)
        
        #time.sleep(1.5)

        while True:
            R1ComRS232.ComSerie.write(b"Q\r")

            time.sleep(0.05)  # petite attente pour réponse

            if R1ComRS232.ComSerie.in_waiting > 0:
                resp = R1ComRS232.ComSerie.read(1).decode()

                print("Status:", resp)

                if resp == ".":
                    print("Mouvement terminé")
                    break

            time.sleep(0.2)

        i+=1
        print(i)


    
    R1ComRS232.CommStop()


