from modules.linear_space import SmartCoordinate, SmartVector

class HuntWumpusStateCustom(object):
    """
    describe the state of a Hunt the Wumpus game with 
    any environment description 
    """
    
    @staticmethod
    def get_state_space_size():
        loc_x_bit_size = 3
        loc_y_bit_size = 3
        orientation_bit_size = 2
        grabbed_gold_bit_size = 1
        arrow_available_bit_size = 1
        wumpus_alive_bit_size = 1
        scream_bit_size = 1
        climbed_out_bit_size = 1
        
        return 2**(loc_x_bit_size + loc_y_bit_size + orientation_bit_size + grabbed_gold_bit_size + arrow_available_bit_size + wumpus_alive_bit_size + scream_bit_size + climbed_out_bit_size)
    
    def __init__(self, agent_location=SmartCoordinate(0, 0), agent_orientation=SmartVector(0, 1), is_arrow_available=True, has_agent_grabbed_gold=False, is_wumpus_alive=True, is_agent_hearing_scream=False, has_agent_climbed_out=False):
        self.agent_location = SmartCoordinate(0, 0)
        self.agent_orientation = SmartVector(0, 1)
        self.is_arrow_available = is_arrow_available
        self.has_agent_grabbed_gold = has_agent_grabbed_gold
        self.is_wumpus_alive = is_wumpus_alive
        self.is_agent_hearing_scream = is_agent_hearing_scream
        self.has_agent_climbed_out = has_agent_climbed_out
        
    def get_index(self):
        
        loc_x = ((str(bin(self.agent_location.x)))[2:]).zfill(3)
        loc_y = ((str(bin(self.agent_location.y)))[2:]).zfill(3)
        
        orientation_index = 0
        
        if self.agent_orientation.x == 0 and self.agent_orientation.y == 1:
            orientation_index = 0
        elif self.agent_orientation.x == 1 and self.agent_orientation.y == 0:
            orientation_index = 1
        elif self.agent_orientation.x == 0 and self.agent_orientation.y == -1:
            orientation_index = 2
        elif self.agent_orientation.x == -1 and self.agent_orientation.y == 0:
            orientation_index = 3
        
        orientation = ((str(bin(orientation_index)))[2:]).zfill(2)
        arrow = str(bin(self.is_arrow_available))[2:]
        gold = str(bin(self.has_agent_grabbed_gold))[2:]
        wumpus_alive = str(bin(self.is_wumpus_alive))[2:]
        scream = str(bin(self.is_agent_hearing_scream))[2:]
        climb_out = str(bin(self.has_agent_climbed_out))[2:]
        
        binary_repr = "".join([loc_x, loc_y, orientation, arrow, gold, wumpus_alive, scream, climb_out])

        return int(binary_repr, 2)