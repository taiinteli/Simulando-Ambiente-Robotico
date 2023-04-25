#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
import math

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer_ = self.create_timer(0.1, self.move_turtle)
        self.twist_msg_ = Twist()

    def move_turtle(self):
        radius = 0.1  # valor do raio da espira
        revolutions = 2  # vezes que ira fazer a espiral
        angular_velocity = 1.0  # valor da velocidade angular medida em radianos/segundos da tartaruga 
        frequency = 10  # frequencia da publicacao das mensagens
        period = 1.0 / frequency  #  intervalo de segundo sobre cada mensagem 
        time_increment = period / 2  # incremento de tempo com a finalidade de calcular a proxima posicao 


        t = 0.0  # tempo inicial 
        for i in range(int(revolutions * 2 * math.pi / time_increment)):
            # calculo para a proxima posicao da tartaruga com base no tempo inicial 
            x = radius * math.cos(angular_velocity * t) * t
            y = radius * math.sin(angular_velocity * t) * t

            # calculo da velocidade angular da tartaruga com base a posicao e velocidade  atual
            linear_velocity = math.sqrt(x**2 + y**2) / period  # valor da velocidade angular constante
            angular_velocity = angular_velocity  # velocidade angular constante 

            #  criar e publicar uma mensagem Twist para a posicao e velocidade atual
            twist_msg = Twist()
            twist_msg.linear.x = linear_velocity
            twist_msg.angular.z = angular_velocity
            self.publisher_.publish(twist_msg)

            # aguarda a duracao do periodo atual 
            time.sleep(period)

            # atualiza o tempo que foi decorrido 
            t += time_increment


def main(args=None):
    rclpy.init(args=args)
    turtle_controller = TurtleController()
    rclpy.spin(turtle_controller)
    turtle_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
