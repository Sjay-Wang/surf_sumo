import traci
import time


# from RL_brain import QLearningTable


def Qlearnning_routefile(trafficlight_time):
    sumofile = "C:/Users/23368/Desktop/sumoTest/sumot7.sumocfg"
    traci.start(["sumo-gui", "-c", sumofile])
    isAdd = True
    step = 0
    all_Vehicle_Id0 = ()
    all_Vehicle_waitingtime = 0
    dict = {"vehicle_x": 0}
    time = trafficlight_time[0] + trafficlight_time[1] + trafficlight_time[2] + trafficlight_time[3]
    while step < time:
        time.sleep(0.1)
        traci.simulationStep()
        step += 1
        all_Vehicle_Id1 = traci.vehicle.getIDList()
        for i in all_Vehicle_Id1:
            if i not in dict:
                dict[i] = traci.vehicle.getAccumulatedWaitingTime(i)
            else:
                if traci.vehicle.getAccumulatedWaitingTime(i) > dict.get(i):
                    dict[i] = traci.vehicle.getAccumulatedWaitingTime(i)
        # print(all_Vehicle_Id1)

        # if(traci.vehicle)
    traci.close()
    value = 0
    for k, v in dict.items():
        value = v + value
    # print("The waitingtime of the vehicle", value)
    return value


# trafficlight_time[t1,t2,t3,t4]
def step(action, trafficlight_time):
    beforetime = Qlearnning_routefile(trafficlight_time)
    if action == 0:
        if trafficlight_time[0] < 60:
            trafficlight_time[0] + 5
    if action == 1:
        if trafficlight_time[1] < 60:
            trafficlight_time[1] + 5
    if action == 2:
        if trafficlight_time[2] < 60:
            trafficlight_time[2] + 5
    if action == 3:
        if trafficlight_time[3] < 60:
            trafficlight_time[3] + 5
    if action == 4:
        if trafficlight_time[0] > 0:
            trafficlight_time[0] - 5
    if action == 5:
        if trafficlight_time[1] > 0:
            trafficlight_time[1] - 5
    if action == 6:
        if trafficlight_time[2] > 0:
            trafficlight_time[2] - 5
    if action == 7:
        if trafficlight_time[3] > 0:
            trafficlight_time[3] - 5

    aftertime = Qlearnning_routefile(trafficlight_time)
    if (beforetime > aftertime):
        reward = beforetime - aftertime
        done = True
        s_ = 'terminal'
    if (beforetime < aftertime):
        reward = beforetime - aftertime
        done = False
        s_ = 'terminal'
    if (beforetime == aftertime):
        reward = 0
        done = False
    return s_, reward, done


def update():
    for episode in range(20):
        observation = reset()
        while True:
            action = RL.choose_action(str(observation))
            observation_, reward, done = step(action)
            RL.learn(str(observation), action, reward, str(observation_))
            observation = observation_
            if done:
                break
    print('It’s over')


def reset():
    trafficlight_time = [20, 20, 20, 20]
    initime = Qlearnning_routefile(trafficlight_time)


if __name__ == '__main__':
    # RL = QLearningTable(actions=list(range(env.n_actions)))
    Qlearnning_routefile()


