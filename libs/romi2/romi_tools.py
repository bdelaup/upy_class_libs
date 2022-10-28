class CircularBuffer :
    def __init__(self, size, initial_value):
        self._buffer = [initial_value]*size
        self._i = 0
        self._size = size
    
    def push(self, val):
        self._buffer[self._i] = val
        if self._i >= self._size -1:
            self._i = 0
        else :
            self._i = self._i + 1
            
    @property
    def buffer(self):
        return self._buffer
    
    @property
    def average(self):
        s = 0
        for val in self._buffer:
            s = s + val
        return s / self._size 
    

def generate_ramp(initial_position, rate, duration):
    def ramp(time):
        """time in s"""
        if time > duration:
            return None
        else:
            return  round(rate * time + initial_position)

    return lambda t : ramp(t)

# duration in ms
def generate_plateau(initial_position, duration):
    def plateau(time):
        """time in s"""
#         print("time",time, "duration", duration)
        if time > duration:
            return None
        else:
            return  round(initial_position)

    return lambda t : plateau(t)

