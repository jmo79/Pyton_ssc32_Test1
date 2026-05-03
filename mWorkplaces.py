from dataclasses import dataclass, field
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

@dataclass
class RobotWorkplaceCmd:
    AccessAuthorization : bool = False
    WorkRequest: bool = False

@dataclass
class RobotExchangeCmd:
    StopMovement : bool
   # AccessAuthorization : bool
   # WorkRequest : bool
   # Workplaces: list[RobotWorkplaceCmd]
    wkPick : RobotWorkplaceCmd = field(default_factory=RobotWorkplaceCmd)
    wkPlace : RobotWorkplaceCmd = field(default_factory=RobotWorkplaceCmd)

@dataclass
class RobotExchangeStsSystem:
    AutoActive : bool = False
    HomePositionOK : bool = False

@dataclass
class RobotExchangeSts:
    System : RobotExchangeStsSystem = field(default_factory=RobotExchangeStsSystem)
    WorkInProgress : bool = False
    WorkOK : bool = False
    WorkZoneFree: bool = False              # egal True si robot hors zone
    DynMonitoringActivated : bool = False


@dataclass
class RobotExchange:
    Cmd : RobotExchangeCmd
    Sts : RobotExchangeSts
    
    @classmethod
    def create_default(cls):
        return cls(
            Cmd=RobotExchangeCmd(
                StopMovement= False,
                wkPick= RobotWorkplaceCmd(),
                wkPlace= RobotWorkplaceCmd()
            ), 
            Sts=RobotExchangeSts()
        )
        

class WorkplaceManagement:
    def __init__(self,Rob:RobotExchange,wkZone:str):
        # externe In/Out
        self.Rob = Rob
        self.wkZone = wkZone
        self.Zone = getattr(Rob.Cmd, wkZone)
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

    @property
    def ZoneCmd(self) -> RobotWorkplaceCmd:
        return getattr(self.Rob.Cmd, self.wkZone)
    
    def update(self):
        # commande PLC -> Robot
       # self.Rob.Cmd.AccessAuthorization = self.Cmd.AccessAuthorization
       # self.Rob.Cmd.WorkRequest = self.Cmd.WorkRequest
       #ZoneCmd()
   
      #  self.Zone.WorkRequest = self.Cmd.WorkRequest
        self.ZoneCmd.WorkRequest = self.Cmd.WorkRequest

        # Statut Robot -> PLC
        self.WorkInProgress = self.Rob.Sts.WorkInProgress or (self.Simul and self.Cmd.WorkRequest and not self.self.WorkOk)
        self.WorkOk = self.Rob.Sts.WorkOK or (self.Simul and self.Local.Ton_SimulWorkOk.DN)
        self.WorkZoneFree = self.Rob.Sts.WorkZoneFree or self.Simul

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
    Rob1Exchange = RobotExchange.create_default()

    
    Workplace1 = WorkplaceManagement(Rob1Exchange,"wkPick")
    Workplace2 = WorkplaceManagement(Rob1Exchange,"wkPlace")
    Workplace1.Cmd.WorkRequest = True
    Workplace1.update()
    print("zone Pick : "+ str(Rob1Exchange.Cmd.wkPick.WorkRequest))
    print("zone Place : "+ str(Rob1Exchange.Cmd.wkPlace.WorkRequest))
    
    
    """

    Workplace1.Cmd.WorkRequest = False;
    Workplace1.update();
    print(Rob1Exchange.Cmd.WorkRequest)
    """
    print("Fin test")
    
 




    