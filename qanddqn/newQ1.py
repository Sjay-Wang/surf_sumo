import json
import os

import traci
import time
import threading
import numpy as np
import random
import matplotlib.pyplot as plt
from RLDQN_brain import DeepQNetwork



from RL_brain import QLearningTable

def Qlearnning_routefile(trafficlight_time):
    sumofile = r"C:/Users/23368/Desktop/sumoTest/sumot7.sumocfg"
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

def step1(action,trafficlight_time,dictx):
    beforetime= dictx.get(str(trafficlight_time))
    #print(trafficlight_time)
    trafficlight_time1=[i for i in trafficlight_time]
    if action==0:
        if trafficlight_time1[0]<100:
            trafficlight_time1[0]= trafficlight_time1[0]+10
    if action==1:
        if trafficlight_time1[1]<100:
            trafficlight_time1[1]= trafficlight_time1[1]+10
    if action==2:
        if trafficlight_time1[2]<100:
            trafficlight_time1[2]=trafficlight_time1[2]+10
    if action==3:
        if trafficlight_time1[3]<100:
            trafficlight_time1[3]=trafficlight_time1[3]+10
    if action==4:
        if trafficlight_time1[0]>50:
            trafficlight_time1[0]=trafficlight_time1[0]-10
    if action==5:
        if trafficlight_time1[1]>50:
            trafficlight_time1[1]=trafficlight_time1[1]-10
    if action==6:
        if trafficlight_time1[2]>50:
            trafficlight_time1[2]=trafficlight_time1[2]-10
    if action==7:
        if trafficlight_time1[3]>50:
            trafficlight_time1[3]=trafficlight_time1[3]-10
    if action==8:
        return 0,trafficlight_time1
    #print(trafficlight_time)
    aftertime = dictx.get(str(trafficlight_time1))
    #print(beforetime-aftertime)
    #print(trafficlight_time1,trafficlight_time)
    return beforetime-aftertime,trafficlight_time1

def step(action,trafficlight_time,dictx):
    beforetime= dictx.get(str(trafficlight_time))
    #print(trafficlight_time)
    trafficlight_time1=[i for i in trafficlight_time]
    if action==0:
        if trafficlight_time1[0]<80:
            trafficlight_time1[0]= trafficlight_time1[0]+5
    if action==1:
        if trafficlight_time1[1]<80:
            trafficlight_time1[1]= trafficlight_time1[1]+5
    if action==2:
        if trafficlight_time1[2]<80:
            trafficlight_time1[2]=trafficlight_time1[2]+5
    if action==3:
        if trafficlight_time1[3]<80:
            trafficlight_time1[3]=trafficlight_time1[3]+5
    if action==4:
        if trafficlight_time1[0]>30:
            trafficlight_time1[0]=trafficlight_time1[0]-5
    if action==5:
        if trafficlight_time1[1]>30:
            trafficlight_time1[1]=trafficlight_time1[1]-5
    if action==6:
        if trafficlight_time1[2]>30:
            trafficlight_time1[2]=trafficlight_time1[2]-5
    if action==7:
        if trafficlight_time1[3]>30:
            trafficlight_time1[3]=trafficlight_time1[3]-5
    if action==8:
        return 0,trafficlight_time1
    #print(trafficlight_time)
    aftertime = dictx.get(str(trafficlight_time1))
    #print(beforetime-aftertime)
    #print(trafficlight_time1,trafficlight_time)
    return beforetime-aftertime,trafficlight_time1

def update():

    #observation = [random.randint(1, 4) * 50, random.randint(1, 4) * 50, random.randint(1, 4) * 50,
    #               random.randint(1, 4) * 50]

    #observation1 = [100, 100, 100, 100]
    #bestobservation = observation
    dictx = makeDic()
    observation = [80, 80, 80, 80]
    observation_rem = np.zeros(4001)
    rewardall = 0
    nember = 0
    for i in range(100):
    # 对每一个训练,随机选择一种状态


        times = 0


        #print(state)
        while True:
            list0 = []
            list1 = []
            # 选择当前状态下的所有可能动作]
            for i in range(0,9):
                reward_, newob = step(i, observation,dictx)
                list0.append(reward_)
            #RL.check_state_exist(observation,list)
            action = RL.choose_action(str(observation),list0)
            #print(action)

            reward,observation_= step(action,observation,dictx)
            for i in range(0,9):
                reward_, newob = step(i, observation_,dictx)
                list1.append(reward_)
            print("The reward is", reward)

            print(observation)


            nember=nember+1
            RL.learn(str(observation), action, reward, str(observation_), list1)
            rewardall=rewardall+reward
            print(rewardall)
            observation_rem[nember] = rewardall
            print(RL.q_table)
            observation = observation_
            times = times + 1
            if times>=40:

                break

            #print(observation_)
            #if reward>


    index = np.arange(0, 5000, 1)
    observation_rem1 = updateDQN()
    plt.plot(index, observation_rem, c='blue', linestyle='solid')
    plt.plot(index, observation_rem1, c='green', linestyle='solid')
    plt.xlabel("Number of Iteration")
    plt.ylabel("reward")
    plt.show()  # 同时显示显示训练集和测试集损失曲线
    print('This is the best',observation)

def updateDQN():

    #observation = [random.randint(1, 4) * 50, random.randint(1, 4) * 50, random.randint(1, 4) * 50,
    #               random.randint(1, 4) * 50]

    #observation1 = [100, 100, 100, 100]
    #bestobservation = observation
    stepx = 0
    observation = [80, 80, 80, 80]
    dictx = makeDic()
    observation_rem = np.zeros(4001)
    nember=0
    rewardall=0
    for i in range(100):
    # 对每一个训练,随机选择一种状态
        times = 0
        reward = 0
        #print(state)
        while True:
            action = RL1.choose_action(observation)
            reward,observation_= step(action,observation,dictx)
            print("The reward is", reward)
            RL1.store_transition(list(observation), action, reward, observation_)
            if (stepx > 200) and (stepx % 5 == 0):
                RL1.learn()
            observation = observation_
            times = times + 1
            nember = nember + 1
            rewardall = rewardall + reward
            observation_rem[nember]=rewardall
            if times>=40:

                break
            stepx += 1
            print(RL1.epsilon)

            #print(observation_)
            #if reward>
    return observation_rem
    #print('This is the best',observation)

dict_ = {"vehicle_x": 0}
def makeDic():
    if (os.path.exists('C:/Users/23368/Desktop/dic1.json') != True):
        for i in range(5, 11):
            for j in range(5, 11):
                for k in range(5, 11):
                    for l in range(5, 11):
                        answer = Qlearnning_routefile([0 + i * 10, 0 + j * 10, 0 + k * 10, 0 + l * 10])
                        dict_[str([0 + i * 10, 0 + j * 10, 0 + k * 10, 0 + l * 10])]=answer
        jsonstr = json.dumps(dict_)
        filename = open('C:/Users/23368/Desktop/dic1.json', 'w')  # dict转josn
        filename.write(jsonstr)
        return dict_
    else:
        filename = open('C:/Users/23368/Desktop/dic2.json', 'r')
        dict = json.loads(filename.read())
        return dict


if __name__ == '__main__':
    RL = QLearningTable(actions=list(range(9)))
    #trafficlight_time=[100,100,100,100]
    #makeDic()
    RL1 = DeepQNetwork(9, 4,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    print(makeDic())
    update()


