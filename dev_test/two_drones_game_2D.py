import argparse
import time
from pynput import keyboard

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
from envs.multi_agent.TwoDronesAviary import TwoDronesAviary
from wrappers.Multi2Dto3DWrapper import Convert2DTo3DWrapper


EPISODES = 100
CONST_ACTION = {0: np.array([1, 0, 0, 1]), 1: np.array([0, 1, 0, 1])}

# Global variables for storing key states
key_states = {
    'w': False,
    'a': False,
    's': False,
    'd': False,
    'up': False,
    'down': False,
    'left': False,
    'right': False
}


# Function to handle key press events
def on_press(key):
    try:
        if key.char == 'w':
            key_states['w'] = True
        elif key.char == 'a':
            key_states['a'] = True
        elif key.char == 's':
            key_states['s'] = True
        elif key.char == 'd':
            key_states['d'] = True
    except AttributeError:
        if key == keyboard.Key.up:
            key_states['up'] = True
        elif key == keyboard.Key.down:
            key_states['down'] = True
        elif key == keyboard.Key.left:
            key_states['left'] = True
        elif key == keyboard.Key.right:
            key_states['right'] = True


# Function to handle key release events
def on_release(key):
    try:
        if key.char == 'w':
            key_states['w'] = False
        elif key.char == 'a':
            key_states['a'] = False
        elif key.char == 's':
            key_states['s'] = False
        elif key.char == 'd':
            key_states['d'] = False
    except AttributeError:
        if key == keyboard.Key.up:
            key_states['up'] = False
        elif key == keyboard.Key.down:
            key_states['down'] = False
        elif key == keyboard.Key.left:
            key_states['left'] = False
        elif key == keyboard.Key.right:
            key_states['right'] = False


def run():
    env = Convert2DTo3DWrapper(TwoDronesAviary(gui=True))
    print("[INFO] Action space:", env.action_space)
    print("[INFO] Observation space:", env.observation_space)
    env.observation_space.sample()

    # Initialize the keyboard listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    for episode in range(EPISODES):
        print("#######################", episode, "###############################")
        env.reset()

        while True:
            action = {0: np.array([0, 0, 0, 1]), 1: np.array([0, 0, 0, 1])}
            print("step")

            if key_states['w']:
                action[0][1] = 1
            elif key_states['a']:
                action[0][0] = -1
            elif key_states['s']:
                action[0][1] = -1
            elif key_states['d']:
                action[0][0] = 1

            if key_states['up']:
                action[1][1] = 1
            elif key_states['down']:
                action[1][1] = -1
            elif key_states['left']:
                action[1][0] = -1
            elif key_states['right']:
                action[1][0] = 1

            observation, reward, done, info = env.step(action)
            print("#####DONE#####", done)
            
            if done["__all__"]:
                break

    listener.stop()


if __name__ == "__main__":
    print("starting")
    run()
