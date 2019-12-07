import socket
import time
import Simulator
import cv2
import os
from Image_Processing import *

CAM_IP = 'http://192.168.43.119:4747/video'
IP = ''
PORT = 5050
SIZE = 1024
ADDR = (IP, PORT)
tor = '035'
duration = 150
m_r = 1

def send_list(comm_list, client_socket):
    for command in comm_list:
        print(command)
        if len(command)==2:
            while True:
                add_com = input("Type command to send. If you want to pass, just type 's'\n").lower()
                if add_com == 's':
                    break
                else:
                    client_socket.send(add_com.encode())
                    client_socket.recv(SIZE).decode()
        client_socket.send(command.encode())
        client_socket.recv(SIZE).decode()

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
            client_socket.send('s'.encode())
            client_socket.recv(SIZE).decode()
            break
    print("Backward: '1', Forward: '2', Red&Yellow pens: 'p1', Blue pen: 'p2'")
    for i in range(4):
        client_socket.recv(SIZE).decode()
        ans = input("Please type the right motor name.: ")
        client_socket.send((ans.lower()).encode())
        client_socket.recv(SIZE).decode()

def set_pens(client_socket):
    print("Please type 'u' for upward movement, 'd' for downward, or 's' for saving current status.")
    for i in range(3):
        print('For pen'+str(i))
        while True:
            ans = input().lower()
            client_socket.send(ans.encode())
            if ans == 's':
                break
            client_socket.recv(SIZE).decode()
        client_socket.recv(SIZE).decode()
            

def set_one_step(client_socket):
    global tor
    global duration
    while True:
        print("Current torque: " + tor)
        tor = input("How do you want to adjust the torque?\n").zfill(3)
        client_socket.send(tor.encode())
        client_socket.recv(SIZE).decode()
        print("Current duration: " + str(duration))
        duration = float(input("How do you want to adjust the torque?\n"))
        client_socket.send(str(duration).encode())
        client_socket.recv(SIZE).decode()
        client_socket.recv(SIZE).decode()
        print("Do you satisfy with the current setting? Robot should have moved for 3cm.")
        ans = input("Type 's' to keep this setting. If you want to adjust it again, type 'n'.\n").lower()
        client_socket.send(ans.encode())
        client_socket.recv(SIZE).decode()
        if ans == 's':
            break

def set_m_r(client_socket):
    global m_r
    while True:
        print("The current offset for right_motor_torque is "+str(m_r))
        m_r = float(input("How do you want to adjust the offset for right_motor_torque?\n"))
        client_socket.send(str(m_r).encode())
        client_socket.recv(SIZE).decode()
        print("Do you satisfy with the current setting? Robot should have moved for 3cm.")
        while True:
            ans = input("Type 's' to keep this setting. If you want to adjust it again, type 'n'.\n").lower()
            client_socket.send(ans.encode())
            client_socket.recv(SIZE).decode()
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
                client_socket.send('y'.encode())
                client_socket.recv(SIZE).decode()
                set_one_step(client_socket)
                break
            elif ans == 'n':
                client_socket.send('n'.encode())
                client_socket.recv(SIZE).decode()
                client_socket.send((tor+str(duration)).encode())
                client_socket.recv(SIZE).decode()
                break
        print("Almost done!")
        print("Do you want to change the basic offset for right_motor_torque?")
        while True:
            ans = input("If you want, type 'y'. If not, type 'n'\n").lower()
            if ans == 'y':
                client_socket.send('y'.encode())
                client_socket.recv(SIZE).decode()
                set_m_r(client_socket)
                break
            elif ans == 'n':
                client_socket.send('n'.encode())
                client_socket.recv(SIZE).decode()
                client_socket.send(str(m_r).encode())
                client_socket.recv(SIZE).decode()
                break
        print("All seting processes are finally done!")
        print('Sketch what you want. But watch out! Your drawing should consist of CLOSED loops.')
        img, img_colored = camera(CAM_IP)
        print ("Just wair for a few seconds for CAB to find better way to color your amazing sketch.")
        path = Simulator.draw(img,img_colored, tor, duration, 1675)
        print('Path is decided!')
        send_list(path, client_socket)
        print("Done! CAB said it was happy to be with you!")
        client_socket.close()