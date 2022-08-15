#! /usr/bin/env python
import rospy
import math
import angles
from geometry_msgs.msg import Twist, Pose2D
from turtlesim.msg import Pose

def callback(data):
    global current_pose
    current_pose = Pose()
    current_pose = data

def calcParam(goal_pose):
    distance = abs(math.sqrt( ( ( goal_pose.x - current_pose.x ) ** 2 ) + ( ( goal_pose.y - current_pose.y) ** 2 ) ) )
    angle = math.atan2(goal_pose.y - current_pose.y, goal_pose.x - current_pose.x)
    return [distance, angle]

if __name__ == '__main__':
    try:
        rospy.init_node('nodo1', anonymous=True)
        rospy.loginfo("Nodo Iniciado")

        # Suscriptor para obtener la posicion actual
        sub = rospy.Subscriber('/turtle1/pose', Pose, callback)
        
        # Publicador para mandar los datos
        pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
        
        # Se piden los datos 
        goal_pose = Pose2D()
        goal_pose.x = input("Ingrese el punto objetivo x:")
        goal_pose.y = input("Ingrese el punto objetivo y:")

        while (True):
            # Se calcula la distancia y el angulo
            parameters = calcParam(goal_pose)
            distance = parameters[0]
            goal_angle = parameters[1]

            # Diferencia mas corta entre el angulo objetivo y el angulo actual
            current_angle = current_pose.theta
            difference_angle = angles.shortest_angular_distance(current_angle, goal_angle)
            
            # Prepara los datos a publicar
            velocity = Twist()
            velocity.linear.x = distance * 0.2
            velocity.angular.z = difference_angle * 0.66

            # Publica los datos
            pub.publish(velocity)
            rospy.loginfo(current_pose)

            if (distance < 0.01):
                break

    except rospy.ROSInterruptException:
        pass