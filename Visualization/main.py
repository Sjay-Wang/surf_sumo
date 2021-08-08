import threading
import time
import traci
import optparse
import os
from tkinter import *
import tkinter as tk
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture
from ObjLoader import ObjLoader
from sumolib import checkBinary

global flag


# 验证环境变量
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


def returnLeaders(target_vehicle_id):
    all_leader_vehicle = []
    temp_vehicle_id = target_vehicle_id
    while traci.vehicle.getLeader(temp_vehicle_id) is not None:
        leader = list(traci.vehicle.getLeader(temp_vehicle_id))
        all_leader_vehicle.append(leader)
        temp_vehicle_id = leader[0]
    return all_leader_vehicle


def returnAllLeftLeaders(target_vehicle_id):
    all_left_leader_vehicle = []
    temp = target_vehicle_id
    res = returnLeftLeaders(temp)
    while res:
        all_left_leader_vehicle.append(res)
        temp = res[0][0]
        res = returnLeftLeaders(temp)
    return all_left_leader_vehicle


def returnAllRightLeaders(target_vehicle_id):
    all_right_leader_vehicle = []
    temp = target_vehicle_id
    res = returnRightLeaders(temp)
    while res:
        all_right_leader_vehicle.append(res)
        temp = res[0][0]
        res = returnRightLeaders(temp)
    return all_right_leader_vehicle


def returnLeftLeaders(target_vehicle_id):
    all_left_leader_vehicle = []
    temp_vehicle_id = target_vehicle_id
    if traci.vehicle.getLeftLeaders(temp_vehicle_id) != ():
        left_leader = list(traci.vehicle.getLeftLeaders(temp_vehicle_id))[0]
        all_left_leader_vehicle.append(left_leader)
        temp_vehicle_id = left_leader[0]
        while traci.vehicle.getLeader(temp_vehicle_id) is not None:
            leader = list(traci.vehicle.getLeader(temp_vehicle_id))
            all_left_leader_vehicle.append(leader)
            temp_vehicle_id = leader[0]
    return all_left_leader_vehicle


def returnRightLeaders(target_vehicle_id):
    all_right_leader_vehicle = []
    temp_vehicle_id = target_vehicle_id
    if traci.vehicle.getRightLeaders(temp_vehicle_id) != ():
        right_leader = list(traci.vehicle.getRightLeaders(temp_vehicle_id))[0]
        all_right_leader_vehicle.append(right_leader)
        temp_vehicle_id = right_leader[0]
        while traci.vehicle.getLeader(temp_vehicle_id) is not None:
            leader = list(traci.vehicle.getLeader(temp_vehicle_id))
            all_right_leader_vehicle.append(leader)
            temp_vehicle_id = leader[0]
    return all_right_leader_vehicle


# start sumo/sumo-gui
def generate_routeFile():
    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    traci.start(['sumo-gui', "-c", "suzhouMap.sumocfg"])

    step = 0

    while step < 3600:
        time.sleep(0.3)

        global flag
        flag = 0

        while flag == 1:    # 当flag=1时，start_simulation()在通过traci向sumo请求
            print('waiting for opengl')

        traci.simulationStep()  # 当flag=0时，进行下一步仿真
        flag = 1


        # if (step > 15) & (step < 20):
        #     print('start')
        #     target_vehicle_id = 'veh0'  # 要获取信息的目标车辆ID
        #     print('###### speed:', '%.2f' % traci.vehicle.getSpeed(target_vehicle_id), 'm/s')

        step += 1
    traci.close()


# set window parameter
def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    # print(size)
    root.geometry(size)


