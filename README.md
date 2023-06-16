# README


## Directory Breakup

1. ```/dev_test``` is the directory for all testing and reference code files. All basic tests and general developments that weren't used in the end, are in this directory for future reference

2. ```/DronePPO``` is the directory for all PPO implementations for single and multiple agent environments

3. ```/envs``` is the directory for all the environments, it's further broken up into ```/single_agent``` and ```/multi_agent``` environment direcotries

4. ```/wrappers``` is the directory for all self implemented wrappers


## Saved Models

1. ```fly-through``` is the trained model for a single drone flying through gate environment

2. ```fly-through-obs1``` is the trained model for a single drone flying through a gate with a single obstacle 
---

## To Do
- [x] Complete single drone and obstacle training

- [x] import environments and wrappers from ```wrappers``` and ```envs ```

- [ ] Change save location of models to ```/models```

