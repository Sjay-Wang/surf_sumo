import os
import sys
import random
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
import traci
import threading

sumofile="C:/Users/23368/Desktop/sumoTest/sumot6.sumocfg"
traci.start(["sumo-gui", "-c",sumofile ])
def generate_routefile():
    step = 0
    while step < 1000:
        time.sleep(0.1)
        traci.simulationStep()
        step += 1
        trafficlight()
    traci.close()

def trafficlight():
    print(traci.edge.getLastStepVehicleNumber("gneE2"))
    if (traci.edge.getLastStepVehicleNumber("gneE2")==0):
        traci.trafficlight.setRedYellowGreenState("2","rrgg")

if __name__ == "__main__":
     generate_routefile()
