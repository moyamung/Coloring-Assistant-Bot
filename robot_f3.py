import socket
import time
import modi
import struct
SERVER_IP = '110.76.119.155'
SERVER_PORT = 5050
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
m_r = 1
robot = modi.MODI()

motor1 = None # robot.motors[0]
motor2 = None #robot.motors[1]
motorp1 = None #robot.motors[2]
motorp2 = None #robot.motors[3]

pen = 0
t = 30
d = 30
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

def pen_move(motor1, motor2, motor3, motor4, Color, Up_Down):
    global pen
    if Up_Down == 'U':
        to = -1
    elif Up_Down == 'D':
        to = 1
    if Color == 'R':
        if pen == 0:
            backward(motor3, motor4, t, float(d)*50)
        elif pen == -1:
            backward(motor3, motor4, t, float(d)*100)
        elif pen == 1:
            pass
        pen = 1
        motor1.first_torque(15*to)
        time.sleep(0.3)
        motor1.first_torque(0)
        time.sleep(0.001)
    elif Color == 'Y':
        if pen == 0:
            pass
        elif pen == -1:
            backward(motor3, motor4, t, float(d)*50)
        elif pen == 1:
            forward(motor3, motor4, t, float(d)*50)
        pen = 0
        motor1.second_torque(15*to)
        time.sleep(0.3)
        motor1.second_torque(0)
        time.sleep(0.001)
    elif Color == 'B':
        if pen == 0:
            forward(motor3, motor4, t, float(d)*50)
        elif pen == -1:
            pass
        elif pen == 1:
            forward(motor3, motor4, t, float(d)*100)
        pen = -1
        motor2.first_torque(15*to)
        time.sleep(0.3)
        motor2.first_torque(0)
        time.sleep(0.001)

def forward(motor1, motor2, torque, period):
    t = int(torque)
    if float(period) == d:
        period = 60
    if not float(period) == 0:
        motor1.torque(0, t)
        motor2.torque(0, -1*t*m_r)
        time.sleep(float(period)*0.001)
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(2)
    else:
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.1)

def m_left(motor1, motor2, torque, period):
    t = int(torque)
    if float(period) == d:
        period = 60
    if not float(period) == 0:
        motor1.torque(-1*t, 0)
        motor2.torque(t*m_r, 0)
        time.sleep(float(period)*0.001)
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(2)
    else:
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.2)

def backward(motor1, motor2, torque, period):
    t = int(torque)
    if float(period) == d:
        period = 60
    if not float(period) == 0:
        motor1.torque(0, -1*t)
        motor2.torque(0, t*m_r)
        time.sleep(float(period)*0.001)
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(2)
    else:
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.3)

def m_right(motor1, motor2, torque, period):
    t = int(torque)
    if float(period) == d:
        period = 60
    if not float(period) == 0:
        motor1.torque(t, 0)
        motor2.torque(-1*t*m_r, 0)
        time.sleep(float(period)*0.001)
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(2)
    else:
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.4)

def di_nw(motor1, motor2, torque, period):
    t = int(torque)
    if not float(period) == 0:
        motor1.torque(-1*t, t)
        motor2.torque(t*m_r, -1*t*m_r)
        time.sleep(float(period)*0.001)
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.001)
    else:
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.5)

def di_sw(motor1, motor2, torque, period):
    t = int(torque)
    if not float(period) == 0:
        motor1.torque(-1*t, -1*t)
        motor2.torque(t*m_r, t*m_r)
        time.sleep(float(period)*0.001)
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.001)
    else:
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.6)

def di_ne(motor1, motor2, torque, period):
    t = int(torque)
    if not float(period) == 0:
        motor1.torque(t, t)
        motor2.torque(-1*t*m_r, -1*t*m_r)
        time.sleep(float(period)*0.001)
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.001)
    else:
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.7)

def di_se(motor1, motor2, torque, period):
    t = int(torque)
    if not float(period) == 0:
        motor1.torque(t, -1*t)
        motor2.torque(-1*t*m_r, t*m_r)
        time.sleep(float(period)*0.001)
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.001)
    else:
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.8)

def t_c(motor1, motor2, torque, period):
    t = int(torque)
    if not float(period) == 0:
        motor1.torque(t, t)
        motor2.torque(t*m_r, t*m_r)
        time.sleep(float(period)*0.001)
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.001)
    else:
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.9)

def t_cc(motor1, motor2, torque, period):
    t = int(torque)
    if not float(period) == 0:
        motor1.torque(-1*t, -1*t)
        motor2.torque(-1*t*m_r, -1*t*m_r)
        time.sleep(float(period)*0.001)
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(0.001)
    else:
        motor1.torque(0, 0)
        motor2.torque(0, 0)
        time.sleep(1)

def set_up_motor(client):
    global motor1
    global motor2
    global motorp1
    global motorp2
    for i in range(4):
        tmp = robot.motors[i]
        tmp.torque(0, 0)
    for i in range(4):
        tmp = robot.motors[i]
        tmp.torque(-30, -30)
        time.sleep(0.5)
        tmp.torque(0, 0)
        send_msg(client, 'd'.encode())
        x = recv_msg(client)
        if x == '1':
            motor1 = robot.motors[i]
        elif x == '2':
            motor2 = robot.motors[i]
        elif x == 'p1':
            motorp1 = robot.motors[i]
        elif x == 'p2':
            motorp2 = robot.motors[i]
        send_msg(client, 'd'.encode())

