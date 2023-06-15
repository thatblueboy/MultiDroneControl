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
from stable_baselines3 import PPO
from stable_baselines3 import A2C
from stable_baselines3.a2c import MlpPolicy
from stable_baselines3.common.env_checker import check_env
from GateAndObsAviary import FlyThruGateAviary
#from gym_pybullet_drones.envs.single_agent_rl.FlyThruGateAviary import FlyThruGateAviary

def run():

    env = gym.make('flythrugate-aviary-v0')
    print("[INFO] Observation space:", env.observation_space)
    print("[INFO] Observation space:", env.observation_space)

    model = A2C(MlpPolicy,
                    env,
                    verbose=1,
                    learning_rate=0.05,
                    n_steps = 10
                    )
    model.learn(total_timesteps=30000)
    model.save("fly-through")
    model = A2C.load("fly-through")
    ##################3
    env = FlyThruGateAviary(gui=True)
    obs = env.reset()
    start = time.time()
    for i in range(6000):
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        if i%env.SIM_FREQ == 0:
            env.render()
            print(done)
        sync(i, start, env.TIMESTEP)
        if done:
            obs = env.reset()
    env.close()
    
if __name__ == "__main__":
    run()
