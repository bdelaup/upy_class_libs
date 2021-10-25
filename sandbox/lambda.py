
# def generate_ramp(initial_position, rate, duration):
#     def ramp(time):
#         if time > duration:
#             return False
#         else:
#             return  rate * time + initial_position

#     return lambda t : ramp(t)

# rampe1 = generate_ramp(0,2,1000)
# rampe2 = generate_ramp(0,3,1000)

# print(rampe1(1200))
# print(rampe2(50))


def test_yield():
    i = 0
    while i < 4:
        print(i)
        i+=1
        yield True
    return False


f = test_yield()
for i in f:
    print (i)

f = test_yield()
for i in f:
    print (i)
