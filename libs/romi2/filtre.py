from romi_tools import CircularBuffer
class Filter:
    def __init__(self, kp=0):
        self._kp=kp
        self._order=0        
        self._proportional=0
        self._epsilon = 0
    
    @property
    def kp(self):
        return self._kp

    @kp.setter
    def kp(self, val):
        self._kp = val

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, sp):
        self._order=sp
        
    def set_signal(self, value):
        """
        update the input signal value
        """
#         print(self._order, value)
        self._epsilon = self._order-value
        
    def get_filtered_signal(self):
        """
        returns the filtered signal
        """
        val = self._kp * self._epsilon       
        return self._kp * self._epsilon
    
class Filter2:
    def __init__(self, kp=0, average_nb_values = 1):
        self._kp=kp
        self._order=0        
        self._proportional=0
        self._epsilon = 0
        if average_nb_values > 1:
            self._buf = CircularBuffer(average_nb_values,0)
        else:
            self._buf = None

    
    @property
    def kp(self):
        return self._kp

    @kp.setter
    def kp(self, val):
        self._kp = val

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, sp):
        self._order=sp
        
    def set_signal(self, value):
        """
        update the input signal value
        """
#         print(self._order, value)
        self._epsilon = self._order-value
        
    def get_filtered_signal(self):
        """
        returns the filtered signal
        """
        val = self._kp * self._epsilon
        if self._buf != None :
            self._buf.push(val)
            val = self._buf.average
        return val
    
class Filter3:
    def __init__(self, kp=0, ki = 0, kd = 0, average_nb_values = 1):
        self._kp=kp
        self._ki=ki
        self._kd=kd
     
        if average_nb_values > 1:
            self._buf = CircularBuffer(average_nb_values,0)
        else:
            self._buf = None        

        self._order=0
        self._epsilon = 0
        self._last_epsilon = 0
        self._epsilon_sum = 0
        
        self._last_time = 0
        self._time = 0

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, sp):
        self._order=sp
        
    def set_signal(self, value, time):
        """
        update the input signal value
        """
        self._last_epsilon = self._epsilon
        self._epsilon = self._order-value
        self._epsilon_sum += self._epsilon
        
        if (time != self._time):
            self.last_time = self._time
            self._time = time
        
    def get_filtered_signal(self):
        """
        returns the filtered signal
        """
        val = self._kp * self._epsilon +\
              self._ki * self._epsilon_sum +\
              self._kd * (self._epsilon_sum - self._last_epsilon) / (self._time - self.last_time)
        
        if self._buf != None :
            self._buf.push(val)
            val = self._buf.average
            
        return val