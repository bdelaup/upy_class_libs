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
        

    def update(self, date:int, value)->None:
        
        epsilon = self._set_point-value

        # P
        self._proportional = self._kp * epsilon

#         # I
#         self._integral_accumulator = self._integral_accumulator + epsilon * (date - self._last_date)
#         self._integral = self._ki * self._integral_accumulator 
#         
#         # D
#         if date != self._last_date:
#             self._derivative = self._kd * (epsilon - self._last_epsilon) / (date - self._last_date)

        self._last_date=date
        self._last_epsilon=epsilon
#         print ("Consigne : ", self._set_point, "Position : ", value, "Epsi : ", epsilon, "P : ", self._proportional)

    def get_driving_parameters(self):
        return (self._proportional, self._integral, self._derivative)

    def get_driving_value(self):
        return self._proportional #+ self._integral + self._derivative


def test_filter_p():
    filter = Filter(3, 0, 0)

    filter.set_point = 10
    filter.update(0, 0)
    filter.update(1, 1)
    cmd = filter.get_driving_value()
    assert(cmd == 27)
    
    filter.update(2, 20)
    cmd = filter.get_driving_value()
    assert(cmd == -30)

    print("SUCCESS")   

def test_filter_i():
    filter = Filter(0, 3, 0)

    filter.set_point = 10
    filter.update(1, 0)
    cmd = filter.get_driving_value()
    # print (cmd)
    assert(cmd == 30)

    filter.update(2, 1)
    cmd = filter.get_driving_value()
    # print (cmd)
    assert(cmd == 57)

    filter.update(3, 10)
    cmd = filter.get_driving_value()
    # print (cmd)
    assert(cmd == 57)

    filter.update(4, 20)
    cmd = filter.get_driving_value()
    # print (cmd)
    assert(cmd == 27)
    
    filter.update(5, 50)
    cmd = filter.get_driving_value()
    # print (cmd)
    assert(cmd == -93)

    print("SUCCESS")    

def test_filter_d():
    filter = Filter(0, 0, 3)

    filter.set_point = 10
    filter.update(1, 0)
    cmd = filter.get_driving_value()
    # print (cmd)
    assert(cmd == 30)

    filter.update(2, 0)
    cmd = filter.get_driving_value()
    # print (cmd)
    assert(cmd == 0)

    filter.update(3, 10)
    cmd = filter.get_driving_value()
    # print (cmd)
    assert(cmd == -30)

    filter.update(4, 20)
    cmd = filter.get_driving_value()
    # print (cmd)
    assert(cmd == -30)
    
    filter.update(5, 50)
    cmd = filter.get_driving_value()
    # print (cmd)
    assert(cmd == -90)

    print("SUCCESS")         

if __name__ == "__main__" :
    test_filter_p()
    test_filter_i()
    test_filter_d()