import numpy as np
import rospy
import airsim

import nav_msgs.msg
import geometry_msgs.msg

rospy.init_node("path_processing", anonymous=True)

# destination = np.array([-1.0, -1.0, -1.0])
# destination = None
path = []

def path_callback(msg):
    # global destination
    global path
    path = []
    position = msg.poses[1].pose.position
    print(len(msg.poses), position.x, position.y, position.z, end='\r')
    # if len(msg.poses) > 0:
    #     destination = np.array([position.x, position.y, position.z])
    for i in range(len(msg.poses)):
        waypoint = msg.poses[i].pose.position
        path.append([waypoint.x, waypoint.y, waypoint.z])

rospy.Subscriber("/waypoint_path", nav_msgs.msg.Path, callback=path_callback, queue_size=1)

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

client.takeoffAsync().join()
print("Taken Control of the UAV")

control_freq = 60 # control update frequency in hertz
path_following_rate = rospy.Rate(control_freq) # Once a second
base_speed = 5
control_period = 1/control_freq

while not rospy.is_shutdown():
    # if destination[2] != -1.0:
    #     print("Flying towards", destination[0], destination[1], destination[2], end='\r')
    #     displacement = destination-current_position
    #     direction = displacement/np.sqrt(np.sum(displacement**2))
    #     velocity = base_speed*direction
    #     client.moveByVelocityAsync(velocity[0], velocity[1], velocity[2], control_period)
        # client.moveToPositionAsync(x=destination[0], y=destination[1], z=destination[2], velocity=base_speed).join()
    if len(path) > 0:
        estimate = client.getMultirotorState().kinematics_estimated.position
        current_position = np.array([estimate.x_val, estimate.y_val, estimate.z_val])
        waypoint_index = 0
        next_waypoint = np.asarray(path[waypoint_index])
        last_waypoint = np.asarray(path[-1])
        while (np.linalg.norm(current_position-last_waypoint) <
               np.linalg.norm(next_waypoint-last_waypoint) and waypoint_index < len(path)):
            waypoint_index += 1
            next_waypoint = np.asarray(path[waypoint_index])
        print(next_waypoint, end='\r')
        if waypoint_index == len(path):
            client.armDisarm(False)
            client.reset()
            client.enableApiControl(False)
        displacement = next_waypoint-current_position
        direction = displacement/np.sqrt(np.sum(displacement**2))
        velocity = base_speed*direction
        client.moveByVelocityAsync(velocity[0], velocity[1], velocity[2], control_period)
    #     print(path)
    #     client.moveOnPathAsync(path = path, velocity = base_speed).join()
    path_following_rate.sleep()

# client.armDisarm(False)
# client.reset()
# client.enableApiControl(False)