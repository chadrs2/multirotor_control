#!/usr/bin/python3

import rospy
import airsim

import std_msgs.msg
import nav_msgs.msg

rospy.init_node("odom_processing", anonymous=True)
odom_publisher1 = rospy.Publisher("odom_drone1", nav_msgs.msg.Odometry, queue_size=1)
odom_publisher2 = rospy.Publisher("odom_drone2", nav_msgs.msg.Odometry, queue_size=1)

client = airsim.MultirotorClient()
client.confirmConnection()

odom_publishing_rate = rospy.Rate(90) # 90hz
msg_num = 0

def parse_odom(estimated_kinematics, droneId):
    global msg_num
    out_odom = nav_msgs.msg.Odometry()
    out_odom.header.frame_id = 'world'
    out_odom.header.seq = msg_num
    out_odom.header.stamp = rospy.Time.now()
    out_odom.pose.pose.position.x = estimated_kinematics.position.x_val
    out_odom.pose.pose.position.y = estimated_kinematics.position.y_val
    out_odom.pose.pose.position.z = estimated_kinematics.position.z_val
    out_odom.pose.pose.orientation.w = estimated_kinematics.orientation.w_val
    out_odom.pose.pose.orientation.x = estimated_kinematics.orientation.x_val
    out_odom.pose.pose.orientation.y = estimated_kinematics.orientation.y_val
    out_odom.pose.pose.orientation.z = estimated_kinematics.orientation.z_val
    msg_num += 1
    if droneId == 1:
        odom_publisher1.publish(out_odom)
    elif droneId == 2:
        odom_publisher2.publish(out_odom)
    else:
        print("Incorrect drone ID: Can't process odometry data")

while not rospy.is_shutdown():
    # something
    parse_odom(client.getMultirotorState("drone_1").kinematics_estimated, 1)
    parse_odom(client.getMultirotorState("drone_2").kinematics_estimated, 2)
    odom_publishing_rate.sleep()