import time

def now_ms():
    return int(time.perf_counter() * 1000)

def create_ton(preset_ms):
    return {
        "IN": False,
        "PRE": preset_ms,
        "ET":0,
        "START": None,
        "DN": False
        
    }

def update_ton(t, current_time_ms):
    if t["IN"]:
        
        if t["START"] is None:
            t["START"] = current_time_ms

        t["ET"] = current_time_ms - t["START"]

        if t["ET"] >= t["PRE"]:
            t["Q"] = True
        else:
            t["Q"] = False

    else:
        t["START"] = None
        t["ET"] = 0
        t["Q"] = False

class TON:
    def __init__(self,preset_ms):
        self.IN=    False
        self.PRE=   preset_ms
        self.START= None
        self.DN=    False
        self.ET=    0
    
    def update(self, now_ms):
        if self.IN:
            if self.START is None:
                self.START = now_ms

            self.ET = now_ms - self.START

            if now_ms - self.START >= self.PRE:
                self.DN = True
        else:
            self.START = None
            self.DN = False