import argparse
import time
import getch
import curses
import keyboard

import gym
import numpy as np
import ray
from gym_pybullet_drones.utils.Logger import Logger
from gym_pybullet_drones.utils.utils import str2bool, sync
from ray.rllib.agents import ppo
from ray.tune import register_env
from stable_baselines3 import A2C
from stable_baselines3.a2c import MlpPolicy
from stable_baselines3.common.env_checker import check_env
from TwoDroneAviary import TwoDroneAviary


EPISODES = 100
CONST_ACTION = {0:np.array([1, 0, 0, 1]), 1:np.array([0, 1, 0, 1])}

def run():
    # env = gym.make("two-drone-aviary-v0")
    env = TwoDroneAviary(gui=True)
    print("[INFO] Action space:", env.action_space)
    print("[INFO] Observation space:", env.observation_space)
    env.observation_space.sample()

    for episodes in range(EPISODES):
        print("#######################", episodes, "###############################")
        env.reset()
       

        while True:
            action = {0:np.array([0, 0, 0, 1]), 1:np.array([0, 0, 0, 1])}
            print("step")
           
            # Check if 'w' key is pressed
            if keyboard.is_pressed('w'):
                action[0][1] = 1
            # Check if 'a' key is pressed
            elif keyboard.is_pressed('a'):
                action[0][0] = -1 
            # Check if 's' key is pressed
            elif keyboard.is_pressed('s'):
                action[0][1] = -1
            # Check if 'd' key is pressed
            elif keyboard.is_pressed('d'):
                action[0][0] = 1

            # Check if up arrow key is pressed
            if keyboard.is_pressed(keyboard.KEY_UP):
                action[1][1] = 1
            # Check if down arrow key is pressed
            elif keyboard.is_pressed(keyboard.KEY_DOWN):
                action[1][1] = -1
            # Check if left arrow key is pressed
            elif keyboard.is_pressed(keyboard.KEY_LEFT):
                action[1][0] = -1
            # Check if right arrow key is pressed
            elif keyboard.is_pressed(keyboard.KEY_RIGHT):
                action[1][0] = 1

            observation, reward, done, info = env.step(action)
            print("#####DONE#####", done)
            # print(observation)
            if done["__all__"]:
                break
    
    
    # check_env(env,s
    #           warn=True,
    #           skip_render_check=True
    #           )
    
if __name__ == "__main__":
    print("starting")
    run()