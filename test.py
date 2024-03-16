from vectornav_lib import *
import sys


# if __name__ == '__main__': 
#     vn = VNUSB_lib(sys.argv[1], 115200)

#     while(1):
#         data = vn.poll_data()
#         print(data.yaw_pitch_roll)

async def main():
    vn = VNUSB_lib(sys.argv[1], 115200)
    while(1):
        result = await vn.poll_data_async()
        print(f"Result: {result.yaw_pitch_roll}")

# Run the main coroutine
if __name__ == '__main__': 
    asyncio.run(main())