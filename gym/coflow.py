from jpype import *
import os
from gym import Env, spaces
from algo.ddpg import DDPG
from algo.ddpg import OUNoise
import numpy as np
import json
import math, sys, time


class CoflowSimEnv(Env):
    def __init__(self, gym):
        self.coflowsim = gym
        self.NUM_COFLOW = self.coflowsim.MAX_COFLOW # 10
        self.UNIT_DIM = 4 # id, width/1000, sent_bytes, duration_time/1000
        self.STATE_DIM = self.NUM_COFLOW*self.UNIT_DIM
        self.ACTION_DIM = 9

        self.low_property = np.zeros((self.UNIT_DIM,))
        assert self.UNIT_DIM == 4, "UNIT_DIM != 4"
        self.high_property = np.array([526, 21170, 8501205*1048576, 0]) # B, ms
        
        self.observation_space = spaces.Box(0, 1, (self.STATE_DIM,))
        self.action_space = spaces.Box(0, 1, (self.ACTION_DIM,))

        self.MB = 1024*1024 # 1MB = ? B
        self.old_throughout = 0

    def step(self, action):
        # correction for action
        action = np.clip(action, 0.01, 100)

        res = self.coflowsim.toOneStep(action)
        # print("res", res)
        result = json.loads(str(res))
        obs = result["observation"]
        obs = self.__parseObservation(obs)
        done = result["done"]
        # obs = self.coflowsim.printStats()
        # obs = np.zeros(self.observation_space.shape)

        ### calculate the throughout
        completed = result["completed"]
        c_coflows = eval(completed.split(":")[-1])
        throughout = 0
        for coflow in c_coflows:
            ## id, width, total bytes(B), duration time(ms)
            throughout += (coflow[-2]/(coflow[-1]*1024)) # unit is Mbs
        ### calculate the reward
        reward = 0
        if self.old_throughout == 0:
            if throughout == 0:
                reward = 0
            else:
                reward = 100
        else:
            rate = throughout/self.old_throughout
            reward = np.clip(rate if rate <= 1 else rate*10, 0, 100)
        self.old_throughout = throughout
        # print("throughout: ", throughout, "reward: ", reward)
        
        return obs, reward, done, {}
    
    def __parseObservation(self, obs):
        arr = obs.split(":")[-1]
        arrs = sorted(eval(arr), key=lambda x: x[2], reverse=True) # sort according to sent bytes
        arrs = arrs[:self.NUM_COFLOW]
        state = []
        for a in arrs:
            ## id, width, already bytes(B), duration time(ms)
            # power = int(math.log(a[2], 10)) if a[2] != 0 else 0
            # b = (a[0], a[1]/1000, a[2]/(10**power), power, a[3]/1000)
            if a[3] > self.high_property[3]:
                self.high_property[3] = a[3]
            # print("parse: ", a, self.low_property, self.high_property)
            b = [(a[i]-self.low_property[i])/(self.high_property[i]-self.low_property[i]) for i in range(self.UNIT_DIM)]
            # print(b)
            state.extend(b)
        if len(arrs) < self.NUM_COFLOW:
            state.extend([0]*(self.NUM_COFLOW-len(arrs))*self.UNIT_DIM)
        return np.array(state)

    def getResult(self):
        return self.coflowsim.printStats()
    
    def reset(self):
        obs = self.coflowsim.reset()
        return self.__parseObservation(str(obs))
    
    def render(self):
        pass
    
    def close(self):
        pass
