import socket
import time
import modi

SERVER_IP = '192.168.1.189'
SERVER_PORT = 5050
SIZE = 1024
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
m_r = 1
robot = modi.MODI()
motor1 = robot.motors[0]
motor2 = robot.motors[1]
motorp1 = robot.motors[2]
motorp2 = robot.motors[3]
pen = 0
t = 30
d = 70
def pen_move(motor1, motor2, motor3, motor4, Color, Up_Down):
    global pen
    if Up_Down == 'U':
        t = -1
    elif Up_Down == 'D':
        t = 1
    if Color == 'R':
        if pen == 0:
            backward(motor3, motor4, 30, 850)
        elif pen == -1:
            backward(motor3, motor4, 30, 1700)
        elif pen == 1:
            pass
        pen = 1
        motor1.first_torque(15*t)
        time.sleep(0.3)
        motor1.first_torque(0)
        time.sleep(0.001)
    elif Color == 'Y':
        if pen == 0:
            pass
        elif pen == -1:
            backward(motor3, motor4, 30, 850)
        elif pen == 1:
            forward(motor3, motor4, 30, 1700)
        pen = 0
        motor1.second_torque(15*t)
        time.sleep(0.3)
        motor1.second_torque(0)
        time.sleep(0.001)
    elif Color == 'B':
        if pen == 0:
            forward(motor3, motor4, 30, 850)
        elif pen == -1:
            pass
        elif pen == 1:
            forward(motor3, motor4, 30, 1700)
        pen = -1
        motor2.first_torque(15*t)
        time.sleep(0.3)
        motor2.first_torque(0)
        time.sleep(0.001)

def forward(motor1, motor2, torque, period):
    t = int(torque)
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
        client.send('d'.encode())
        x = client.recv(SIZE).decode()
        if x == '1':
            motor1 = robot.motors[i]
        elif x == '2':
            motor2 = robot.motors[i]
        elif x == 'p1':
            motorp1 = robot.motors[i]
        elif x == 'p2':
            motorp2 = robot.motors[i]
        client.send('d'.encode())

def set_up_pen(client, motorp1, motorp2):
    while True:
        t = client.recv(SIZE).decode()
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
        client.send('d'.encode())
    client.send('d'.encode())
    while True:
        t = client.recv(SIZE).decode()
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
        client.send('d'.encode())
    client.send('d'.encode())
    while True:
        t = client.recv(SIZE).decode()
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
        client.send('d'.encode())
    client.send('d'.encode())

def set_one_step(client, motor1, motor2):
    while True:
        tor = client.recv(SIZE).decode()
        client.send('d'.encode())
        duration = client.recv(SIZE).decode()
        client.send('d'.encode())
        forward(motor1, motor2, tor, float(duration)*10)
        client.send('d'.encode())
        ans = client.recv(SIZE).decode()
        if ans == 's':
            client.send('d'.encode())
            break
        else:
            client.send('d'.encode())
    return tor, duration

def set_m_r(client, motor1, motor2, tor, duration):
    global m_r
    while True:
        m = client.recv(SIZE).decode()
        m_r = float(m)
        forward(motor1, motor2, tor, float(duration)*10)
        client.send('d'.encode())
        ans = client.recv(SIZE).decode()
        if ans == 's':
            client.send('d'.encode())
            break
        else:
            client.send('d'.encode())

if __name__=="__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)

        ans = client_socket.recv(SIZE).decode()
        client_socket.send('d'.encode())
        set_up_motor(client_socket)
        set_up_pen(client_socket, motorp1, motorp2)

        ans = client_socket.recv(SIZE).decode()
        if ans == 'y':
            client_socket.send('d'.encode())
            t, d = set_one_step(client_socket, motor1, motor2)
        elif ans == 'n':
            client_socket.send('d'.encode())
            const = client_socket.recv(SIZE).decode()
            t = ''.join(const[:3])
            d = ''.join(const[3:len(ans)])
            client_socket.send('d'.encode())
        
        ans = client_socket.recv(SIZE).decode()
        if ans == 'y':
            client_socket.send('d'.encode())
            set_m_r(client_socket, motor1, motor2, t, d)
        elif ans == 'n':
            client_socket.send('d'.encode())
            const = client_socket.recv(SIZE).decode()
            m_r = float(const)
            client_socket.send('d'.encode())

        while True:
            msg = client_socket.recv(SIZE).decode()
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
                client_socket.send('d'.encode())