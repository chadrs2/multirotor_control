#!/usr/bin/python3

import airsim

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

while True:
    in_coords = list(map(int,input("\nEnter destination waypoint in NED cooridnates ").strip().split()))[:3]
    print("Flying to ({},{},{}) at 5 m/s".format(in_coords[0],in_coords[1],in_coords[2]))
    # client.moveToPositionAsync(in_coords[0], in_coords[1], in_coords[2], 5) # This will set the multirotor on a path and imediately return
    client.moveToPositionAsync(in_coords[0], in_coords[1], in_coords[2], 5).join() # This will block until the multirotor has reached its destination
    in_char = input("Continue flying?  y/n ")
    if in_char == 'y':
        continue
    elif in_char == 'n':
        break

client.armDisarm(False)
client.reset()
client.enableApiControl(False)