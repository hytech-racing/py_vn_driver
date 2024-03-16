from vnpy import *
import sys
from typing import Tuple
from enum import Enum


# yaw pitch roll angles
# linear accel data
# angular accel
# body velocities
# gps position
# gps time

# x forward, z down, y right
VectorXYZ = Tuple[float, float, float]
VectorLatLonAlt = VectorXYZ

class GpsFixType(Enum):
    NO_FIX = 0 
    TIME_ONLY = 1 
    FIX_2D = 2 
    FIX_3D = 3 

class VectornavData:
    yaw_pitch_roll: VectorXYZ
    linear_accel_ins_body: VectorXYZ
    linear_accel_uncomp: VectorXYZ
    body_vel: VectorXYZ
    gps_lat_lon_altitude: VectorLatLonAlt
    gps_fix: GpsFixType
    def __init__(self):
        self.yaw_pitch_roll = [0.0, 0.0, 0.0]
        self.linear_accel_uncomp = [0.0, 0.0, 0.0]
        self.linear_accel_ins_body = [0.0, 0.0, 0.0]
        self.body_vel = [0.0, 0.0, 0.0]
        self.gps_lat_lon_alt = [0.0, 0.0, 0.0]
        self.gps_time = 0.0 # The absolute GPS time since start of GPS epoch 1980 expressed in nano seconds. This field is equivalent to the TimeGps field in group 2.
        self.gps_fix = GpsFixType.NO_FIX

class VNUSB_lib:
    def __init__(self, port, baudrate):
        self.vn_sensor_ez = EzAsyncData.connect(port, baudrate)
    
    def poll_data(self) -> VectornavData:
        data = VectornavData()
        # from: https://blog.benhall.tech/vn_driver_lib/cpp/help/ez_async_data_2main_8cpp-example.html
        # // Often, we would like to get and process each packet received from the sensor.
        # // This is not realistic with ez->currentData() since it is non-blocking and we
        # // would also have to compare each CompositeData struture for changes in the data.
        # // However, EzAsyncData also provides the getNextData() method which blocks until
        # // a new data packet is available. The for loop below shows how to output each
        # // data packet received from the sensor using getNextData().
        # self.vn_sensor_ez.getNextData()
        data.body_vel = self.vn_sensor_ez.current_data.velocity_estimated_body
        data.linear_accel_uncomp = self.vn_sensor_ez.current_data.acceleration_uncompensated
        data.linear_accel_ins_body = self.vn_sensor_ez.current_data.acceleration_linear_body
        data.yaw_pitch_roll = self.vn_sensor_ez.current_data.yaw_pitch_roll
        data.gps_lat_lon_alt = self.vn_sensor_ez.current_data.position_gps_lla
        data.gps_time = self.vn_sensor_ez.current_data.time_gps
        data.gps_fix = self.vn_sensor_ez.current_data.fix
        return data