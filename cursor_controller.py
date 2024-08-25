import pyautogui

class CursorController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        pyautogui.FAILSAFE = False
        self.smoothing_factor = 0.5  
        self.prev_x, self.prev_y = pyautogui.position()

        self.x_min, self.x_max = 0.2, 0.8  
        self.y_min, self.y_max = 0.1, 0.9  

    def move_cursor(self, x, y):
        
        screen_x = self._map_coordinate(x, self.x_min, self.x_max, 0, self.screen_width)
        screen_y = self._map_coordinate(y, self.y_min, self.y_max, 0, self.screen_height)

        
        smooth_x = self.prev_x + (screen_x - self.prev_x) * self.smoothing_factor
        smooth_y = self.prev_y + (screen_y - self.prev_y) * self.smoothing_factor

        
        pyautogui.moveTo(smooth_x, smooth_y)

        
        self.prev_x, self.prev_y = smooth_x, smooth_y

    def _map_coordinate(self, value, in_min, in_max, out_min, out_max):
        
        mapped = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        return max(out_min, min(out_max, mapped))  