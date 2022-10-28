from romi import Romi, emergency_stop
from romi_tools import generate_ramp, generate_plateau

if __name__=="__main__":
    emergency_stop()
#     test_asservissement_ch2_right_speed()
#     test_asservissement_ch1_left_speed()
#     test_asservissement_ch1ch2_speed()
    robot = Romi(kp_in=0.1, ki_in = 0.05, kd_in = 0.00001)
    
    ramp_inc = generate_ramp(0, 150, 2)
    plateau = generate_plateau(300,2)
    ramp_dec = generate_ramp(300, -300, 1)
    
    robot.move(ramp_inc, ramp_inc)
    robot.move(plateau, plateau)
    robot.move(ramp_dec, ramp_dec)