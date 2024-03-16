from vectornav_lib import *
import sys


if __name__ == '__main__': 
    vn = VNUSB_lib(sys.argv[1], 115200)

    while(1):
        data = vn.poll_data()
        print(data.body_vel)