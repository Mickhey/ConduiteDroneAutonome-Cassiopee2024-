import tellopy
import av
import cv2
import numpy as np
import person_detector_yolov8 as detector
import sys
import traceback
import time
from time import sleep

def main():
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)
        drone.start_video()  # Starts sending the video stream
        drone.takeoff()

        retry = 3
        container = None
        while container is None and retry > 0:
            retry -= 1
            try:
                container = av.open(drone.get_video_stream())
            except av.AVError as ave:
                print(ave)
                print('retry...')

        frame_skip = 1
        skip_count = frame_skip

        for frame in container.decode(video=0):
            if skip_count > 0:
                skip_count -= 1
                continue  # Skip this frame

            image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
            result, coordinates, barycenter = detector.run_object_detection(image)
            if coordinates != [0, 0, 0, 0]:  # If an object is detected
                bx, by = barycenter
                if bx > 448:
                    drone.clockwise(10)
                    sleep(1)  # Let the drone rotate for 5 seconds
                    if frame.time_base < 1.0/60:
                        time_base = 1.0/60
                    else:
                        time_base = frame.time_base
                    skip_count = int(5 / time_base)
                elif bx < 408:
                    drone.counter_clockwise(10)
                    sleep(1)  # Let the drone rotate for 5 seconds
                    if frame.time_base < 1.0/60:
                        time_base = 1.0/60
                    else:
                        time_base = frame.time_base
                    skip_count = int(5 / time_base)

        drone.land()

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(e)

    finally:
        drone.land()
        drone.quit()  # Properly quit the drone

if __name__ == '__main__':
    main()