def set_up_pen(client, motorp1, motorp2):
    while True:
        t = recv_msg(client)
        if t=='u':
            motorp1.torque(-30,0)
            time.sleep(0.1)
            motorp1.torque(0,0)
        elif t=='d':
            motorp1.torque(30,0)
            time.sleep(0.1)
            motorp1.torque(0,0)
        elif t == 's':
            break
        send_msg(client, 'd'.encode())
    send_msg(client, 'd'.encode())
    while True:
        t = recv_msg(client)
        if t=='u':
            motorp1.torque(0,-30)
            time.sleep(0.1)
            motorp1.torque(0,0)
        elif t=='d':
            motorp1.torque(0,30)
            time.sleep(0.1)
            motorp1.torque(0,0)
        elif t == 's':
            break
        send_msg(client, 'd'.encode())
    send_msg(client, 'd'.encode())
    while True:
        t = recv_msg(client)
        if t=='u':
            motorp2.torque(-30,0)
            time.sleep(0.1)
            motorp2.torque(0,0)
        elif t=='d':
            motorp2.torque(30,0)
            time.sleep(0.1)
            motorp2.torque(0,0)
        elif t == 's':
            break
        send_msg(client, 'd'.encode())
    send_msg(client, 'd'.encode())

def set_one_step(client, motor1, motor2):
    while True:
        tor = recv_msg(client)
        send_msg(client, 'd'.encode())
        duration = recv_msg(client)
        send_msg(client, 'd'.encode())
        forward(motor1, motor2, tor, float(duration)*20)
        send_msg(client, 'd'.encode())
        ans = recv_msg(client)
        if ans == 's':
            send_msg(client, 'd'.encode())
            break
        else:
            send_msg(client, 'd'.encode())
    return tor, duration

def set_m_r(client, motor1, motor2, tor, duration):
    global m_r
    while True:
        m = recv_msg(client)
        m_r = float(m)
        forward(motor1, motor2, tor, float(duration)*10)
        send_msg(client, 'd'.encode())
        ans = recv_msg(client)
        if ans == 's':
            send_msg(client, 'd'.encode())
            break
        else:
            send_msg(client, 'd'.encode())

if __name__=="__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)

        ans = recv_msg(client_socket)
        send_msg(client_socket, 'd'.encode())
        set_up_motor(client_socket)
        set_up_pen(client_socket, motorp1, motorp2)

        ans = recv_msg(client_socket)
        if ans == 'y':
            send_msg(client_socket, 'd'.encode())
            t, d = set_one_step(client_socket, motor1, motor2)
        elif ans == 'n':
            send_msg(client_socket, 'd'.encode())
            const = recv_msg(client_socket)
            t = ''.join(const[:3])
            d = float(''.join(const[3:len(const)]))
            send_msg(client_socket, 'd'.encode())
        
        ans = recv_msg(client_socket)
        if ans == 'y':
            send_msg(client_socket, 'd'.encode())
            set_m_r(client_socket, motor1, motor2, t, d)
        elif ans == 'n':
            send_msg(client_socket, 'd'.encode())
            const = recv_msg(client_socket)
            m_r = float(const)
            send_msg(client_socket, 'd'.encode())
        while True:
            msg = recv_msg(client_socket)
            if not msg=="":
                if msg[0] == '1':
                    forward(motor1, motor2, ''.join(msg[1:4]), ''.join(msg[4:len(msg)]))
                elif msg[0] == '2':
                    m_left(motor1, motor2, ''.join(msg[1:4]), ''.join(msg[4:len(msg)]))
                elif msg[0] == '3':
                    backward(motor1, motor2, ''.join(msg[1:4]), ''.join(msg[4:len(msg)]))
                elif msg[0] == '4':
                    m_right(motor1, motor2, ''.join(msg[1:4]), ''.join(msg[4:len(msg)]))
                elif msg[0] == '5':
                    di_nw(motor1, motor2, ''.join(msg[1:4]), ''.join(msg[4:len(msg)]))
                elif msg[0] == '6':
                    di_sw(motor1, motor2, ''.join(msg[1:4]), ''.join(msg[4:len(msg)]))
                elif msg[0] == '7':
                    di_ne(motor1, motor2, ''.join(msg[1:4]), ''.join(msg[4:len(msg)]))
                elif msg[0] == '8':
                    di_se(motor1, motor2, ''.join(msg[1:4]), ''.join(msg[4:len(msg)]))
                elif msg[0] == '9':
                    t_c(motor1, motor2, ''.join(msg[1:4]), ''.join(msg[4:len(msg)]))
                elif msg[0] == '0':
                    t_cc(motor1, motor2, ''.join(msg[1:4]), ''.join(msg[4:len(msg)]))
                elif msg[0] == 'R' or msg[0] == 'Y' or msg[0] == 'B':
                    pen_move(motorp1, motorp2, motor1, motor2, msg[0], msg[1])
                send_msg(client_socket, 'd'.encode())
