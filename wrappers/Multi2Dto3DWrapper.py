import gym
from gym import spaces
import numpy as np

class Convert2DTo3DWrapper(gym.Wrapper):
    def __init__(self, env, NUM_OF_DRONES):
        super(Convert2DTo3DWrapper, self).__init__(env)
        #super().__init__(env)
        
        # Define the new action space
        
        self.action_space = spaces.Dict({i: spaces.Box(low=-1*np.ones(3),
                                          high=np.ones(3),
                                          dtype=np.float32
                                          ) for i in range(NUM_OF_DRONES)})


    def step(self, action):
       action_3d = {}
       for i in range (len(action)):
        np.insert(action[i], 3, 0)
        next_state, reward, done, info = self.env.step(action_3d)

        return next_state, reward, done, info
    
    # def reset(self, **kwargs):
    #     # Reset the underlying environment
    #     return self.env.reset(**kwargs)
