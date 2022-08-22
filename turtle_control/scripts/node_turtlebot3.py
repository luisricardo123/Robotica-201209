#!/usr/bin/env python

import rospy
# import random
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def scan_callback(msg):
  global lectura_minima_sensor
  lectura_minima_sensor = min(msg.ranges)

def obstaculo_cerca(lectura_sensor):
#   print("Obstaculo: ", lectura_sensor < 0.7)
  return lectura_sensor < 0.7

def acabo_tiempo(tiempo_limite):
#   print("Acabo el tiempo: ", rospy.Time.now() > tiempo_limite)
  return rospy.Time.now() > tiempo_limite

if __name__ == '__main__':
  rospy.init_node('Nodo1')
  rospy.loginfo("Nodo Iniciado")

  lectura_minima_sensor = 1
  scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)
  cmd_vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
  tiempo_limite = rospy.Time.now() + rospy.Duration(5)
  
  avanzar = True
  rate = rospy.Rate(10)

  while not rospy.is_shutdown():
    if avanzar:

      if (obstaculo_cerca(lectura_minima_sensor) or acabo_tiempo(tiempo_limite)):
        avanzar = False
        tiempo_limite = rospy.Time.now() + rospy.Duration(0.3)
      
    else:

      if (acabo_tiempo(tiempo_limite)):
        avanzar = True
        tiempo_limite = rospy.Time.now() + rospy.Duration(5)
      
    twist = Twist()

    if avanzar:
      twist.linear.x = 1
    #   print("avanza")
    else:
      twist.angular.z = 1
    #   print("gira")

    # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

    cmd_vel_pub.publish(twist)

    rate.sleep()
