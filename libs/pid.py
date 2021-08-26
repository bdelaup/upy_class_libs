class Filter:
    def __init__(self, kp=0, ki=0, kd=0):
        self._kp=kp
        self._ki=ki
        self._kd=kd

        self._last_date=0
        self._set_point=0
        
        self._proportional=0
        self._derivative=0
        self._integral=0

        self._last_epsilon=0
        self._integral_accumulator=0
    
    @property
    def kp(self):
        return self._kp

    @kp.setter
    def kp(self, val):
        self._kp = val

    @property
    def ki(self):
        return self._ki

    @ki.setter
    def ki(self, val):
        self._ki = val

    @property
    def kd(self):
        return self._kd

    @kd.setter
    def kd(self, val):
        self._kd = val

    @property
    def set_point(self):
        return self._set_point

    @set_point.setter
    def set_point(self, sp):
        self._set_point=sp
        
        self._proportional=0
        self._derivative=0
        self._integral=0

        self._last_epsilon=0
        self._integral_accumulator=0


    def update(self, date:int, value)->None:
        epsilon = self._set_point-value

        # P
        self._proportional = self._kp * epsilon

        # I
        self._integral_accumulator = self._integral_accumulator + (epsilon + self._last_epsilon)/2 * (date - self._last_date)
        self._integral = self._ki * self._integral_accumulator 
        
        # D
        self._derivative = self._kp * (epsilon - self._last_epsilon) / (date - self._last_date)

        self._last_date=date
        self._last_epsilon=epsilon

    def get_driving_parameters(self):
        return (self._proportional, self._integral, self._derivative)

    def get_driving_value(self):
        return self._proportional + self._integral + self._derivative


