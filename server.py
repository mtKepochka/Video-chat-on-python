import socket
import cv2
import numpy as np
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 55000
sock.bind(('', port))
sock.listen(10)
print('Server is listening on port:', port)
data = b""
while True:
    conn, addr = sock.accept()
    size_of_data = struct.calcsize(">L")
    while len(data) < size_of_data:
        data += conn.recv(1024)
        if not data:
            conn.close()
            break

    frame_size = struct.unpack(">L", data[:size_of_data])[0]
    data = data[size_of_data:]
    while len(data) < frame_size:
        data += conn.recv(1024)
        if not data:
            conn.close()
            break
    frame_data = data[:frame_size]
    frame_data = np.asarray(bytearray(frame_data))

    frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
    cv2.imshow("Facetime", frame)

    data = data[frame_size:]

    k = cv2.waitKey(1)
    if k == 113 or k == 27:
        conn.close()
        break
    conn.close()

cv2.destroyAllWindows()
