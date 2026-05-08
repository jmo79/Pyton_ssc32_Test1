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

    def MoveList(self,moves:list[ServoMove]):
        print("MoveServoListe")


class RobotMoveSequenceStatus(Enum):
    IDLE = auto()
    RUNNING  = auto()
    FINISHED  = auto()
    ERROR = auto()

class RobotMoveSequence:

    def __init__(self, SSC32ComRS232):
        self.SSC32ComRS232 = SSC32ComRS232
        self.status = RobotMoveSequenceStatus.IDLE
        self.step = 0
        self.current_pose_index=0
        self.start_request = False
        self.stop_request = False
        self.reset_cycle_request = False
        self.reset_all_request = False
        self.ton_step = mTimer.TON(20)

    def start(self, poses:list[list[ServoMove]]):
        self.poses = poses                  # recuperation de la liste de positions
        self.start_request = True           # demande de demmarage
    
    def stop(self):
        self.stop_request = False

    def reset_cycle(self):
        self.reset_cycle_request = True

    def reset_all(self):
        self.reset_all_request = True

    def _reset_cycle(self):
        self.step = 0
        self.current_pose_index = 0
        self.status = RobotMoveSequenceStatus.IDLE 

    def _reset_all(self):
        self.step = 0
        self.current_pose_index = 0
        self.status = RobotMoveSequenceStatus.IDLE 
        self.start_request = False
    
    def update(self):
        #ERROR
        #STOP
        #RESET
        #START
        #NORMAL RUN
        
        if self.reset_all_request:
            self.reset_all_request = False
            self._reset_all()
            return

        if self.reset_cycle_request and self.step == 6:
            self.reset_cycle_request = False
            self._reset_cycle()
            return

        match self.step:
            case 0: # Attente demarrage
                if self.start_request:
                    self.start_request = False
                    self.step = 1
                    self.current_pose_index = 0
  
            case 1: # commande de position
                pose = self.poses[self.current_pose_index]
                self.SSC32ComRS232.MoveJ(*pose)
                self.ton_step.reset()
                self.step = 2
            case 2: # petite attente avant envoi question mouvement (20ms)                
                self.ton_step.IN = True
                self.ton_step.update()
                if self.ton_step.DN:
                    self.step = 3    
            case 3: # commande Question mouvement en cours
                self.SSC32ComRS232.ComSerie.write(b"Q\r")
                self.ton_step.reset()
                self.step = 4
            case 4: # petite attente avant lecture reponse (20ms)                
                self.ton_step.IN = True
                self.ton_step.update()
                if self.ton_step.DN:
                    self.step = 5  
            case 5: # lecture reponse
                if self.SSC32ComRS232.ComSerie.in_waiting > 0:
                    resp = self.SSC32ComRS232.ComSerie.read(1).decode()
                    if resp == ".":     # reponse Mvt treminée
                        self.current_pose_index += 1
                        print("Class Mouvement terminé n°:" + str(self.current_pose_index) +"/" + str(len(self.poses)) )
                        if self.current_pose_index >= len(self.poses):
                            print("Class Sequence terminé")
                            self.step = 6 
                        else:
                            self.step = 1 

                    else:      # pas de reponse Mvt
                        self.step = 2 
            case 6: # sequence terminée
                pass


        if self.step == 0:
            self.status = RobotMoveSequenceStatus.IDLE    
        elif self.step == 6:
            self.status = RobotMoveSequenceStatus.FINISHED   
        else:
            self.status = RobotMoveSequenceStatus.RUNNING



 ################## Test Module   

if __name__=="__main__":
    R1ComRS232 = SSC32ComRS232()
    r1_move_sequence_pick = RobotMoveSequence(R1ComRS232)
    R1ComRS232.CommStart()
    time.sleep(1)
    #R1ComRS232.MoveJ_Init()

    pose1 = [ServoMove(ServoId.P00,90,300),
            ServoMove(ServoId.P01,145,500),
            ServoMove(ServoId.P02,145,500),
            ServoMove(ServoId.P03,45,500),
            ServoMove(ServoId.P04,90,500),
            ServoMove(ServoId.P05,90,500)]
    
    pose2 = [ServoMove(ServoId.P00,90,300),
            ServoMove(ServoId.P01,90,500),
            ServoMove(ServoId.P02,90,500),
            ServoMove(ServoId.P03,0,500),
            ServoMove(ServoId.P04,00,1000),
            ServoMove(ServoId.P05,20,1000)]
    
    poses_pick = [pose1,pose2,pose1,pose2]
    poses_place = [pose1,pose2,pose1,pose2]


    r1_move_sequence_pick.start(poses_pick)
    end_prog_2 = False 
    while not end_prog_2: 
        r1_move_sequence_pick.update()       

        if r1_move_sequence_pick.status == RobotMoveSequenceStatus.FINISHED:
            i +=1
            r1_move_sequence_pick.reset_cycle()
            r1_move_sequence_pick.start(poses_pick)
            print("cyle:"+ str(i)+"/500")

       
        if i == 500:
            end_prog_2 = True   

        time.sleep(0.1)

    
    
    
    R1ComRS232.CommStop()


