#!/usr/bin/python3

import airsim

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True, vehicle_name="drone_1")
client.armDisarm(True, vehicle_name="drone_1")
client.enableApiControl(True, vehicle_name="drone_2")
client.armDisarm(True, vehicle_name="drone_2")

while True:
    #in_coords = list(map(int,input("\nEnter destination waypoint in NED cooridnates followed by 1/2 for droneID: ").strip().split()))[:4]
    in_coords = list(map(int,input("\nEnter destination waypoint in NED cooridnates: ").strip().split()))[:3]
    print("Flying to ({},{},{}) at 5 m/s".format(in_coords[0],in_coords[1],in_coords[2]))
    # client.moveToPositionAsync(in_coords[0], in_coords[1], in_coords[2], 5) # This will set the multirotor on a path and imediately return
    client.moveToPositionAsync(in_coords[0], in_coords[1], in_coords[2], 5, vehicle_name="drone_1").join()
    client.moveToPositionAsync(in_coords[0], in_coords[1]+2, in_coords[2], 5, vehicle_name="drone_2").join()
    '''if in_coords[3] == 1:
        client.moveToPositionAsync(in_coords[0], in_coords[1], in_coords[2], 5, vehicle_name="drone_1").join() # This will block until the multirotor has reached its destination
    elif in_coords[3] == 2:
        client.moveToPositionAsync(in_coords[0], in_coords[1], in_coords[2], 5, vehicle_name="drone_2").join()
    else:
        print("Incorrect droneID entered for waypoint navigation!!")
    '''
    in_char = input("Continue flying?  y/n ")
    if in_char == 'y':
        continue
    elif in_char == 'n':
        break

client.armDisarm(False, vehicle_name="drone_1")
client.armDisarm(False, vehicle_name="drone_2")
client.reset()
client.enableApiControl(False, vehicle_name="drone_1")
client.enableApiControl(False, vehicle_name="drone_2")