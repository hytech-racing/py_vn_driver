from vectornav_lib import *
import sys

import asyncio
import socket
from vn_protos_np_proto_py.vectornav_proto import wrapper_pb2
from hytech_np_proto_py import hytech_pb2


async def send_message_over_udp(serialized_message, host="127.0.0.1", port=6000):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    loop = asyncio.get_running_loop()
    sock.setblocking(False)
    await loop.sock_sendto(sock, serialized_message, (host, port))
    sock.close()


async def main():
    wrapper = wrapper_pb2.VNWrapper()

    vn = VNUSB_lib(sys.argv[1], 115200)

    while 1:
        result = await vn.poll_data_async()

        vn_ypr_msg = hytech_pb2.vn_ypr(
            vn_yaw=result.yaw_pitch_roll[0],
            vn_pitch=result.yaw_pitch_roll[1],
            vn_roll=result.yaw_pitch_roll[2],
        )
        vn_linear_accel = hytech_pb2.vn_linear_accel(
            vn_lin_ins_accel_x=result.linear_accel_ins_body[0],
            vn_lin_ins_accel_y=result.linear_accel_ins_body[1],
            vn_lin_ins_accel_z=result.linear_accel_ins_body[2]
        )
        vn_linear_accel_uncomp = hytech_pb2.vn_linear_accel_uncomp(
            vn_lin_uncomp_accel_x=result.linear_accel_uncomp[0],
            vn_lin_uncomp_accel_y=result.linear_accel_uncomp[1],
            vn_lin_uncomp_accel_z=result.linear_accel_uncomp[2],
        )
        vn_vel = hytech_pb2.vn_vel(
            vn_body_vel_x=result.body_vel[0],
            vn_body_vel_y=result.body_vel[1],
            vn_body_vel_z=result.body_vel[2],
        )
        vn_lat_lon = hytech_pb2.vn_lat_lon(
            vn_gps_lat=result.gps_lat_lon[0],
            vn_gps_lon=result.gps_lat_lon[1]
        )
        vn_gps_time = hytech_pb2.vn_gps_time(
            vn_gps_time=result.gps_time,
        )
        vn_status = hytech_pb2.vn_status(
            vn_gps_status = result.gps_fix
        )

        wrapper.vn_ypr_data.CopyFrom(vn_ypr_msg)
        wrapper.vn_linear_accel_data.CopyFrom(vn_linear_accel)
        wrapper.vn_linear_accel_uncomp_data.CopyFrom(vn_linear_accel_uncomp)
        wrapper.vn_vel_data.CopyFrom(vn_vel)
        wrapper.vn_lat_lon_data.CopyFrom(vn_lat_lon)
        wrapper.vn_gps_time_data.CopyFrom(vn_gps_time)
        wrapper.vn_status_data.CopyFrom(vn_status)
        serialized_message = wrapper.SerializeToString()
        await send_message_over_udp(serialized_message)

        print(f"Result: {result.yaw_pitch_roll}")


# Run the main coroutine
if __name__ == "__main__":
    asyncio.run(main())
