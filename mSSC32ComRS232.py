import serial
import time
import math
from typing import Optional
from enum import Enum, auto
from dataclasses import dataclass
import mTimer
#600 0°
#1500 90°
#2400 180°
ServoNbPoint_0Deg = 600
ServoNbPoint_180Deg = 2400

#AXE1 : rotation base
#AXE2 : rotation epaule 135 --> part vers l'arrier
#AXE3 : rotation bras 135 --> plié de a 45°
#AXE4 : rotation main 90° aligné avec le bras, 0° plié pour pendulaire
#AXE5 : rotation poignet
#AXE6 : ouverture fermeture pince
R1_HEIGHT_GROUND_TO_AXE2 = 75   # base a AXE2
R1_SHOULDER_LENGTH = 157      # AXE2 a AXE3
R1_ARM_LENGTH = 157           # AXE3 a AXE4
R1_AXIS4_TO_GRIPPER = 100        # AXE4 a bout de pince  
R1_CIRCLE_AREA_MIN = 100
R1_CIRCLE_AREA_MAX = 250
R1_CIRCLE_ANGLE_MIN = -90
R1_CIRCLE_ANGLE_MAX = 90

SERVO1_OFFSET_DEG= 90   

servoP00_calib = [
    (35, 12.5),
    (45, 24.5),
    (67.5, 58),
    (90, 85)
]

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

def linear_piecewise(setpoint_deg:float, calib_table:list):
    for i in range(len(calib_table) - 1):
        c1, v1 = calib_table[i]
        c2, v2 = calib_table[i+1]

        if c1 <= setpoint_deg <= c2:
            t = (setpoint_deg - c1) / (c2 - c1)
            return v1 + t * (v2 - v1)

    return calib_table[-1][1]

@dataclass
class ServoMoveXYZ:
    x: float
    y: float
    z: float
    speed: int

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
        
    def MoveXYZ(self,p:ServoMoveXYZ):
        theta1 = math.atan2(p.y, p.x)
        angle_servo1 = math.degrees(theta1) + SERVO1_OFFSET_DEG

        r = math.sqrt(p.x**2 + p.y**2)   
        z = p.z + R1_AXIS4_TO_GRIPPER - R1_HEIGHT_GROUND_TO_AXE2
        d = math.sqrt(r**2 + z**2)
        cos_theta3 = (R1_SHOULDER_LENGTH**2 + R1_ARM_LENGTH**2 - d**2) / (2 * R1_SHOULDER_LENGTH * R1_ARM_LENGTH)
        theta3 = math.acos(cos_theta3)
        angle_servo3 = 180 - math.degrees(theta3)

        theta2_triangle_r_z = math.atan2(z,r)
        cos_theta2_triangle_shoulder_d = (R1_SHOULDER_LENGTH**2 + d**2 - R1_ARM_LENGTH**2) / (2 * R1_SHOULDER_LENGTH * d)
        theta2_Trianger_shoulder_d = math.acos(cos_theta2_triangle_shoulder_d)
        theta2 = theta2_triangle_r_z + theta2_Trianger_shoulder_d
        angle_servo2 = math.degrees(theta2)

        theta4_sum = (theta2 + theta3 )
        theta4 = math.pi-theta4_sum
        angle_servo4 = math.degrees(theta4)

                 

        print("tetha1: " + str(math.degrees(theta1)))
        print("tetha2: " + str(math.degrees(theta2)))
        print("tetha3: " + str(math.degrees(theta3)))
        print("tetha4: " + str(math.degrees(theta4)))

        print("AxeServo1: " + str(angle_servo1))
        print("AxeServo2: " + str(angle_servo2))
        print("AxeServo3: " + str(angle_servo3))
        print("AxeServo4: " + str(angle_servo4))
        cmd = StrServoMove(ServoMove(ServoId.P00,int(angle_servo1),p.speed), 
                            ServoMove(ServoId.P01,int(angle_servo2),p.speed),
                            ServoMove(ServoId.P02,int(angle_servo3),p.speed),
                            ServoMove(ServoId.P03,int(angle_servo4),p.speed),
                            )

        if self.ComSerie is not None:
            self.ComSerie.write(cmd.encode())
            print("MoveXYZ")
        pass




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
    time.sleep(0.1)
    #R1ComRS232.MoveJ_Init()

    pose0 = [ServoMove(ServoId.P00,90,300), 
        ServoMove(ServoId.P01,90,500),
        ServoMove(ServoId.P02,90,500),
        ServoMove(ServoId.P03,90,500),
        ServoMove(ServoId.P04,90,500),
        ServoMove(ServoId.P05,90,500)]

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
    i=0
    end_prog_2 = True 
    while not end_prog_2: 
        r1_move_sequence_pick.update()       

        if r1_move_sequence_pick.status == RobotMoveSequenceStatus.FINISHED:
            i +=1
            r1_move_sequence_pick.reset_cycle()
            r1_move_sequence_pick.start(poses_pick)
            print("cyle:"+ str(i)+"/10")

       
        if i == 10:
            end_prog_2 = True   

        time.sleep(0.1)

    R1ComRS232.MoveJ(*pose0)

    #R1ComRS232.MoveXYZ(ServoMoveXYZ(270,0,80,250))
    time.sleep(6)
  #  R1ComRS232.MoveXYZ(ServoMoveXYZ(150,0,10,180))

    #R1ComRS232.MoveXYZ(ServoMoveXYZ(150,0,10,250))





    
    
    R1ComRS232.CommStop()


