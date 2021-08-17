import json
import os

import traci
from RL_brain import DeepQNetwork
from RLQ_brain import QLearningTable
import time
import threading
import numpy as np
import random



def Qlearnning_routefile(trafficlight_time):
    sumofile = "C:/Users/23368/Desktop/sumoTest/sumot9.sumocfg"
    #traci.start(["sumo-gui", "-c", sumofile])
    traci.start(["sumo", "-c", sumofile])
    dict = {"vehicle_x": 0}

    step = 0
    traci.route.add("route0", ["gneE0", "gneE1", "gneE4"])
    traci.route.add("route1", ["gneE0", "gneE2"])
    traci.route.add("route2", ["-gneE2", "gneE3"])
    traci.route.add("route3", ["-gneE2", "-gneE0"])
    traci.route.add("route4", ["-gneE5", "-gneE1", "-gneE0"])
    traci.route.add("route5", ["-gneE4", "-gneE1", "-gneE0"])

    colora = (125, 255, 255, 255)
    colorb = (125, 255, 0, 255)
    colorc = (125, 0, 255, 255)
    colord = (225, 255, 255, 255)
    colore = (0, 255, 255, 255)
    colorf = (225, 0, 0, 255)
    while step < 500:
        #time.sleep(0.1)
        traci.simulationStep()
        step += 1
        if (step % (trafficlight_time[0] + trafficlight_time[1] + trafficlight_time[2] + trafficlight_time[3]) <
                trafficlight_time[0]):
            traci.trafficlight.setRedYellowGreenState('2', "grrrrrrrrrrrrrrrr")
        elif (step % (trafficlight_time[0] + trafficlight_time[1] + trafficlight_time[2] + trafficlight_time[3]) <
              trafficlight_time[0] + trafficlight_time[1]):
            traci.trafficlight.setRedYellowGreenState('2', "rggrrrrrrrrrrrrrr")
        elif (step % (trafficlight_time[0] + trafficlight_time[1] + trafficlight_time[2] + trafficlight_time[3]) <
              trafficlight_time[0] + trafficlight_time[1] + trafficlight_time[2]):
            traci.trafficlight.setRedYellowGreenState('2', "rrrrrrrrrrrrrggr")
        elif (step % (trafficlight_time[0] + trafficlight_time[1] + trafficlight_time[2] + trafficlight_time[3]) <
              trafficlight_time[0] + trafficlight_time[1] + trafficlight_time[2] + trafficlight_time[3]):
            traci.trafficlight.setRedYellowGreenState('2', "rrrrrrrrrrrrrrrg")
        if (step % (trafficlight_time[4] + trafficlight_time[5]) < trafficlight_time[4]):
            traci.trafficlight.setRedYellowGreenState('3', "GGGgrrrrGGGgrrrr")
        elif (step % (trafficlight_time[4] + trafficlight_time[5]) < trafficlight_time[4] + trafficlight_time[5]):
            traci.trafficlight.setRedYellowGreenState('3', "rrrrGGGgrrrrGGGg")
        if (step % 12 == 0):
            traci.vehicle.add("0" + str(step / 6), "route0")
            traci.vehicle.setColor("0" + str(step / 6), colora)
            traci.vehicle.changeLane("0" + str(step / 6), 0, 1)
            traci.vehicle.setLaneChangeMode("0" + str(step / 6), 0b001000000000)
            # 设置车辆禁止变道
            traci.vehicle.add("1" + str(step / 6), "route1")
            traci.vehicle.setColor("1" + str(step / 6), colorb)
            traci.vehicle.changeLane("1" + str(step / 6), 1, 1)
            # traci.vehicle.setLaneChangeMode("1" + str(step / 6), 0b001000000000)
            traci.vehicle.add("2" + str(step / 6), "route2")
            traci.vehicle.setColor("2" + str(step / 6), colorc)
            traci.vehicle.changeLane("2" + str(step / 6), 1, 1)
            traci.vehicle.setLaneChangeMode("2" + str(step / 6), 0b001000000000)
            traci.vehicle.add("3" + str(step / 6), "route3")
            traci.vehicle.setColor("3" + str(step / 6), colord)
            traci.vehicle.changeLane("3" + str(step / 6), 0, 1)
            traci.vehicle.setLaneChangeMode("3" + str(step / 6), 0b001000000000)
            traci.vehicle.add("4" + str(step / 6), "route4")
            traci.vehicle.setColor("4" + str(step / 6), colore)
            traci.vehicle.add("5" + str(step / 6), "route5")
            traci.vehicle.setColor("5" + str(step / 6), colorf)
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
    # print(value)
    return value
    # if(step == trafficlight_time[0] + trafficlight_time[1] + trafficlight_time[2] + trafficlight_time[3]):
    #   for i in all_Vehicle_Id:
    #      traci.vehicle.remove(i)
    #    step=0


def stepagent1(action, trafficlight_time,dictx):
    beforetime = dictx.get(str(trafficlight_time))
    # print(trafficlight_time)
    trafficlight_time1 = [i for i in trafficlight_time]
    if action == 0:
        if trafficlight_time1[0] < 100:
            trafficlight_time1[0] = trafficlight_time1[0] + 50
    if action == 1:
        if trafficlight_time1[1] < 100:
            trafficlight_time1[1] = trafficlight_time1[1] + 50
    if action == 2:
        if trafficlight_time1[2] < 100:
            trafficlight_time1[2] = trafficlight_time1[2] + 50
    if action == 3:
        if trafficlight_time1[3] < 100:
            trafficlight_time1[3] = trafficlight_time1[3] + 50
    if action == 4:
        if trafficlight_time1[0] > 50:
            trafficlight_time1[0] = trafficlight_time1[0] - 50
    if action == 5:
        if trafficlight_time1[1] > 50:
            trafficlight_time1[1] = trafficlight_time1[1] - 50
    if action == 6:
        if trafficlight_time1[2] > 50:
            trafficlight_time1[2] = trafficlight_time1[2] - 50
    if action == 7:
        if trafficlight_time1[3] > 50:
            trafficlight_time1[3] = trafficlight_time1[3] - 50
    if action == 8:
        a = 1
        return a, trafficlight_time1
    # print(trafficlight_time)
    aftertime = dictx.get(str(trafficlight_time1))
    # print(beforetime-aftertime)
    # print(trafficlight_time1,trafficlight_time)
    return beforetime - aftertime, trafficlight_time1

