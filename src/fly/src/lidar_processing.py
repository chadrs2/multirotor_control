import numpy as np
import rospy
import airsim

import std_msgs.msg
import sensor_msgs.msg

rospy.init_node("lidar_processing", anonymous=True)
lidar_publisher = rospy.Publisher("lidar_drone1", sensor_msgs.msg.PointCloud2, queue_size=1)

client = airsim.MultirotorClient()
client.confirmConnection()

lidar_publishing_rate = rospy.Rate(30) # 30hz

def numpy_to_pointcloud(points):
    dimensions = len(points[0,:])
    itemsize = np.dtype(np.float32).itemsize
    data = points.astype(np.float32).tobytes()
    fields = [sensor_msgs.msg.PointField(name=n,
                                         offset=i*itemsize, 
                                         datatype=sensor_msgs.msg.PointField.FLOAT32, 
                                         count=1) for i, n in enumerate('xyz')]

    header = std_msgs.msg.Header(frame_id = 'world', stamp = rospy.Time.now())
    return sensor_msgs.msg.PointCloud2(header=header,
                                        height=1,
                                        width=points.shape[0],
                                        is_dense=False,
                                        is_bigendian=False,
                                        fields=fields,
                                        point_step=(itemsize * dimensions),
                                        row_step=(itemsize * dimensions * points.shape[0]),
                                        data=data)

def parse_lidar(lidar_point_cloud):
    if (len(lidar_point_cloud) < 3):
        print('No points received from Lidar data', end = '\r')
    else:
        points = np.array(lidar_point_cloud, dtype=np.dtype(np.float32))
        points = np.reshape(points, (int(points.shape[0]/3), 3))
        lidar_publisher.publish(numpy_to_pointcloud(points))

while not rospy.is_shutdown():
    # something
    parse_lidar(client.getLidarData().point_cloud)
    lidar_publishing_rate.sleep()