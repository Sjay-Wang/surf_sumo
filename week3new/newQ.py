import traci
import time
import threading
import numpy as np
import random
from RL_brain import QLearningTable

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
    beforetime= dict_.get(str(trafficlight_time))
    #print(trafficlight_time)
    trafficlight_time1=[i for i in trafficlight_time]
    if action==0:
        if trafficlight_time1[0]<100:
            trafficlight_time1[0]= trafficlight_time1[0]+50
    if action==1:
        if trafficlight_time1[1]<100:
            trafficlight_time1[1]= trafficlight_time1[1]+50
    if action==2:
        if trafficlight_time1[2]<100:
            trafficlight_time1[2]=trafficlight_time1[2]+50
    if action==3:
        if trafficlight_time1[3]<100:
            trafficlight_time1[3]=trafficlight_time1[3]+50
    if action==4:
        if trafficlight_time1[0]>50:
            trafficlight_time1[0]=trafficlight_time1[0]-50
    if action==5:
        if trafficlight_time1[1]>50:
            trafficlight_time1[1]=trafficlight_time1[1]-50
    if action==6:
        if trafficlight_time1[2]>50:
            trafficlight_time1[2]=trafficlight_time1[2]-50
    if action==7:
        if trafficlight_time1[3]>50:
            trafficlight_time1[3]=trafficlight_time1[3]-50
    if action==8:
        return 1,trafficlight_time1
    #print(trafficlight_time)
    aftertime = dict_.get(str(trafficlight_time1))
    #print(beforetime-aftertime)
    #print(trafficlight_time1,trafficlight_time)
    return beforetime-aftertime,trafficlight_time1

def update():

    #observation = [random.randint(1, 4) * 50, random.randint(1, 4) * 50, random.randint(1, 4) * 50,
    #               random.randint(1, 4) * 50]

    #observation1 = [100, 100, 100, 100]
    #bestobservation = observation
    for i in range(50):
    # 对每一个训练,随机选择一种状态
        observation = [100, 100, 100, 100]
        times = 0
        reward = 0
        #print(state)
        while True:
            list0 = []
            list1 = []
            # 选择当前状态下的所有可能动作]
            for i in range(0,9):
                reward_, newob = step(i, observation)
                list0.append(reward_)
            #RL.check_state_exist(observation,list)
            action = RL.choose_action(str(observation),list0)
            #print(action)

            reward,observation_= step(action,observation)
            for i in range(0,9):
                reward_, newob = step(i, observation_)
                list1.append(reward_)
            print("The reward is", reward)

            print(observation)
            RL.learn(str(observation), action, reward, str(observation_), list1)


            print(RL.q_table)
            observation = observation_
            times = times + 1
            if times>40:

                break

            #print(observation_)
            #if reward>

    print('This is the best',observation)

dict_ = {"vehicle_x": 0}
def makeDic():
    for i in range(1, 3):
        for j in range(1, 3):
            for k in range(1, 3):
                for l in range(1, 3):
                    answer = Qlearnning_routefile([0 + i * 50, 0 + j * 50, 0 + k * 50, 0 + l * 50])
                    dict_[str([0 + i * 50, 0 + j * 50, 0 + k * 50, 0 + l * 50])]=answer
    return dict_


if __name__ == '__main__':
    RL = QLearningTable(actions=list(range(9)))
    #trafficlight_time=[100,100,100,100]
    makeDic()
    #print(makeDic())
    update()
