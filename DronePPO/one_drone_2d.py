import argparse
import time
from pynput import keyboard

import gym
import sys
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
# from GateAndObsAviary import FlyThruGateAviary
# from gym_pybullet_drones.envs.single_agent_rl.FlyThruGateAviary import FlyThruGateAviary

sys.path.insert(0, '../envs/single_agent/')
sys.path.insert(0, '../wrappers/')
from Convert2DTo3DWrapper import Convert2DTo3DWrapper
from FlyThruGateVEL import FlyThruGateAviary

def run():

    # env = gym.make('flythrugate-aviary-v0')
    env = FlyThruGateAviary()
    env = Convert2DTo3DWrapper(env)
    check_env(env)
    print("[INFO] Observation space:", env.observation_space)
    print("[INFO] Observation space:", env.observation_space)

    model = PPO(MlpPolicy,
                    env,
                    verbose=2,
                    learning_rate=0.05,
                    n_steps = 5, 
                    gamma = 0.99,
                    ent_coef= 0.01
                    )
    # model.learn(total_timesteps=3000)
    # model.save("fly-through")
    model = PPO.load("fly-through")

    ####################################SHOW TRAINED POLICY####################################
    
    env = FlyThruGateAviary(gui=True)
    env = Convert2DTo3DWrapper(env)

    for i in range(20):    
        obs = env.reset()
        start = time.time()
        while True:
            action, _states = model.predict(obs)
            # action = np.array([-0.7, 0.5, 1])
            print("#####ACTION####", action)
            obs, reward, done, info = env.step(action)
            env.render()
            print(done)            
            # sync(i, start, env.TIMESTEP)
            if done:
                break
    obs = env.reset()        
    env.close()
    
if __name__ == "__main__":
    run()
