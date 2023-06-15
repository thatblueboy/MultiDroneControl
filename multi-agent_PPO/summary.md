# Implementation of Multi-agent control and obstacle avoidance using PPO

The research paper that is being referenced is [this](https://ieeexplore.ieee.org/document/9658635). Starting off, we will be working with a single drone in an empty world environment followed by adding obstacles and then finally adding multiple drones. The reward system and the hyperparameters will be changed accordingly and mentioned in the respective sections. 
\
\
The packages that are being used are:

## Single Drone-Gate World:

The model was trained over 20,000 time steps, with policy updates occuring after every 50 time steps. The reward system is the same as the original FlyThruGateAviary problem.  

## Single Drone-Gate World with Obstacle:

The obstacle in this case is a single pillar. The center of the gate is at (0,-1) in the x-y plane and the drone starts ar (0,0) in the x-y plane. A pillar shaped obstacle has been placed at (0,-0.5) the height being the same as that of the gate supports. 

