import socket
import time
import Simulator
import cv2
import os
import struct
from Image_Processing import *

CAM_IP = 'http://110.76.111.13:4747/video'
IP = ''
PORT = 5050
ADDR = (IP, PORT)
tor = '025'
duration = 20
m_r = 1

def send_list(comm_list, client_socket):
    for command in comm_list:
        print(command)
        if len(command)==2:
            while True:
                #add_com = 's'
                add_com = input("Type command to send. If you want to pass, just type 's'\n").lower()
                if add_com == 's':
                    #time.sleep(1)
                    break
                else:
                    send_msg(client_socket, add_com.encode())
                    recv_msg(client_socket)
        send_msg(client_socket, command.encode())
        recv_msg(client_socket)

def send_msg(client_socket, msg):
    msg = struct.pack('>I', len(msg))+msg
    client_socket.sendall(msg)

def recv_msg(client_socekt):
    raw_msg_len = recvall(client_socket, 4).encode()
    if not raw_msg_len:
        return None
    msg_len = struct.unpack('>I', bytes(raw_msg_len))[0]
    return recvall(client_socekt, msg_len)

def recvall(client_socekt, n):
    data = bytearray()
    while len(data)<n:
        packet = client_socket.recv(n-len(data))
        if not packet:
            return None
        data.extend(packet)
    return data.decode()

def camera(droidcam):
    cap = cv2.VideoCapture(droidcam)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    print("Type 's' when you want to capture the image.")
    while True:
        success, tmp = cap.read()
        cv2.imshow('Current view', tmp)
        if cv2.waitKey(1) == ord('s'):
            break
    success, img = cap.read()
    print('Sketch image captured.')
    cv2.imshow('Sketch image', img)
    print('Please mark the color for CAB. A disk about 50won is enough.')
    print("Type 's' when you want to capture the image.")
    while True:
        success, tmp = cap.read()
        cv2.imshow('Current view', tmp)
        if cv2.waitKey(1) == ord('s'):
            break
    success, img_colored = cap.read()
    cv2.imshow('Colored image', img_colored)
    time.sleep(1)
    print('All image capturing processes were successfully done.')
    print("Type 's' to continue")
    while True:
        cv2.imshow('Colored image', img_colored)
        if cv2.waitKey(1) == ord('s'):
            break
    cv2.destroyAllWindows()
    cap.release()
    return img, img_colored

def set_motor(client_socket):
    while True:
        ans = input("If you're ready to set motors, please type 's': ")
        if ans == 's':
            send_msg(client_socket, 's'.encode())
            recv_msg(client_socket)
            break
    print("Backward: '1', Forward: '2', Red&Yellow pens: 'p1', Blue pen: 'p2'")
    for i in range(4):
        recv_msg(client_socket)
        ans = input("Please type the right motor name.: ")
        send_msg(client_socket, (ans.lower()).encode())
        recv_msg(client_socket)

def set_pens(client_socket):
    print("Please type 'u' for upward movement, 'd' for downward, or 's' for saving current status.")
    for i in range(3):
        print('For pen'+str(i))
        while True:
            ans = input().lower()
            send_msg(client_socket, ans.encode())
            if ans == 's':
                break
            recv_msg(client_socket)
        recv_msg(client_socket)
            

def set_one_step(client_socket):
    global tor
    global duration
    while True:
        print("Current torque: " + tor)
        tor = input("How do you want to adjust the torque?\n").zfill(3)
        send_msg(client_socket, tor.encode())
        recv_msg(client_socket)
        print("Current duration: " + str(duration))
        duration = float(input("How do you want to adjust the duration?\n"))
        send_msg(client_socket, str(duration).encode())
        recv_msg(client_socket)
        recv_msg(client_socket)
        print("Do you satisfy with the current setting? Robot should have moved for 2cm.")
        ans = input("Type 's' to keep this setting. If you want to adjust it again, type 'n'.\n").lower()
        send_msg(client_socket, ans.encode())
        recv_msg(client_socket)
        if ans == 's':
            break

def set_m_r(client_socket):
    global m_r
    while True:
        print("The current offset for right_motor_torque is "+str(m_r))
        m_r = float(input("How do you want to adjust the offset for right_motor_torque?\n"))
        send_msg(client_socket, str(m_r).encode())
        recv_msg(client_socket)
        print("Do you satisfy with the current setting? Robot should have moved for 3cm.")
        while True:
            ans = input("Type 's' to keep this setting. If you want to adjust it again, type 'n'.\n").lower()
            send_msg(client_socket, ans.encode())
            recv_msg(client_socket)
            if ans == 's':
                break
            elif ans == 'n':
                break
        if ans == 's':
            break


if __name__=="__main__":    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(ADDR)
        server_socket.listen()
        client_socket, client_addr = server_socket.accept()
        time.sleep(1)
        print('Hello. My name is CAB.')
        print("Let's set motors for CAB.")
        set_motor(client_socket)
        print("Great!")
        print("Let's set pens for CAB.")
        set_pens(client_socket)
        print("Excellent!")
        print("Do you want to change the basic offset for one_step?")
        while True:
            ans = input("If you want, type 'y'. If not, type 'n'\n").lower()
            if ans == 'y':
                send_msg(client_socket, 'y'.encode())
                recv_msg(client_socket)
                set_one_step(client_socket)
                break
            elif ans == 'n':
                send_msg(client_socket, 'n'.encode())
                recv_msg(client_socket)
                send_msg(client_socket, (tor+str(duration)).encode())
                recv_msg(client_socket)
                break
        print("Almost done!")
        print("Do you want to change the basic offset for right_motor_torque?")
        while True:
            ans = input("If you want, type 'y'. If not, type 'n'\n").lower()
            if ans == 'y':
                send_msg(client_socket, 'y'.encode())
                recv_msg(client_socket)
                set_m_r(client_socket)
                break
            elif ans == 'n':
                send_msg(client_socket, 'n'.encode())
                recv_msg(client_socket)
                send_msg(client_socket, str(m_r).encode())
                recv_msg(client_socket)
                break
        print("All seting processes are finally done!")
        print('Sketch what you want. But watch out! Your drawing should consist of CLOSED loops.')
        img, img_colored = camera(CAM_IP)
        print ("Just wair for a few seconds for CAB to find better way to color your amazing sketch.")
        path = Simulator.draw(img,img_colored, tor, duration, 1675)
        print('Path is decided!')
        while True:
            ans = input("Type 's' to start!\n").lower()
            if ans == 's':
                break
        send_list(path, client_socket)
        print("Done! CAB said it was happy to be with you!")
        client_socket.close()