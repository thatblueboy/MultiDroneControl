# README


## Directory Breakup

1. ```/dev_test``` is the directory for all testing and reference code files. All basic tests and general developments that weren't used in the end, are in this directory for future reference

2. ```/DronePPO``` is the directory for all PPO implementations for single and multiple agent environments

3. ```/envs``` is the directory for all the environments, it's further broken up into ```/single_agent``` and ```/multi_agent``` environment direcotries

4. ```/wrappers``` is the directory for all self implemented### Usage

Run ```twoDronesGamePynput.py``` to test ```TwoDroneAviary.py``` environment <br>
Simulation starts with drone 1 at (-1, -1) and drone 2 at (1,-1), episode ends in 60 seconds or when drones reach (1, 1) and (-1, 1) respectively. There are by default 100 episodes.<br>Action inputs are manual, 
use ```WASD``` to control Drone 1, and ```arrow keys``` to control Drone 2 <br>


## Saved Models

1. ```fly-through``` is the trained model for a single drone flying through gate environment

2. ```fly-through-obs1``` is the trained model for a single drone flying through a gate with a single obstacle 
---

## To Do
- [x] Complete single drone and obstacle training

- [x] import environments and wrappers from ```wrappers``` and ```envs ```

- [ ] Change save location of models to ```/models```

