from urrobot import URRobot
from urrobot import URRobot
import sys


# Initialize the Robot
UR5 = URRobot("10.103.0.202")
UR5.load_config_filename('config.xml')

UR5.connect_to_robot()
UR5.setup_recipes()

# Setpoints to move the robot to
point1 = [-0.12, -0.43, 0.14, 0, 3.11, 0.04]
point2 = [-0.12, -0.51, 0.21, 0, 3.11, 0.04]

# start data synchronization
if not UR5.send_start():
    sys.exit()

i = 0
# control loop
while UR5.keep_running:
    # receive the current state
    UR5.state = UR5.get_current_state()

    if UR5.state is None:
        break

    # do something...
    output = [False, True, True, True, True, True, True, True]

    if i == 2:
        print("----------------------------------------------")
        print(UR5.get_setup("standard_digital_output_mask"))
        i += 1
    if i == 1:
        UR5.set_single_standard_digital_output_mask(0)
        i += 1
    if i == 0:
        UR5.set_list_standard_digital_output(output)
        print(UR5.get_setup("standard_digital_output_mask"))
        i += 1

    UR5.send(UR5.setup)
    # kick watchdog
    UR5.send(UR5.watchdog)

UR5.send_pause()

UR5.disconnect()
