import os
import sys
import random
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
import traci
import threading

sumofile="C:/Users/23368/Desktop/sumoTest/sumot5.sumocfg"
traci.start(["sumo-gui", "-c",sumofile ])
def generate_routefile():
     step = 0
     while step < 1000:
         time.sleep(1)
         traci.simulationStep()
         step += 1
         simulation_current_time=traci.simulation.getTime()
         #print("The time of the simulation",simulation_current_time)
         all_Vehicle_Id=traci.vehicle.getIDList()
         #print("The ID of the vehicle", all_Vehicle_Id)
         all_Vehicle_position = [(i,traci.vehicle.getPosition(i)) for i in all_Vehicle_Id]
         #traci.vehicle.getDistance()
         #print( all_Vehicle_position)
         all_Vehicle_speed = [(i, traci.vehicle.getSpeed(i)) for i in all_Vehicle_Id]
         print(all_Vehicle_speed)
         if ("vehicle_0" in all_Vehicle_Id):
             traci.vehicle.setSpeed("vehicle_0",30)
             if not (traci.vehicle.getLeader('vehicle_0') is None):
                 #print(traci.vehicle.getLeader('vehicle_0'))
                 if (traci.vehicle.getLeader('vehicle_0')[1] <= 10):
                     traci.vehicle.changeLane('vehicle_0', 1, 1)
         if ("vehicle_1" in all_Vehicle_Id):
             traci.vehicle.setSpeed("vehicle_1", 10)
         if ("vehicle_2" in all_Vehicle_Id):
             traci.vehicle.setSpeed("vehicle_2", 30)
             traci.vehicle.changeTarget('vehicle_2','gneE5')
         if ("vehicle_3" in all_Vehicle_Id):
             traci.vehicle.setSpeed("vehicle_3", 30)

     traci.close()


def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    print(size)
    root.geometry(size)


def setWindow():
    root = tk.Tk()
    root.title('checkspeed')

    center_window(root, 300, 240)
    root.maxsize(600, 400)
    root.minsize(300, 240)
    Labela = ttk.Label(root,text="Enter the vehicle")
    Labela.place(x=20,y=10)
    Entrya = ttk.Entry(root)
    Entrya.place(x=130,y=10)
    text = Text(root, width=40, height=12, undo=True, autoseparators=True)
    text.place(x=10, y=70)
    def checkspeed():
        getVehicle = Entrya.get()
        if not (traci.vehicle.getSpeed(getVehicle) is None):
            getVehicleColor = traci.vehicle.getColor(getVehicle)
            print(getVehicleColor)
            color_red = (255, 0, 0)
            traci.vehicle.setColor(getVehicle,color_red)
            if not (traci.vehicle.getLeader(getVehicle) is None):
                text.insert(END, traci.vehicle.getLeader(getVehicle),traci.vehicle.getSpeed(getVehicle))
                text.insert(END, '\n')
            else:
                text.insert(END, traci.vehicle.getSpeed(getVehicle))
                text.insert(END, '\n')
        time.sleep(0.5)
      #  if not (getVehicle is None):
        #    traci.vehicle.setColor(getVehicle, getVehicleColor)

    def reset():
        Entrya.delete(0,'end')
        text.delete('1.0','end')
    Buttona = ttk.Button(root, text="Enter" ,command=checkspeed)
    Buttona.place(x=50, y=40)
    Buttona = ttk.Button(root, text="Reset", command=reset)
    Buttona.place(x=160, y=40)
    root.mainloop()  # 进入消息循环

if __name__ == "__main__":
     thread1 = threading.Thread(target=setWindow)
     thread2 = threading.Thread(target=generate_routefile)
     thread2.start()
     thread1.start()

