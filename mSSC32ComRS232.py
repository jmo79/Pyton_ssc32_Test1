import serial
import time
from typing import Optional
from enum import Enum, auto
from dataclasses import dataclass

ServoNbPoint_0Deg = 600
ServoNbPoint_180Deg = 2100

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

def StrServoMove(unit:ServoUnit,*servos : ServoMove)->str:
    cmd = ""
    for s in servos:
        if unit == ServoUnit.Deg:
            pos = int(ServoNbPoint_0Deg + (s.pos / 180) * (ServoNbPoint_180Deg - ServoNbPoint_0Deg))
        else:
            pos = s.pos
        cmd += f"#{s.id.value}P{pos}S{s.speed}\r"
    return(cmd)


def StrServoMoveBis(servos: list[ServoMove])->str:
    cmd = ""
    for s in servos:
        cmd += f"#{s.id.value}P{s.pos}S{s.speed}"
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

    def Cmd1(self):
        cmd = "#1P1800S250#2P1700S250#3P1000S250#4P1000S250#5P1000S250\r"
        if self.ComSerie is not None:
            self.ComSerie.write(cmd.encode())
            print("Commande Mvt1 envoyée au servos")

    def MoveJ(self,*servos : ServoMove):
        cmd = StrServoMove(ServoUnit.Deg,*servos)
        if self.ComSerie is not None:
            self.ComSerie.write(cmd.encode())
            print("MoveJ")
            return(cmd)


    def MoveJb(self, servos: list[ServoMove]):
        cmd = ""
        for s in servos:
            cmd += f"#{s.id.value}P{s.pos}S{s.speed}"




if __name__=="__main__":
    R1ComRS232 = SSC32ComRS232()
    R1ComRS232.CommStart()
    R1ComRS232.Cmd1()
    time.sleep(5)
    

    print(StrServoMove(ServoUnit.Point,ServoMove(ServoId.P00,1000,250),ServoMove(ServoId.P02,1000,250)))
    print(StrServoMove(ServoUnit.Deg,ServoMove(ServoId.P00,80,250),ServoMove(ServoId.P02,90,250)))

    print("class")
    print( R1ComRS232.MoveJ(ServoMove(ServoId.P03,90,500),ServoMove(ServoId.P04,90,500)) )

    print(StrServoMoveBis([ServoMove(ServoId.P03,1000,20),ServoMove(ServoId.P04,1000,20)]))

    time.sleep(5)

    R1ComRS232.CommStop()


