import gym
from gym import spaces
import numpy as np

class Convert2DTo3DWrapper(gym.Wrapper):
    def __init__(self, env):
        super(Convert2DTo3DWrapper, self).__init__(env)
        #super().__init__(env)
        
        # Define the new action space
        self.action_space = spaces.Box(
            low=np.array([-1, -1, -1]),  # Lower bounds for x and y
            high=np.array([1, 1, -1]),    # Upper bounds for x and y
            dtype=np.float32
        )
        
    def step(self, action):
        print("###ACTION###", action)
        # Convert 2D action to 3D action
        action_3d = np.array([action[0], action[1], 0, action[2]])  # Set constant z value
        print("###ACTION_3D###", action_3d)
        # Perform the action in the underlying environment
        next_state, reward, done, info = self.env.step(action_3d)
        
        return next_state, reward, done, info
    
    def reset(self, **kwargs):
        # Reset the underlying environment
        return self.env.reset(**kwargs)
