from dataclasses import dataclass, field
from mTypes import RobotExchange
import mTimer



@dataclass
class WorkplaceCmd:
    reset : bool
    AccessAuthorization : bool
    WorkRequest: bool
    DynMonitoringActivated : bool

@dataclass
class WorkplaceLocal:
    Ton_SimulWorkOk : mTimer.TON    
        
class WorkplaceManagement:
    def __init__(self,Rob:RobotExchange,IdWkZone:int):
        # externe In/Out
        self.Rob = Rob
        self.IdWkZone = IdWkZone
        # interne In
        self.Cmd = WorkplaceCmd(reset=False,AccessAuthorization=False,WorkRequest=False,DynMonitoringActivated=False)
        self.Simul = False
        # interne  Out
        self.ErrorActive = False
        self.WorkInProgress = False
        self.WorkOk = False
        self.WorkZoneFree = False       
        # local
        self.Local = WorkplaceLocal(Ton_SimulWorkOk=mTimer.TON(3000))

    
    def update(self):
        # commande PLC -> Robot
        self.Rob.Cmd.AccessAuthorization[self.IdWkZone] = self.Cmd.AccessAuthorization
        self.Rob.Cmd.WorkRequest[self.IdWkZone] = self.Cmd.WorkRequest

        # Statut Robot -> PLC
        self.WorkInProgress = self.Rob.Sts.WorkInProgress[self.IdWkZone] or (self.Simul and self.Cmd.WorkRequest and not self.WorkOk)
        self.WorkOk = self.Rob.Sts.WorkOK[self.IdWkZone] or (self.Simul and self.Local.Ton_SimulWorkOk.DN)
        self.WorkZoneFree = self.Rob.Sts.WorkZoneFree[self.IdWkZone] or self.Simul

        # surveillance de mouvement
        if self.Cmd.DynMonitoringActivated and self.Rob.Sts.System.AutoActive:
            if not self.Cmd.AccessAuthorization and not self.WorkZoneFree:
                self.Rob.Cmd.StopMovement = True
                self.ErrorActive = True

        # local
        self.Local.Ton_SimulWorkOk.IN = self.WorkInProgress and self.Simul
        self.Local.Ton_SimulWorkOk.update()




if __name__=="__main__":
    print("Start")

    IdRob1_WkPick=0
    IdRob1_WkPlace=1
    IdRob1_WkWaste=2

    Rob1Exchange = RobotExchange()    
    Workplace1 = WorkplaceManagement(Rob1Exchange,IdRob1_WkPick)
    Workplace2 = WorkplaceManagement(Rob1Exchange,IdRob1_WkPlace)
    
    Workplace1.Cmd.WorkRequest = True  
    Workplace1.update()

    Workplace2.Cmd.WorkRequest = True
    Workplace2.update()
    print("zone Pick : "+ str(Rob1Exchange.Cmd.WorkRequest[IdRob1_WkPick]))
    print("zone Place : "+ str(Rob1Exchange.Cmd.WorkRequest[IdRob1_WkPlace]))
    
    
 
    print("Fin test")
    
 




    