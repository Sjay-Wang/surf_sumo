import traci
import time
import threading
import numpy as np
import random
from RL_brain import QLearningTable



γ = 0.8

def Qlearnning_routefile(trafficlight_time):
    sumofile = "C:/Users/23368/Desktop/sumoTest/sumot7.sumocfg"
    #traci.start(["sumo-gui", "-c", sumofile])
    traci.start(["sumo", "-c", sumofile])
    dict = {"vehicle_x": 0}

    step = 0
    traci.route.add("route0", ["gneE0", "gneE1"])
    traci.route.add("route1", ["gneE0", "gneE2"])
    traci.route.add("route2", ["-gneE2", "gneE3"])
    traci.route.add("route3", ["-gneE2", "-gneE0"])
    colora = (125, 255, 255, 255)
    colorb = (125, 255, 0, 255)
    colorc = (125, 0, 255, 255)
    colord = (225, 255, 255, 255)
    while step < 500:
        #time.sleep(0.3)
        traci.simulationStep()
        step += 1
        if(step%(trafficlight_time[0]+trafficlight_time[1]+trafficlight_time[2]+trafficlight_time[3])<trafficlight_time[0]):
            traci.trafficlight.setRedYellowGreenState('2',"grrrrrrrrrrrrrrrr")
        elif(step%(trafficlight_time[0]+trafficlight_time[1]+trafficlight_time[2]+trafficlight_time[3])<trafficlight_time[0]+trafficlight_time[1]):
            traci.trafficlight.setRedYellowGreenState('2', "rggrrrrrrrrrrrrrr")
        elif(step%(trafficlight_time[0]+trafficlight_time[1]+trafficlight_time[2]+trafficlight_time[3]) < trafficlight_time[0] + trafficlight_time[1] + trafficlight_time[2]):
            traci.trafficlight.setRedYellowGreenState('2', "rrrrrrrrrrrrrggr")
        elif (step%(trafficlight_time[0]+trafficlight_time[1]+trafficlight_time[2]+trafficlight_time[3]) < trafficlight_time[0] + trafficlight_time[1] + trafficlight_time[2] + trafficlight_time[3]):
            traci.trafficlight.setRedYellowGreenState('2', "rrrrrrrrrrrrrrrg")
        if(step%12==0):
            traci.vehicle.add("0" + str(step/6), "route0")
            traci.vehicle.setColor("0" + str(step/6), colora)
            traci.vehicle.changeLane("0" + str(step/6),0,1)
            traci.vehicle.setLaneChangeMode("0" + str(step/6),0b001000000000)
            #设置车辆禁止变道
            traci.vehicle.add("1" + str(step/6), "route1")
            traci.vehicle.setColor("1" + str(step / 6), colorb)
            traci.vehicle.changeLane("1" + str(step / 6), 1, 1)
            #traci.vehicle.setLaneChangeMode("1" + str(step / 6), 0b001000000000)
            traci.vehicle.add("2" + str(step/6), "route2")
            traci.vehicle.setColor("2" + str(step / 6), colorc)
            traci.vehicle.changeLane("2" + str(step / 6), 1, 1)
            traci.vehicle.setLaneChangeMode("2" + str(step / 6), 0b001000000000)
            traci.vehicle.add("3" + str(step/6), "route3")
            traci.vehicle.setColor("3" + str(step / 6), colord)
            traci.vehicle.changeLane("3" + str(step / 6), 0, 1)
            traci.vehicle.setLaneChangeMode("3" + str(step / 6), 0b001000000000)
        all_Vehicle_Id1 = traci.vehicle.getIDList()
        for i in all_Vehicle_Id1:
            if i not in dict:
                dict[i] = traci.vehicle.getAccumulatedWaitingTime(i)
            else:
                if traci.vehicle.getAccumulatedWaitingTime(i) > dict.get(i):
                    dict[i] = traci.vehicle.getAccumulatedWaitingTime(i)
    traci.close()
    value = 0
    for k, v in dict.items():
        value = v + value
        # print("The waitingtime of the vehicle", value)
    #print(value)
    return value
        #if(step == trafficlight_time[0] + trafficlight_time[1] + trafficlight_time[2] + trafficlight_time[3]):
         #   for i in all_Vehicle_Id:
          #      traci.vehicle.remove(i)
        #    step=0


def step(action,trafficlight_time):
    beforetime= Qlearnning_routefile(trafficlight_time)
    #print(trafficlight_time)
    if action==0:
        if trafficlight_time[0]<200:
            trafficlight_time[0]= trafficlight_time[0]+50
    if action==1:
        if trafficlight_time[1]<200:
            trafficlight_time[1]= trafficlight_time[1]+50
    if action==2:
        if trafficlight_time[2]<200:
            trafficlight_time[2]=trafficlight_time[2]+50
    if action==3:
        if trafficlight_time[3]<200:
            trafficlight_time[3]=trafficlight_time[3]+50
    if action==4:
        if trafficlight_time[0]>0:
            trafficlight_time[0]=trafficlight_time[0]-50
    if action==5:
        if trafficlight_time[1]>0:
            trafficlight_time[1]=trafficlight_time[1]-50
    if action==6:
        if trafficlight_time[2]>0:
            trafficlight_time[2]=trafficlight_time[2]-50
    if action==7:
        if trafficlight_time[3]>0:
            trafficlight_time[3]=trafficlight_time[3]-50
    #print(trafficlight_time)
    aftertime = Qlearnning_routefile(trafficlight_time)
    #print(beforetime-aftertime)
    return beforetime-aftertime,trafficlight_time
def update():

    #observation = [random.randint(1, 4) * 50, random.randint(1, 4) * 50, random.randint(1, 4) * 50,
    #               random.randint(1, 4) * 50]
    observation = [100, 100, 100, 100]
    for i in range(50):
    # 对每一个训练,随机选择一种状态

        #print(state)
        while True:
            # 选择当前状态下的所有可能动作
            action = RL.choose_action(str(observation))
            #print(action)
            reward,observation_= step(action,observation)
            RL.learn(str(observation), action, reward, str(observation_))

            print("The reward is",reward)
            print(RL.q_table)
            if reward <= 0:

                break
            observation = observation_
    print('This is the best',observation)



if __name__ == '__main__':
    RL = QLearningTable(actions=list(range(8)))
    #trafficlight_time=[100,100,100,100]

    update()
    #Qlearnning_routefile([50, 50, 0, 50])
    #print(Qlearnning_routefile([0, 150, 0, 50])-Qlearnning_routefile([50, 50, 50, 0]))
