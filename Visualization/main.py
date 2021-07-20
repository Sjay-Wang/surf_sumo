import threading
import time
import traci
import optparse
import os
from tkinter import *
import traci
import tkinter as tk
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture
from ObjLoader import ObjLoader
import numpy as np
import traci
import tkinter as tk

# 验证环境变量
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


def generate_routeFile():
    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    traci.start(['sumo', "-c", "suzhouMap.sumocfg"])  # 打开对应的sumo文件

    step = 0

    while step < 360000:
        # time.sleep(1)
        traci.simulationStep()
        step += 1

        all_vehicle_id = traci.vehicle.getIDList()  # 输出当前画面所有车辆ID
        # print(all_vehicle_id)

        # if step == 36:
        #
        #     target_vehicle_id = 'veh0'  # 要获取信息的目标车辆ID
        #     print()
        #     print('################## target car information ######')
        #     position = traci.vehicle.getPosition(target_vehicle_id)
        #     position3D = traci.vehicle.getPosition3D(target_vehicle_id)
        #     angle = traci.vehicle.getAngle(target_vehicle_id)
        #     # 车辆信号灯状况，对应https://sumo.dlr.de/docs/TraCI/Vehicle_Signalling.html
        #     signals = traci.vehicle.getSignals(target_vehicle_id)
        #     print('###### type:', traci.vehicle.getTypeID(target_vehicle_id))
        #     print('###### length:', traci.vehicle.getLength(target_vehicle_id), 'm')
        #     print('###### width:', traci.vehicle.getWidth(target_vehicle_id), 'm')
        #     print('###### height:', traci.vehicle.getHeight(target_vehicle_id), 'm')
        #     print('###### color:', traci.vehicle.getColor(target_vehicle_id))
        #     print('###### mileage:', '%.2f' % traci.vehicle.getDistance(target_vehicle_id), 'm')    # 行车里程
        #     print('###### speed:', '%.2f' % traci.vehicle.getSpeed(target_vehicle_id), 'm/s')
        #     print('###### real speed:', '%.2f' % traci.vehicle.getSpeedWithoutTraCI(target_vehicle_id), 'm/s')  # 如果不受traci控制
        #     print('###### max speed:', '%.2f' % traci.vehicle.getMaxSpeed(target_vehicle_id), 'm/s')
        #     print('###### maximum acceleration:', '%.2f' % traci.vehicle.getAccel(target_vehicle_id), 'm/s^2')
        #     print('###### maximum deceleration:', '%.2f' % traci.vehicle.getDecel(target_vehicle_id), 'm/s^2')
        #     # 一步的燃油量，费电量
        #     print('###### Fuel Consumption:', '%.2f' % traci.vehicle.getFuelConsumption(target_vehicle_id), 'ml/s')
        #     print('###### Electricity Consumption:',
        #           '%.2f' % traci.vehicle.getElectricityConsumption(target_vehicle_id), 'Wh/s')
        #     print('###### lateral speed:',
        #           '%.2f' % traci.vehicle.getLateralSpeed(target_vehicle_id), 'm/s')
        #     print('###### acceleration:', '%.2f' % traci.vehicle.getAcceleration(target_vehicle_id), 'm/s^2')
        #     print()
        #     print('################## road information ######')
        #     road_id = traci.vehicle.getRoadID(target_vehicle_id)
        #     lane_id = traci.vehicle.getLaneID(target_vehicle_id)
        #     lane_index = traci.vehicle.getLaneIndex(target_vehicle_id)
        #     route_id = traci.vehicle.getRouteID(target_vehicle_id)
        #     route_index = traci.vehicle.getRouteIndex(target_vehicle_id)
        #     edges_made_of_route = traci.vehicle.getRoute(target_vehicle_id)
        #     lane_position = traci.vehicle.getLanePosition(target_vehicle_id)    # 车前保险杠到所在车道最开始的距离
        #     print('###### which lane the car in:', lane_index + 1)
        #     print('###### number of lanes in current road:', traci.edge.getLaneNumber(road_id))
        #     print('###### current lane length:', traci.lane.getLength(lane_id), 'm')
        #     print('###### current lane width:', traci.lane.getWidth(lane_id), 'm')
        #     print()
        #     print('################## surrounding information ######')
        #     # traci.vehicle.getNeighbors(target_vehicle_id, 1)
        #     next_stop = traci.vehicle.getNextStops(target_vehicle_id)
        #     if not (traci.vehicle.getNextTLS(target_vehicle_id) is None):
        #         # next_TLS = list(traci.vehicle.getNextTLS(target_vehicle_id))[0][0]
        #         # edges_made_of_TLS = traci.trafficlight.getControlledLanes(next_TLS)
        #         print('###### next traffic lights:', traci.vehicle.getNextTLS(target_vehicle_id))
        #         # print('###### traffic time left:', traci.trafficlight.getNextSwitch(next_TLS)-step)
        #     if not (traci.vehicle.getLeader(target_vehicle_id) is None):
        #         print('###### distance of front car:', '%.2f' % traci.vehicle.getLeader(target_vehicle_id)[1], 'm')
        #     if not (traci.vehicle.getFollower(target_vehicle_id) is None):
        #         print('###### distance of back car:', '%.2f' % traci.vehicle.getFollower(target_vehicle_id)[1], 'm')
        #
        #     print()

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
        window = glfw.create_window(600, 600, "My OpenGL window", None, None)

        # check if window was created
        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        # set window's position
        glfw.set_window_pos(window, 400, 200)

        # set the callback function for window resize
        glfw.set_window_size_callback(window, window_resize)

        # make the context current
        glfw.make_context_current(window)

        # load here the 3d meshes
        car_indices, car_buffer = ObjLoader.load_model("meshes/car.obj")
        road_indices, road_buffer = ObjLoader.load_model("meshes/floor.obj")
        quad_vertices = [-0.5, -0.5, 0, 0.0, 0.0,
                         0.5, -0.5, 0, 1.0, 0.0,
                         0.5, 0.5, 0, 1.0, 1.0,
                         -0.5, 0.5, 0, 0.0, 1.0]

        quad_indices = [0, 1, 2, 2, 3, 0]

        quad_vertices = np.array(quad_vertices, dtype=np.float32)
        quad_indices = np.array(quad_indices, dtype=np.uint32)

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))

        # VAO and VBO
        VAO = glGenVertexArrays(3)
        VBO = glGenBuffers(3)
        EBO = glGenBuffers(1)

        # Chibi VAO
        glBindVertexArray(VAO[0])
        # Chibi Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
        glBufferData(GL_ARRAY_BUFFER, car_buffer.nbytes, car_buffer, GL_STATIC_DRAW)

        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER, chibi_indices.nbytes, chibi_indices, GL_STATIC_DRAW)

        # chibi vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, car_buffer.itemsize * 8, ctypes.c_void_p(0))
        # chibi textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, car_buffer.itemsize * 8, ctypes.c_void_p(12))
        # chibi normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, car_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Road VAO
        glBindVertexArray(VAO[1])
        # Road Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
        glBufferData(GL_ARRAY_BUFFER, road_buffer.nbytes, road_buffer, GL_STATIC_DRAW)

        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER, road_indices.nbytes, road_indices, GL_STATIC_DRAW)

        # chibi vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, road_buffer.itemsize * 8, ctypes.c_void_p(0))
        # chibi textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, road_buffer.itemsize * 8, ctypes.c_void_p(12))
        # chibi normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, road_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Quad VAO
        glBindVertexArray(VAO[2])
        # Quad Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
        glBufferData(GL_ARRAY_BUFFER, quad_vertices.nbytes, quad_vertices, GL_STATIC_DRAW)

        # Quad Element Buffer Object
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, quad_indices.nbytes, quad_indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, quad_vertices.itemsize * 5, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, quad_vertices.itemsize * 5, ctypes.c_void_p(12))

        textures = glGenTextures(3)
        load_texture("meshes/car.png", textures[0])
        load_texture("meshes/Overpass.jpg", textures[1])
        load_texture("textures/grass.jpg", textures[2])

        glUseProgram(shader)
        glClearColor(0.2, 0.6, 0.2, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
        car_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -1.5, 0]))
        car_pos_2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-2, -1.5, -4]))
        road_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -2, 0]))
        road_scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.2, 0, 1.5]))

        # eye, target, up
        view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 10]), pyrr.Vector3([0, 0, 0]),
                                            pyrr.Vector3([0, 1, 0]))

        model_loc = glGetUniformLocation(shader, "model")
        proj_loc = glGetUniformLocation(shader, "projection")
        view_loc = glGetUniformLocation(shader, "view")

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        # type = traci.vehicle.getTypeID('veh0')
        # print(type)

        type = 'veh_passenger'

        # the main application loop
        while not glfw.window_should_close(window):
            glfw.poll_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # rot_y = pyrr.Matrix44.from_y_rotation(-0.8 * glfw.get_time())
            # model = pyrr.matrix44.multiply(rot_y, car_pos)

            if type == 'veh_passenger':
                # draw the chibi character
                glBindVertexArray(VAO[0])
                glBindTexture(GL_TEXTURE_2D, textures[0])
                glUniformMatrix4fv(model_loc, 1, GL_FALSE, car_pos)
                glDrawArrays(GL_TRIANGLES, 0, len(car_indices))
                glUniformMatrix4fv(model_loc, 1, GL_FALSE, car_pos_2)
                glDrawArrays(GL_TRIANGLES, 0, len(car_indices))
                # glDrawElements(GL_TRIANGLES, len(car_indices), GL_UNSIGNED_INT, None)


            model = pyrr.matrix44.multiply(road_scale, road_pos)
            # draw the chibi character
            glBindVertexArray(VAO[1])
            road = 2
            if road == 1:
                glBindTexture(GL_TEXTURE_2D, textures[0])
            elif road == 2:
                glBindTexture(GL_TEXTURE_2D, textures[1])
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            glDrawArrays(GL_TRIANGLES, 0, len(road_indices))
            # glDrawElements(GL_TRIANGLES, len(car_indices), GL_UNSIGNED_INT, None)

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



if __name__ == "__main__":
    thread1 = threading.Thread(target=setWindow)
    thread2 = threading.Thread(target=generate_routeFile)
    thread2.start()
    time.sleep(0.5)
    thread1.start()
