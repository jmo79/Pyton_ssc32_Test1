from enum import Enum, auto
from mTypes import RobotExchange
from mWorkplaces import WorkplaceManagement


class Rob1State(Enum):
    IDLE = auto()
    PICK_HOME_TO_PICK = auto()
    PICK_PICK_TO_HOME = auto()
    PLACE_HOME_TO_PLACE = auto()
    PLACE_PLACE_TO_HOME = auto()

class Rob1Management:
    def __init__(self,Rob:RobotExchange,WkPick:WorkplaceManagement,WkPlace:WorkplaceManagement):
        self.Rob = Rob
        self.WkPick = WkPick
        self.WkPlace = WkPlace
        self.GripperClose = False
        self.state =Rob1State

    def update(self):

        match self.State:
            case Rob1State.IDLE:
                if self.WkPick.Cmd.WorkRequest:
                    self.State = Rob1State.PICK_HOME_TO_PICK
                elif self.WkPlace.Cmd.WorkRequest:
                    self.State = Rob1State.PLACE_HOME_TO_PLACE

            case Rob1State.PICK_HOME_TO_PICK:
                self.TrajHomeToPick()
                self.GripperClose = True
                self.State = Rob1State.PICK_PICK_TO_HOME

            case Rob1State.PICK_PICK_TO_HOME:
                self.TrajPickToHome()
                self.WkPick.Cmd.WorkRequest = False
                self.State = Rob1State.IDLE

            case Rob1State.PLACE_HOME_TO_PLACE:
                self.TrajHomeToPlace()
                self.GripperClose = False
                self.State = Rob1State.PLACE_PLACE_TO_HOME

            case Rob1State.PLACE_PLACE_TO_HOME:
                self.TrajPlaceToHome()
                self.WkPlace.Cmd.WorkRequest = False
                self.State = Rob1State.IDLE
        

    
    def TrajHomeToPick(self):
        
        pass

    def TrajPlace(self):
        pass

    def TrajPick(self):
        pass




if __name__=="__main__":
    print("Start")

    IdRob1_Wk1Pick=0
    IdRob1_Wk2Place=1
    IdRob1_Wk3Waste=2

    Rob1Exchange = RobotExchange()
    Wk1Pick = WorkplaceManagement(Rob1Exchange,IdRob1_Wk1Pick)
    Wk2Place = WorkplaceManagement(Rob1Exchange,IdRob1_Wk2Place)

    Rob1 = Rob1Management(Rob=Rob1Exchange,WkPick=Wk1Pick,WkPlace=Wk2Place)

    
 
    
 
    print("Fin test")