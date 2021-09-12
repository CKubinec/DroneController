from djitellopy import tello
import keyboard_input as Ki

Ki.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())


def get_keyboard_input():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 25

    if Ki.get_key("LEFT"):
        lr = -speed
    elif Ki.get_key("RIGHT"):
        lr = speed

    if Ki.get_key("UP"):
        ud = speed
    elif Ki.get_key("DOWN"):
        ud = -speed

    if Ki.get_key("w"):
        fb = speed
    elif Ki.get_key("s"):
        fb = -speed

    if Ki.get_key("a"):
        yv = speed
    elif Ki.get_key("d"):
        yv = -speed

    if Ki.get_key("t"):
        drone.takeoff()
    if Ki.get_key("l"):
        drone.land()

    return [lr, fb, ud, yv]


while True:
    value = get_keyboard_input()
    drone.send_rc_control(value[0], value[1], value[2], value[3])