def stepagent2(action, trafficlight_time,dictx):
    beforetime = dictx.get(str(trafficlight_time))
    # print(trafficlight_time)
    trafficlight_time1 = [i for i in trafficlight_time]
    if action == 0:
        if trafficlight_time1[4] < 100:
            trafficlight_time1[4] = trafficlight_time1[4] + 50
    if action == 1:
        if trafficlight_time1[5] < 100:
            trafficlight_time1[5] = trafficlight_time1[5] + 50
    if action == 2:
        if trafficlight_time1[4] > 50:
            trafficlight_time1[4] = trafficlight_time1[4] - 50
    if action == 3:
        if trafficlight_time1[5] > 50:
            trafficlight_time1[5] = trafficlight_time1[5] - 50
    if action == 4:
        a = 1
        return a, trafficlight_time1
    # print(trafficlight_time)
    aftertime = dictx.get(str(trafficlight_time1))
    # print(beforetime-aftertime)
    # print(trafficlight_time1,trafficlight_time)
    return beforetime - aftertime, trafficlight_time1
def update():
    dictx = makeDic()
    for i in range(50):
        # 对每一个训练,随机选择一种状态
        observation = [100, 100, 100, 100, 100, 100]
        times = 0
        reward = 0
        # print(state)
        while True:
            list0 = []
            list1 = []
            list2 = []
            # 选择当前状态下的所有可能动作]
            for i in range(0, 9):
                reward_, newob = stepagent1(i, observation,dictx)
                max = 0
                for j in range(0, 5):
                    reward_1, newobx = stepagent2(i, newob, dictx)
                    if (max < reward_1):
                        max = reward_1
                list0.append(reward_+max)
            # RL.check_state_exist(observation,list)
            action = RL.choose_action(str(observation), list0)
            # print(action)
            for j in range(0, 5):
                reward_2, newobx = stepagent2(i, newob, dictx)
                if (max < reward_2):
                    actionx = j
                    max = reward_2
            reward, observation_ = stepagent1(action, observation,dictx)
            rewardx, observation_ = stepagent2(action, observation_, dictx)
            for i in range(0, 9):
                reward_, newob = stepagent1(i, observation_,dictx)
                for j in range(0, 5):
                    reward_0, newobx = stepagent2(i, newob, dictx)
                    if (max < reward_0):
                        actionx = j
                        max = reward_0
                list1.append(reward_+max)
            print("The reward is", reward)

            print(observation)
            RL.learn(str(observation), action, reward+max, str(observation_), list1)

            print(RL.q_table)
            observation = observation_
            times = times + 1
            if times > 40:
                break

            # print(observation_)
            # if reward>
    print('This is the best', observation)

def updateDQN():
    # observation = [random.randint(1, 4) * 50, random.randint(1, 4) * 50, random.randint(1, 4) * 50,
    #               random.randint(1, 4) * 50]

    # observation1 = [100, 100, 100, 100]
    # bestobservation = observation
    stepx = 0
    dictx = makeDic()
    for i in range(300):
        # 对每一个训练,随机选择一种状态
        observation = [100, 100, 100, 100, 100, 100]
        times = 0
        reward = 0
        # print(state)
        while True:
            action = RL.choose_action(observation)
            reward, observation_ = stepagent1(action, observation,dictx)
            print("The reward is", reward)
            max = 0
            newobxm=observation_
            for j in range(0, 5):
                reward_1, newobx = stepagent2(i, observation_, dictx)
                if (max < reward_1):
                    newobxm=newobx
                    max = reward_1
            RL.store_transition(list(observation), action, reward+max, newobx)
            if (stepx > 200) and (stepx % 5 == 0):
                RL.learn()
            observation = newobx
            times = times + 1
            if times > 40:
                break
            stepx += 1
            print(stepx)

            # print(observation_)
            # if reward>

    print('This is the best', observation)


dict_ = {"vehicle_x": 0}


def makeDic():
    if (os.path.exists('C:/Users/23368/Desktop/dic.json') != True):
        for i in range(1, 3):
            for j in range(1, 3):
                for k in range(1, 3):
                    for l in range(1, 3):
                        for m in range(1, 3):
                            for n in range(1, 3):
                                answer = Qlearnning_routefile(
                                    [0 + i * 50, 0 + j * 50, 0 + k * 50, 0 + l * 50, 0 + m * 50, 0 + n * 50])
                                dict_[
                                    str([0 + i * 50, 0 + j * 50, 0 + k * 50, 0 + l * 50, 0 + m * 50,
                                         0 + n * 50])] = answer
        jsonstr = json.dumps(dict_)
        filename = open('C:/Users/23368/Desktop/dic.json', 'w')  # dict转josn
        filename.write(jsonstr)
        return dict_
    else:
        filename = open('C:/Users/23368/Desktop/dic.json', 'r')
        dict = json.loads(filename.read())
        return dict


if __name__ == '__main__':
    #RL = QLearningTable(actions=list(range(9)))
    # trafficlight_time=[100,100,100,100]
    #makeDic()
    # print(makeDic())
    RL = DeepQNetwork(9, 6,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    updateDQN()