def setWindow():
    root = tk.Tk()
    root.title('Peripheral Information')

    root.geometry("350x80+0+150")
    root.configure(bg='white')

    root.attributes("-topmost", True)

    Entry_1 = tk.Entry(root, text='input your text here', bg="white")
    Entry_1.place(x=130, y=10)

    # 开始用OpenGL模拟
    def start_simulation():
        vertex_src = """
        # version 330

        layout(location = 0) in vec3 a_position;
        layout(location = 1) in vec2 a_texture;
        layout(location = 2) in vec3 a_normal;

        uniform mat4 model;
        uniform mat4 projection;
        uniform mat4 view;

        out vec2 v_texture;

        void main()
        {
            gl_Position = projection * view * model * vec4(a_position, 1.0);
            v_texture = a_texture;
        }
        """

        fragment_src = """
        # version 330

        in vec2 v_texture;

        out vec4 out_color;

        uniform sampler2D s_texture;

        void main()
        {
            out_color = texture(s_texture, v_texture);
        }
        """

        # glfw callback functions
        def window_resize(window, width, height):
            glViewport(0, 0, width, height)
            projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
            glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

        # initializing glfw library
        if not glfw.init():
            raise Exception("glfw can not be initialized!")

        # creating the window
        window = glfw.create_window(1200, 600, "My OpenGL window", None, None)

        # check if window was created
        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        # set window's position
        glfw.set_window_pos(window, 800, 200)

        # set the callback function for window resize
        glfw.set_window_size_callback(window, window_resize)

        # make the context current
        glfw.make_context_current(window)

        # load here the 3d meshes
        car_indices, car_buffer = ObjLoader.load_model("meshes/car.obj")
        road_indices, road_buffer = ObjLoader.load_model("meshes/floor.obj")
        grass_indices, grass_buffer = ObjLoader.load_model("meshes/floor.obj")
        tree_indices, tree_buffer = ObjLoader.load_model("meshes/tree.obj")

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))


        # VAO and VBO
        VAO = glGenVertexArrays(4)
        VBO = glGenBuffers(4)
        # EBO = glGenBuffers(1)

        # car VAO
        glBindVertexArray(VAO[0])
        # car Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
        glBufferData(GL_ARRAY_BUFFER, car_buffer.nbytes, car_buffer, GL_STATIC_DRAW)

        # 下两行对应使用EBO，目前还有bug
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER, chibi_indices.nbytes, chibi_indices, GL_STATIC_DRAW)

        # car vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, car_buffer.itemsize * 8, ctypes.c_void_p(0))
        # car textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, car_buffer.itemsize * 8, ctypes.c_void_p(12))
        # car normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, car_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Road VAO
        glBindVertexArray(VAO[1])
        # Road Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
        glBufferData(GL_ARRAY_BUFFER, road_buffer.nbytes, road_buffer, GL_STATIC_DRAW)
        # Road vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, road_buffer.itemsize * 8, ctypes.c_void_p(0))
        # Road textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, road_buffer.itemsize * 8, ctypes.c_void_p(12))
        # Road normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, road_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # sky VAO
        glBindVertexArray(VAO[2])
        # sky Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
        glBufferData(GL_ARRAY_BUFFER, grass_buffer.nbytes, grass_buffer, GL_STATIC_DRAW)
        # sky vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, grass_buffer.itemsize * 8, ctypes.c_void_p(0))
        # sky textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, grass_buffer.itemsize * 8, ctypes.c_void_p(12))
        # sky normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, grass_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # tree VAO
        glBindVertexArray(VAO[3])
        # tree Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO[3])
        glBufferData(GL_ARRAY_BUFFER, tree_buffer.nbytes, tree_buffer, GL_STATIC_DRAW)
        # tree vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, tree_buffer.itemsize * 8, ctypes.c_void_p(0))
        # tree textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, tree_buffer.itemsize * 8, ctypes.c_void_p(12))
        # tree normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, tree_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # 导入纹理
        textures = glGenTextures(14)
        load_texture("meshes/car.png", textures[0])
        load_texture("textures/1_road_sidewalk.jpg", textures[1])
        load_texture("textures/2_road_sidewalk.jpg", textures[2])
        load_texture("textures/3_road_sidewalk.jpg", textures[3])
        load_texture("textures/4_road_sidewalk.jpg", textures[4])
        load_texture("textures/5_road_sidewalk.jpg", textures[5])
        load_texture("textures/6_road_sidewalk.jpg", textures[6])
        load_texture("textures/1_road.jpg", textures[7])
        load_texture("textures/2_road.jpg", textures[8])
        load_texture("textures/3_road.jpg", textures[9])
        load_texture("textures/4_road.jpg", textures[10])
        load_texture("textures/5_road.jpg", textures[11])
        load_texture("textures/6_road.jpg", textures[12])
        load_texture("textures/grass.png", textures[13])

        glUseProgram(shader)
        glClearColor(0.52, 0.80, 0.98, 1)   # 背景色，蓝色
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 读取当前tkinter窗口内，文本框内字符
        target_vehicle_id = Entry_1.get()

        projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)

        grass_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        grass_scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([5, 0, 5]))

        tree_scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.5, 0.5, 0.5]))

        model_loc = glGetUniformLocation(shader, "model")
        proj_loc = glGetUniformLocation(shader, "projection")
        view_loc = glGetUniformLocation(shader, "view")

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

        # test speed

        tree_move = 0
        tree_z_pos = 0
        road_move = 0

        # the main application loop
        while not glfw.window_should_close(window):
            time.sleep(0.2)
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            global flag
            # flag = 1
            while flag == 0:    # 当flag=0，generate_routeFile()正在通过traci向sumo发送请求
                print('waiting for gui')

            road_number = traci.edge.getLaneNumber(traci.vehicle.getRoadID(target_vehicle_id))
            lane_index = traci.vehicle.getLaneIndex(target_vehicle_id) + 1
            # 目标车辆前面的车，list（id，dist）
            all_leader_vehicle = returnLeaders(target_vehicle_id)
            # 目标车辆左边的车，list(最邻近的左车道list(id,dist)，次邻近的左车道list(id,dist))
            all_left_leader_vehicle = returnAllLeftLeaders(target_vehicle_id)
            all_right_leader_vehicle = returnAllRightLeaders(target_vehicle_id)
            speed = traci.vehicle.getSpeed(target_vehicle_id)
            print('###### speed:', '%.2f' % traci.vehicle.getSpeed(target_vehicle_id), 'm/s')

            # road_number = 5
            # lane_index = 2
            flag = 0

            # 目标车辆的位置
            target_car_x_pos = calculateCarPosition(road_number, lane_index)
            # 将目标车辆视角放在屏幕中心
            view = pyrr.matrix44.create_look_at(pyrr.Vector3([target_car_x_pos, 1, 0]),
                                                pyrr.Vector3([target_car_x_pos, 1, -20]),
                                                pyrr.Vector3([0, 1, 0]))
            # view = pyrr.matrix44.create_look_at(pyrr.Vector3([-15, -1, 0]),
            #                                     pyrr.Vector3([0, 0, -20]),
            #                                     pyrr.Vector3([0, 1, 0]))
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)


            # 绘制目标车辆前面的车
            glBindVertexArray(VAO[0])
            glBindTexture(GL_TEXTURE_2D, textures[0])

            car_z_pos = 0
            for item in all_leader_vehicle:
                car_z_pos = car_z_pos + 0.9 * item[1] + 4.5
                car_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([(target_car_x_pos, 0.3, -car_z_pos)]))
                glUniformMatrix4fv(model_loc, 1, GL_FALSE, car_pos)
                glDrawArrays(GL_TRIANGLES, 0, len(car_indices))

            # 绘制目标车辆左边所有的车
            car_lane_index = lane_index
            if all_left_leader_vehicle:
                car_z_pos = 0
                item = all_left_leader_vehicle[0]
                car_lane_index = car_lane_index + 1
                car_x_pos = calculateCarPosition(road_number, car_lane_index)
                for inner_item in item:
                    car_z_pos = car_z_pos + 0.9 * inner_item[1] + 4.5
                    car_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([(car_x_pos, 0.3, -car_z_pos)]))
                    glUniformMatrix4fv(model_loc, 1, GL_FALSE, car_pos)
                    glDrawArrays(GL_TRIANGLES, 0, len(car_indices))

            if all_left_leader_vehicle[1:]:
                count = 1
                for item in all_left_leader_vehicle[1:]:
                    car_z_pos = all_left_leader_vehicle[count-1][0][1]
                    car_lane_index = car_lane_index + 1
                    car_x_pos = calculateCarPosition(road_number, car_lane_index)
                    for inner_item in item:
                        car_z_pos = car_z_pos + 0.9 * inner_item[1] + 4.5
                        car_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([(car_x_pos, 0.3, -car_z_pos)]))
                        glUniformMatrix4fv(model_loc, 1, GL_FALSE, car_pos)
                        glDrawArrays(GL_TRIANGLES, 0, len(car_indices))
                    count = count + 1

            # 绘制目标车辆右边所有的车
            car_lane_index = lane_index
            if all_right_leader_vehicle:
                car_z_pos = 0
                item = all_right_leader_vehicle[0]
                car_lane_index = car_lane_index - 1
                car_x_pos = calculateCarPosition(road_number, car_lane_index)
                for inner_item in item:
                    car_z_pos = car_z_pos + 0.9 * inner_item[1] + 4.5
                    car_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([(car_x_pos, 0.3, -car_z_pos)]))
                    glUniformMatrix4fv(model_loc, 1, GL_FALSE, car_pos)
                    glDrawArrays(GL_TRIANGLES, 0, len(car_indices))

            if all_right_leader_vehicle[1:]:
                count = 1
                for item in all_right_leader_vehicle[1:]:
                    car_z_pos = all_right_leader_vehicle[count-1][0][1]
                    car_lane_index = car_lane_index - 1
                    car_x_pos = calculateCarPosition(road_number, car_lane_index)
                    for inner_item in item:
                        car_z_pos = car_z_pos + 0.9 * inner_item[1] + 4.5
                        car_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([(car_x_pos, 0.3, -car_z_pos)]))
                        glUniformMatrix4fv(model_loc, 1, GL_FALSE, car_pos)
                        glDrawArrays(GL_TRIANGLES, 0, len(car_indices))
                    count = count + 1

            # draw the grass
            glBindVertexArray(VAO[2])
            glBindTexture(GL_TEXTURE_2D, textures[13])
            model = pyrr.matrix44.multiply(grass_scale, grass_pos)
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            glDrawArrays(GL_TRIANGLES, 0, len(grass_buffer))

            # draw tree
            glBindVertexArray(VAO[3])
            glBindTexture(GL_TEXTURE_2D, 0)  # 因为还没给tree找到合适纹理或者导入.mtl文件，暂时解绑纹理
            if (tree_z_pos - tree_move) <= -64:
                tree_move = 0
            tree_move = tree_move + 0.1 * speed
            road_move = road_move + 0.1 * speed
            tree_z_pos = 8
            tree_x_pos = calculateCarPosition(road_number, road_number)
            for i in range(0, 8):

                tree_z_pos = tree_z_pos - 8
                tree_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([(tree_x_pos-5, -0.3, tree_z_pos + tree_move)]))
                model = pyrr.matrix44.multiply(tree_scale, tree_pos)
                glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
                glDrawArrays(GL_TRIANGLES, 0, len(tree_indices))

                tree_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([(-tree_x_pos+5, -0.3, tree_z_pos + tree_move)]))
                model = pyrr.matrix44.multiply(tree_scale, tree_pos)
                glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
                glDrawArrays(GL_TRIANGLES, 0, len(tree_indices))

            # draw the road
            if road_move >= 36:
                road_move = 0
            road_scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.1 * road_number, 0, -5]))
            road_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0.1, 0 + road_move]))
            model = pyrr.matrix44.multiply(road_scale, road_pos)
            glBindVertexArray(VAO[1])
            if road_number == 2:
                glBindTexture(GL_TEXTURE_2D, textures[1])
            elif road_number == 3:
                glBindTexture(GL_TEXTURE_2D, textures[2])
            elif road_number == 4:
                glBindTexture(GL_TEXTURE_2D, textures[3])
            elif road_number == 5:
                glBindTexture(GL_TEXTURE_2D, textures[4])
            elif road_number == 6:
                glBindTexture(GL_TEXTURE_2D, textures[5])
            elif road_number == 7:
                glBindTexture(GL_TEXTURE_2D, textures[6])
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            glDrawArrays(GL_TRIANGLES, 0, len(road_indices))

            glfw.swap_buffers(window)


        # terminate glfw, free up allocated resources
        glfw.terminate()

    def reset():
        Entry_1.delete(0, 'end')
        all_vehicle_id = list(traci.vehicle.getIDList())

        for i in all_vehicle_id:
            traci.vehicle.setColor(i, (255, 255, 0))

    Button_1 = tk.Button(root, text="Enter", command=start_simulation, bg="white")
    Button_1.place(x=50, y=40)
    Button_2 = tk.Button(root, text="Reset", command=reset, bg="white")
    Button_2.place(x=160, y=40)
    root.mainloop()  # 进入消息循环


def calculateCarPosition(road_number, lane_index):
    if road_number % 2 == 0:
        if lane_index <= road_number / 2:
            return ((road_number / 2 + 1) - lane_index) * 5 - 2.5
        else:
            return (road_number / 2 - lane_index) * 5 + 2.5

    if road_number % 2 == 1:
        if lane_index == (road_number + 1) / 2:
            return 0
        else:
            return ((road_number + 1) / 2 - lane_index) * 5


if __name__ == "__main__":
    thread1 = threading.Thread(target=setWindow)
    thread2 = threading.Thread(target=generate_routeFile)
    thread1.start()
    time.sleep(0.5)
    thread2.start()
