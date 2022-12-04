from time import sleep_ms

from romi import Romi, emergency_stop
from romi_tools import generate_ramp, generate_plateau


def mode_detection():
    robot = Romi()
    speed = 20
    while (True):
        r_c = robot.left_contact_state()
        l_c = robot.right_contact_state()
        if r_c == False and l_c == False:
            robot.right_wheel_command(speed)
            robot.left_wheel_command(speed)            
        if r_c == True :
            robot.right_wheel_command(-speed)
            robot.left_wheel_command(speed)
            sleep_ms(800)
        elif l_c == True :
            robot.right_wheel_command(speed)
            robot.left_wheel_command(-speed)
            sleep_ms(1200)
        
        sleep_ms(10)
        
def mode_pseudo_regulated():
    robot = Romi()
    seuil_delta = 10
    speed = 30
    objectif = 10000
    position_gauche = robot.left_coder_position()
    position_droite = robot.right_coder_position()
    
    while (position_gauche < objectif):
        position_gauche = robot.left_coder_position()
        position_droite = robot.right_coder_position()
        delta =  position_gauche - position_droite
        if delta > seuil_delta:
            robot.right_wheel_command(speed)
            robot.left_wheel_command(0)
        elif delta < -seuil_delta:
            robot.right_wheel_command(speed)
            robot.left_wheel_command(0)
        else:
            robot.right_wheel_command(0)
            robot.left_wheel_command(speed)
        
    while True:
        robot.right_wheel_command(0)
        robot.left_wheel_command(0)
        
        
def mode_regulated_speed():
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

if __name__=="__main__":
    emergency_stop()
    mode_pseudo_regulated()
    mode_detection()
    mode_regulated_speed()
    
    
