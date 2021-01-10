import b0RemoteApi
from math import *

class Spider:
    def __init__(self, end_of_name = ""):
        self.end_of_name = end_of_name

        self.init_common()
        self.init_joint()
        self.init_legs()

        self.init_geometry_of_legs()
        self.init_control()
    def init_common(self):
        self.name_of_spider = 'hexapod' + self.end_of_name
        self.error_handler = None
        self.object_handler = None
        self.received_object_position = None
        self.received_object_position_error = None
        self.received_object_rotation = None
        self.received_object_rotation_error = None

        self.parent_name = "sim.handle_parent"
    def init_joint(self):
        self.name_of_joint = [['hexa_joint1_0' + self.end_of_name, 'hexa_joint1_1'+ self.end_of_name, 'hexa_joint1_2'+ self.end_of_name, 'hexa_joint1_3'+ self.end_of_name, 'hexa_joint1_4'+ self.end_of_name, 'hexa_joint1_5'+ self.end_of_name],
                              ['hexa_joint2_0' + self.end_of_name, 'hexa_joint2_1'+ self.end_of_name, 'hexa_joint2_2'+ self.end_of_name, 'hexa_joint2_3'+ self.end_of_name, 'hexa_joint2_4'+ self.end_of_name, 'hexa_joint2_5'+ self.end_of_name],
                              ['hexa_joint3_0' + self.end_of_name, 'hexa_joint3_1'+ self.end_of_name, 'hexa_joint3_2'+ self.end_of_name, 'hexa_joint3_3'+ self.end_of_name, 'hexa_joint3_4'+ self.end_of_name, 'hexa_joint3_5'+ self.end_of_name],
                              ['hexa_footTarget0'+ self.end_of_name, 'hexa_footTarget1'+ self.end_of_name, 'hexa_footTarget2'+ self.end_of_name, 'hexa_footTarget3'+ self.end_of_name, 'hexa_footTarget4'+ self.end_of_name, 'hexa_footTarget5'+ self.end_of_name]]

        self.joint_error_handler = []
        self.joint_object_handler = []
        self.joint_received_position = []
        self.joint_received_position_error = []

        self.joint_received_position_his_first_joint = []
        self.joint_received_position_his_first_joint_error = []
    def init_legs(self):
        self.name_of_leg = ['hexa_footTarget0'+ self.end_of_name, 'hexa_footTarget1'+ self.end_of_name, 'hexa_footTarget2'+ self.end_of_name, 'hexa_footTarget3'+ self.end_of_name, 'hexa_footTarget4'+ self.end_of_name, 'hexa_footTarget5'+ self.end_of_name]
        self.leg_error_handler = []
        self.leg_object_handler = []
        self.leg_received_position = []
        self.leg_received_position_error = []
        self.leg_received_position_real = []
        self.leg_received_position_real_error = []
    def init_geometry_of_legs(self):
        self.joint_size_of_part = []
        self.math_position_of_center = [0, 0, 0]
        self.math_position_of_joint_piece = []
        self.math_position_of_joint = []
        self.math_position_offset = []
    def init_control(self):
        self.leg_move_spin_side_no_spin = [0, 0, 0]
        self.leg_move_spin_side_horizontal = [0, 0, 1]
        self.leg_move_spin_side_vertical = [0, 1, 0]

        self.engine_position_default = 90
        self.engine_position_default2 = [90, 120, -25]
        #[90, 0, 90]#[90, 120, -25] # [90, 160, -30]
        self.engine_position_default_min = [0,0,-30]
        self.engine_position_default_max = [180, 180, 210]

        self.engine_side_of_spin = []
        self.engine_position = []
        self.engine_position_min = []
        self.engine_position_max = []
        for i in range(len(self.name_of_joint) - 1):
            self.engine_side_of_spin.append([])
            self.engine_position.append([])
            self.engine_position_min.append([])
            self.engine_position_max.append([])
            for j in range(len(self.name_of_joint[i])):
                if i == 0: self.engine_side_of_spin[i].append(self.leg_move_spin_side_horizontal)
                else: self.engine_side_of_spin[i].append(self.leg_move_spin_side_vertical)
                self.engine_position[i].append(self.engine_position_default2[i])
                self.engine_position_min[i].append(self.engine_position_default_min[i])
                self.engine_position_max[i].append(self.engine_position_default_max[i])



    def set_robot(self, client):
        # Встановлюємо посилання на центр робота
        message = client.simxGetObjectHandle(self.name_of_spider, client.simxServiceCall())
        self.error_handler = message[0]
        self.object_handler = message[1]

        # Встановити посилання на кожен суглоб
        if (self.joint_object_handler == []):
            for i in range(len(self.name_of_joint)):
                self.joint_error_handler.append([])
                self.joint_object_handler.append([])
                for j in range(len(self.name_of_joint[i])):
                    message = client.simxGetObjectHandle(self.name_of_joint[i][j], client.simxServiceCall())
                    self.joint_error_handler[i].append(message[0])
                    self.joint_object_handler[i].append(message[1])
        else:
            for i in range(len(self.name_of_joint)):
                for j in range(len(self.name_of_joint[i])):
                    message = client.simxGetObjectHandle(self.name_of_joint[i][j], client.simxServiceCall())
                    self.joint_error_handler[i][j] = message[0]
                    self.joint_object_handler[i][j] = message[1]

        # Встановити посилання на кожну кінцівку ноги
        if (self.leg_object_handler == []):
            for i in self.name_of_leg:
                message = client.simxGetObjectHandle(i, client.simxServiceCall())
                self.leg_error_handler.append(message[0])
                self.leg_object_handler.append(message[1])
        else:
            for i in range(len(self.name_of_leg)):
                message = client.simxGetObjectHandle(self.name_of_leg[i], client.simxServiceCall())
                self.leg_error_handler[i] = message[0]
                self.leg_object_handler[i] = message[1]


    def receive_position(self, client):
        self.always_receive(client)
        if self.joint_received_position == []:
            self.first_receive(client)
            self.calculate_size()
            self.calculate_math_center_of_spin()
            self.calculate_math_position_of_joint()
        else:
            self.not_first_receive(client)
    def always_receive(self, client):
        # Отримаємо позицію центра
        message = client.simxGetObjectPosition(self.object_handler, -1, client.simxServiceCall())
        self.received_object_position_error = message[0]
        self.received_object_position = message[1]

        # Отримуємо кручення робота
        message = client.simxGetObjectOrientation(self.object_handler, -1, client.simxServiceCall())
        self.received_object_rotation_error = message[0]
        self.received_object_rotation = message[1]

        # print("spin", message[1])
    def first_receive(self, client):
        # Отримуємо всі кінці ніг в абсолютній і відносній системі коордниат
        for i in range(len(self.name_of_leg)):
            message = client.simxGetObjectPosition(self.leg_object_handler[i], self.parent_name, client.simxServiceCall())
            self.leg_received_position_error.append(message[0])
            self.leg_received_position.append(message[1])
            message = client.simxGetObjectPosition(self.leg_object_handler[i], -1, client.simxServiceCall())
            self.leg_received_position_real_error.append(message[0])
            self.leg_received_position_real.append(message[1])

        # Отримаємо всі позиції суглобів і кінців ніг
        for i in range(len(self.name_of_joint)):
            self.joint_received_position_error.append([])
            self.joint_received_position.append([])
            for j in range(len(self.name_of_joint[i])):
                message = client.simxGetObjectPosition(self.joint_object_handler[i][j], -1, client.simxServiceCall())
                self.joint_received_position_error[i].append(message[0])
                self.joint_received_position[i].append(message[1])

                if i == 0:
                    message = client.simxGetObjectPosition(self.joint_object_handler[0][j], self.parent_name, client.simxServiceCall())
                    self.joint_received_position_his_first_joint_error.append(message[0])
                    self.joint_received_position_his_first_joint.append(message[1])
    def calculate_size(self):
        # Додаємо перший відрізок - відрізок із центру до першого мотору
        self.joint_size_of_part.append([])
        for i in range(len(self.joint_received_position_his_first_joint)):
            size = sqrt(
                # self.joint_received_position_his_first_joint[i][0] ** 2 + # = 0 Там погане зміщення
                self.joint_received_position_his_first_joint[i][1] ** 2 +
                self.joint_received_position_his_first_joint[i][2] ** 2)
            self.joint_size_of_part[0].append(size)

        # Додаємо інші відрізки між моторами, та останній між останнім мотором і кінцем ноги
        for i in range(0, 1):
            self.joint_size_of_part.append([])
            for j in range(len(self.name_of_joint[i])):
                size = sqrt(
                    (self.joint_received_position[i][j][0] - self.joint_received_position[i + 1][j][0]) ** 2 +
                    (self.joint_received_position[i][j][1] - self.joint_received_position[i + 1][j][1]) ** 2)  # Z -немає
                self.joint_size_of_part[i + 1].append(size)
        for i in range(1, 2):
            self.joint_size_of_part.append([])
            for j in range(len(self.name_of_joint[i])):
                size = sqrt(
                    (self.joint_received_position[i][j][0] - self.joint_received_position[i + 1][j][0]) ** 2 +
                    (self.joint_received_position[i][j][1] - self.joint_received_position[i + 1][j][1]) ** 2 +
                    (self.joint_received_position[i][j][2] - self.joint_received_position[i + 1][j][2]) ** 2)
                self.joint_size_of_part[i + 1].append(size)
        for i in range(2, len(self.name_of_joint) - 1):
            self.joint_size_of_part.append([])
            for j in range(len(self.name_of_joint[i])):
                size = 0.999 * sqrt(
                    (self.joint_received_position[i][j][0] - self.joint_received_position[i + 1][j][0]) ** 2 +
                    (self.joint_received_position[i][j][1] - self.joint_received_position[i + 1][j][1]) ** 2 +
                    (self.joint_received_position[i][j][2] - self.joint_received_position[i + 1][j][2]) ** 2)
                self.joint_size_of_part[i + 1].append(size)
    def calculate_math_center_of_spin(self):
        for i in range(len(self.joint_received_position[0])):
            self.math_position_of_center[0] += (self.joint_received_position[0][i][0] - self.received_object_position[0]) / len(self.joint_received_position[0])
            self.math_position_of_center[1] += (self.joint_received_position[0][i][1] - self.received_object_position[1]) / len(self.joint_received_position[0])
            self.math_position_of_center[2] += self.joint_received_position[1][i][2] / len(self.joint_received_position[0]) #!! Висоту беремо другій кисті а не по першій!!
    def calculate_math_position_of_joint(self):
        self.math_position_of_joint.append([])
        self.math_position_of_joint_piece.append([])
        for i in range(len(self.joint_received_position[0])):
            x = self.joint_received_position[0][i][0] - self.received_object_position[0]
            y = self.joint_received_position[0][i][1] - self.received_object_position[1]
            z = 0
            self.math_position_of_joint_piece[0].append([x, y, z])
            self.math_position_of_joint[0].append([x, y, z])
            self.math_position_offset.append(self.joint_received_position[1][i][2])

        for i in range(1, 2):
            self.math_position_of_joint.append([])
            self.math_position_of_joint_piece.append([])
            for j in range(len(self.joint_received_position[i])):
                x = self.math_position_of_joint[0][j][0] * ((self.joint_size_of_part[0][j] + self.joint_size_of_part[1][j]) / (self.joint_size_of_part[0][j]))
                y = self.math_position_of_joint[0][j][1] * ((self.joint_size_of_part[0][j] + self.joint_size_of_part[1][j]) / (self.joint_size_of_part[0][j]))
                z = self.math_position_of_joint[0][j][2]
                self.math_position_of_joint[i].append([x, y, z])
                x = self.math_position_of_joint[0][j][0] * ((self.joint_size_of_part[i][j]) / (self.joint_size_of_part[0][j]))
                y = self.math_position_of_joint[0][j][1] * ((self.joint_size_of_part[i][j]) / (self.joint_size_of_part[0][j]))
                z = self.math_position_of_joint[0][j][2]
                self.math_position_of_joint_piece[i].append([x, y, z])

        for i in range(2, 3):
            self.math_position_of_joint.append([])
            self.math_position_of_joint_piece.append([])
            for j in range(len(self.joint_received_position[i])):
                x = self.math_position_of_joint[0][j][0] * ((self.joint_size_of_part[0][j] + self.joint_size_of_part[1][j] + self.joint_size_of_part[2][j]) / (self.joint_size_of_part[0][j]))
                y = self.math_position_of_joint[0][j][1] * ((self.joint_size_of_part[0][j] + self.joint_size_of_part[1][j] + self.joint_size_of_part[2][j]) / (self.joint_size_of_part[0][j]))
                z = self.math_position_of_joint[0][j][2]
                self.math_position_of_joint[i].append([x, y, z])
                x = self.math_position_of_joint[0][j][0] * ((self.joint_size_of_part[i][j]) / (self.joint_size_of_part[0][j]))
                y = self.math_position_of_joint[0][j][1] * ((self.joint_size_of_part[i][j]) / (self.joint_size_of_part[0][j]))
                z = self.math_position_of_joint[0][j][2]
                self.math_position_of_joint_piece[i].append([x, y, z])

        for i in range(3, len(self.joint_received_position)):
            self.math_position_of_joint.append([])
            self.math_position_of_joint_piece.append([])
            for j in range(len(self.joint_received_position[i])):
                x = self.math_position_of_joint[0][j][0] * ((self.joint_size_of_part[0][j] + self.joint_size_of_part[1][j] + self.joint_size_of_part[2][j] + self.joint_size_of_part[3][j]) / (self.joint_size_of_part[0][j]))
                y = self.math_position_of_joint[0][j][1] * ((self.joint_size_of_part[0][j] + self.joint_size_of_part[1][j] + self.joint_size_of_part[2][j] + self.joint_size_of_part[3][j]) / (self.joint_size_of_part[0][j]))
                z = self.math_position_of_joint[0][j][2]
                self.math_position_of_joint[i].append([x, y, z])
                x = self.math_position_of_joint[0][j][0] * ((self.joint_size_of_part[i][j]) / (self.joint_size_of_part[0][j]))
                y = self.math_position_of_joint[0][j][1] * ((self.joint_size_of_part[i][j]) / (self.joint_size_of_part[0][j]))
                z = self.math_position_of_joint[0][j][2]
                self.math_position_of_joint_piece[i].append([x, y, z])

        # for i in range(len(self.math_position_of_joint)):
        #     for j in range(len(self.math_position_of_joint[i])):
        #         print(self.math_position_of_joint[i][j])
        #     print()
    def not_first_receive(self, client):
        pass
            #hip = sqrt((self.joint3_received_position[i][0]) ** 2
            #           + (self.joint3_received_position[i][1]) ** 2
            #           + (self.joint3_received_position[i][2]) ** 2)
            #print(i)#, str(hip))



    def set_leg(self, bone, leg, angle):
        if angle > self.engine_position_max[bone][leg]: angle = self.engine_position_max[bone][leg]
        if angle < self.engine_position_min[bone][leg]: angle = self.engine_position_min[bone][leg]
        self.engine_position[bone][leg] = angle
    def set_leg_dx(self, bone, leg, angle): self.set_leg(bone, leg, self.engine_position[bone][leg] + angle)
    def set_leg_slow(self, bone, leg, angle):
        if abs(angle - self.engine_position[bone][leg]) >= 2:
            self.set_leg(bone, leg, self.engine_position[bone][leg] + 2 * (angle - self.engine_position[bone][leg]) / abs(angle - self.engine_position[bone][leg]))
        elif abs(angle - self.engine_position[bone][leg]) != 0:
            self.set_leg(bone, leg, self.engine_position[bone][leg] + (angle - self.engine_position[bone][leg]) / abs(angle - self.engine_position[bone][leg]))
    def reset_position(self):
        for i in range(len(self.engine_position)):
            for j in range(len(self.engine_position[i])):
                self.engine_position[i][j] = self.engine_position_default2[i]
    def get_position(self): return self.received_object_position
    def get_rotation(self): return self.received_object_rotation
    def get_position_of_motor(self): return self.engine_position
    def get_all(self):
        to_return = []
        # for i in range(len(self.get_position())):
        #     to_return.append(self.get_position()[i])
        # for i in range(len(self.get_rotation())):
        #     to_return.append(self.get_rotation()[i]/(2 * pi))
        for i in range(len(self.get_position_of_motor())):
           for j in range(len(self.get_position_of_motor()[i])):
               to_return.append((self.get_position_of_motor()[i][j] - self.engine_position_min[i][j])
                                /(self.engine_position_max[i][j] - self.engine_position_min[i][j]))
        #print(to_return)
        return to_return



    def move(self, client, output_data = None):
        self.update_engine(output_data)
        self.calculate_leg()
        self.send_data(client)

    def update_engine(self, output_data = None):
        if output_data != None:
            for i in range(len(self.engine_position)): # 3 joints
                for j in range(len(self.engine_position[i])): # 6 legs
                    distance = (self.engine_position_max[i][j] - self.engine_position_min[i][j]) / 2
                    self.set_leg_slow(i, j, distance + output_data[i % 3 + j * 3] * distance)
                    continue


    def calculate_leg(self):
        for i in range(1, len(self.math_position_of_joint)):
            for j in range(len(self.math_position_of_joint[i])):
                self.math_position_of_joint_piece[i][j] = self.calc_leg_his_system([self.joint_size_of_part[i][j], 0, 0],
                                                                            self.engine_side_of_spin[i-1][j],
                                                                           radians(self.engine_position_default - self.engine_position[i-1][j]),
                                                                                 self.math_position_of_joint_piece[i-1][j])
        for i in range(1, len(self.math_position_of_joint)):
            for j in range(len(self.math_position_of_joint[i])):
                for k in range(3):
                    if k == 2 and i == 1: # Тільки першу зміщуємо по осі Z
                        self.math_position_of_joint[i][j][k] = self.math_position_of_joint[i-1][j][k] + self.math_position_of_joint_piece[i][j][k] + self.math_position_offset[j]
                    else:
                        self.math_position_of_joint[i][j][k] = self.math_position_of_joint[i-1][j][k] + self.math_position_of_joint_piece[i][j][k]
    # vector_default_x - позиція в основній системі координат яка дивиться в сторону осі Х, vector_offset - вектор зміни системи координат (минулий вектор)
    def calc_leg_his_system(self, vector_default_x, side, angle, vector_offset):
        motor_spin = [side[0] * angle, side[1] * angle, side[2] * angle]
        motor_vector_spined = self.get_spin(vector_default_x, motor_spin)
        # [0, -atan2(vector_offset[2], vector_offset[0]),
        #                 atan2(vector_offset[1], sqrt(vector_offset[0] * vector_offset[0] + vector_offset[2] * vector_offset[2]))]
        spin = [0, -atan2(vector_offset[2], sqrt(vector_offset[1] * vector_offset[1] + vector_offset[0] * vector_offset[0])), atan2(vector_offset[1], vector_offset[0])]
        return self.get_spin(motor_vector_spined, spin)
    def get_spin(self, pos, general_spin, multi=[1, 1, 1], dp=[0, 0, 0]):
        # return [multi[0] * pos[0] * cos(general_spin[1]) * cos(general_spin[2])
        #         + multi[1] * -pos[1] * cos(general_spin[1]) * sin(general_spin[2])
        #         + multi[2] * pos[2] * sin(general_spin[1])
        #         + dp[0],
        #         multi[0] * pos[0] * (sin(general_spin[2]) * cos(general_spin[0]) + sin(general_spin[0]) * sin(general_spin[1]) * cos(general_spin[2]))
        #         + multi[1] * pos[1] * (cos(general_spin[2]) * cos(general_spin[0]) - sin(general_spin[0]) * sin(general_spin[1]) * sin(general_spin[2]))
        #         + multi[2] * -pos[2] * sin(general_spin[0]) * cos(general_spin[1])
        #         + dp[1],
        #         multi[0] * pos[0] * (sin(general_spin[0]) * sin(general_spin[2]) - cos(general_spin[0]) * sin(general_spin[1]) * cos(general_spin[2]))
        #         + multi[1] * pos[1] * (sin(general_spin[0]) * cos(general_spin[2]) + cos(general_spin[0]) * sin(general_spin[1]) * sin(general_spin[2]))
        #         + multi[2] * pos[2] * cos(general_spin[0]) * cos(general_spin[1])
        #         + dp[2]]

        rZ = [[cos(general_spin[2]), sin(general_spin[2]), 0],
             [-sin(general_spin[2]), cos(general_spin[2]), 0],
             [0, 0, 1]]
        rY = [[cos(general_spin[1]), 0, -sin(general_spin[1])],
             [0, 1, 0],
             [sin(general_spin[1]), 0, cos(general_spin[1])]]
        rX = [[1, 0, 0],
             [0, cos(general_spin[0]), sin(general_spin[0])],
             [0, -sin(general_spin[0]), cos(general_spin[0])]]

        Y = rZ
        X = rY
        D = [[X[0][0] * Y[0][0] + X[0][1] * Y[1][0] + X[0][2] * Y[2][0],
              X[0][0] * Y[0][1] + X[0][1] * Y[1][1] + X[0][2] * Y[2][1],
              X[0][0] * Y[0][2] + X[0][1] * Y[1][2] + X[0][2] * Y[2][2]],
             [X[1][0] * Y[0][0] + X[1][1] * Y[1][0] + X[1][2] * Y[2][0],
              X[1][0] * Y[0][1] + X[1][1] * Y[1][1] + X[1][2] * Y[2][1],
              X[1][0] * Y[0][2] + X[1][1] * Y[1][2] + X[1][2] * Y[2][2]],
             [X[2][0] * Y[0][0] + X[2][1] * Y[1][0] + X[2][2] * Y[2][0],
              X[2][0] * Y[0][1] + X[2][1] * Y[1][1] + X[2][2] * Y[2][1],
              X[2][0] * Y[0][2] + X[2][1] * Y[1][2] + X[2][2] * Y[2][2]]]

        X = D
        Y = rX
        D = [[X[0][0] * Y[0][0] + X[0][1] * Y[1][0] + X[0][2] * Y[2][0],
              X[0][0] * Y[0][1] + X[0][1] * Y[1][1] + X[0][2] * Y[2][1],
              X[0][0] * Y[0][2] + X[0][1] * Y[1][2] + X[0][2] * Y[2][2]],
             [X[1][0] * Y[0][0] + X[1][1] * Y[1][0] + X[1][2] * Y[2][0],
              X[1][0] * Y[0][1] + X[1][1] * Y[1][1] + X[1][2] * Y[2][1],
              X[1][0] * Y[0][2] + X[1][1] * Y[1][2] + X[1][2] * Y[2][2]],
             [X[2][0] * Y[0][0] + X[2][1] * Y[1][0] + X[2][2] * Y[2][0],
              X[2][0] * Y[0][1] + X[2][1] * Y[1][1] + X[2][2] * Y[2][1],
              X[2][0] * Y[0][2] + X[2][1] * Y[1][2] + X[2][2] * Y[2][2]]]

        return [multi[0] * pos[0] * D[0][0]
                + multi[1] * pos[1] * D[1][0]
                + multi[2] * pos[2] * D[2][0]
                + dp[0],
                multi[0] * pos[0] * D[0][1]
                + multi[1] * pos[1] * D[1][1]
                + multi[2] * pos[2] * D[2][1]
                + dp[1],
                multi[0] * pos[0] * D[0][2]
                + multi[1] * pos[1] * D[1][2]
                + multi[2] * pos[2] * D[2][2]
                + dp[2]]
    def send_data(self, client):
        for i in range(len(self.leg_object_handler)):
            position = (self.math_position_of_joint[3][i][0], self.math_position_of_joint[3][i][1], self.math_position_of_joint[3][i][2])
            client.simxSetObjectPosition(self.leg_object_handler[i], self.parent_name, position, client.simxServiceCall())