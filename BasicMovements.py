from djitellopy import Tello

"""Connecting to the Drone"""
drone = Tello()
drone.connect()

"""Giving Movement Commands to the Drone"""
drone.takeoff()
drone.move_up(10)
drone.land()
