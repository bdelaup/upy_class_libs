import machine

p6 = machine.Pin(6)
p7 = machine.Pin(7)
p8 = machine.Pin(8)
p9 = machine.Pin(9)

p6.off()
p7.off()
p8.off()
p9.off()


machine.PWM(p6).duty_u16(0)
machine.PWM(p7).duty_u16(0)
machine.PWM(p8).duty_u16(0)
machine.PWM(p9).duty_u16(0)

print("hello")