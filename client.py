import socket
import cv2
import numpy as np
import struct

vid_capture = cv2.VideoCapture(0)
while(vid_capture.isOpened()):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect(('localhost', 55000))  
    ret, frame = vid_capture.read()
    if ret == True:
        cv2.imshow('FaceTime', frame)
        buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])[1]
        data = np.array(buffer)
        byte_data = data.tobytes()
        sock.sendall(struct.pack(">L", len(byte_data))+byte_data)
        k = cv2.waitKey(1)
        if k == 113 or k == 27:
            sock.close()
            break
        sock.close()
    else:
        break
vid_capture.release()
cv2.destroyAllWindows()
