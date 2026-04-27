from enum import Enum
import time
import mTimer

class G7_Test_StepDef(Enum):
    E00_Init =      (0, "Init")
    E01_Stating =   (1, "Stating")
    E02 =           (2, "Step02")
    E03 =           (3, "Step02")
    E10_End =       (10, "End")
    E99_Error =     (99, "Error")

    def __init__(self,num,label):
        self.num = num  
        self.num = num  


class G7_Test:
    def __init__(self):   # creation de la structure G7
        self.G7=    G7_Test_StepDef.E00_Init
        self.MemStep = -1
        self.TrigNewStep = False
        self.StepTimer = mTimer.TON(60000)

    
    def update(self):

        # 1. détection de changement d'étape (FRONT)
        self.TrigNewStep = (self.G7.num != self.MemStep)

        # 2. gestion timer
        if self.TrigNewStep:
            self.StepTimer.IN = False   # reset propre
            self.StepTimer.update()

        self.StepTimer.IN = True
        self.StepTimer.update()



        match self.G7:
            case G7_Test_StepDef.E00_Init:
                if self.TrigNewStep:
                    print("Etape 0")
                if self.StepTimer.ET > 5000:
                    self.G7 = G7_Test_StepDef.E01_Stating  

            case G7_Test_StepDef.E01_Stating:
                if self.TrigNewStep:
                    print("Etape 1")
                if self.StepTimer.ET > 5000:
                    self.G7 = G7_Test_StepDef.E02

            case G7_Test_StepDef.E02:
                if self.TrigNewStep:
                    print("Etape 2")
                if self.StepTimer.ET > 5000:
                    self.G7 = G7_Test_StepDef.E03

            case G7_Test_StepDef.E03:
                if self.TrigNewStep:
                    print("Etape 3")
                if self.StepTimer.ET > 5000:
                    self.G7 = G7_Test_StepDef.E10_End
        """
        self.TrigNewStep = (self.G7.num != self.MemStep)
        self.StepTimer.IN = not self.TrigNewStep
        self.StepTimer.update()"""
        self.MemStep = self.G7.num



 
        




