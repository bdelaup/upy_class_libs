# Usage

```python
from encoder import Encoder
from motor import Motor
from pid import Filter
from setpoint_generator import generate_plateau, generate_ramp

def test_asservissement():
    pin_ch_a = Pin(27)
    pin_ch_b = Pin(26)
    encoder = Encoder(pin_ch_a, pin_ch_b)

    pin_dir = Pin(8)
    pin_speed = Pin(9)
    motor = Motor(pin_dir, pin_speed)
    motor.off()

    Kp = 1
    Ki = 0
    Kd = 0
    filter = Filter(Kp, Ki, Kd)

    controler = Controler(encoder, motor, filter)

    ramp_inc = generate_ramp(0, 100, 4)
    plateau = generate_plateau(400,2)
    ramp_dec = generate_ramp(400, -100, 4)

    controler.position_loop(ramp_inc)
    controler.position_loop(plateau)
    controler.position_loop(ramp_dec)
    motor.off()
```
