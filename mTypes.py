from dataclasses import dataclass, field
N=16

@dataclass
class RobotExchangeCmd:
    StopMovement : bool = False
    AccessAuthorization : list[bool] = field(default_factory = lambda:[False]*N)
    WorkRequest         : list[bool] = field(default_factory = lambda:[False]*N)

@dataclass
class RobotExchangeStsSystem:
    AutoActive : bool = False
    HomePositionOK : bool = False

@dataclass
class RobotExchangeSts:
    System : RobotExchangeStsSystem = field(default_factory=RobotExchangeStsSystem)
    WorkInProgress  : list[bool] = field(default_factory = lambda:[False]*N)
    WorkOK          : list[bool] = field(default_factory = lambda:[False]*N)
    WorkZoneFree      : list[bool] = field(default_factory = lambda:[False]*N)              # egal True si robot hors zone
    DynMonitoringActivated : list[bool] = field(default_factory = lambda:[False]*N)

@dataclass
class RobotExchange:
    Cmd : RobotExchangeCmd = field(default_factory=RobotExchangeCmd)
    Sts : RobotExchangeSts = field(default_factory=RobotExchangeSts)