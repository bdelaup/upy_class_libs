from time import time_ns

# duration in s
# rate in growth / s
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
        if time > duration:
            return None
        else:
            return  round(initial_position)

    return lambda t : plateau(t)


def test_positions():    
    ramp_inc = generate_ramp(0, 10, 4)
    plateau = generate_plateau(40,2)
    ramp_dec = generate_ramp(40, -10, 4)
    t = 0
    val = ramp_inc(t)
    res=[]
    while val != None:
        res.append(val)
        # print(val)
        t = t+1
        val = ramp_inc(t)
        
    t = 0    
    val = plateau(t)
    while val != None:
        res.append(val)
        # print(val)
        t = t+1
        val = plateau(t)

    t = 0
    val = ramp_dec(t)
    while val != None:
        res.append(val)
        # print(val)
        t = t+1
        val = ramp_dec(t)
    ref = [0,10,20,30,40,40,40,40,40,30,20,10,0]

    # print (ref)
    # print (res)
    assert (res == ref)
    print("SUCCESS")


if __name__ == "__main__":
    test_positions()