import math

import numpy as np
import pybullet as p
from gym_pybullet_drones.envs.multi_agent_rl.BaseMultiagentAviary import \
    BaseMultiagentAviary
from gym_pybullet_drones.envs.single_agent_rl.BaseSingleAgentAviary import (
    ActionType, ObservationType)
from gym_pybullet_drones.utils.enums import DroneModel, Physics


class ThreeDronesAviary(BaseMultiagentAviary):
    """ 
    to do
    """

    ################################################################################

    def __init__(self,
                 drone_model: DroneModel=DroneModel.CF2X,
                 num_drones: int=3,
                 neighbourhood_radius: float=np.inf,
                 initial_xyzs=np.array([[-1, -1, 0.5], [1, -1, 0.5], [0, 0, 0.5]]),
                 initial_rpys=np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
                 obstaclePositions = np.array([[0.5, 0.5, 0.5], [1, 0, 0.5], [0, 1, 0.5], [2, 2, 0.5]]),
                 physics: Physics=Physics.PYB,
                 freq: int=240,
                 aggregate_phy_steps: int=1,
                 gui=False,
                 record=False, 
                 obs: ObservationType=ObservationType.KIN,
                 act: ActionType=ActionType.VEL):
        
        """Initialization of a multi-agent RL environment.

        Using the generic multi-agent RL superclass.

        Parameters
        ----------
        drone_model : DroneModel, optional
            The desired drone type (detailed in an .urdf file in folder `assets`).
        num_drones : int, optional
            The desired number of drones in the aviary.
        neighbourhood_radius : float, optional
            Radius used to compute the drones' adjacency matrix, in meters.
        initial_xyzs: ndarray | None, optional
            (NUM_DRONES, 3)-shaped array containing the initial XYZ position of the drones.
        initial_rpys: ndarray | None, optional
            (NUM_DRONES, 3)-shaped array containing the initial orientations of the drones (in radians).
        physics : Physics, optional
            The desired implementation of PyBullet physics/custom dynamics.
        freq : int, optional
            The frequency (Hz) at which the physics engine steps.
        aggregate_phy_steps : int, optional
            The number of physics steps within one call to `BaseAviary.step()`.
        gui : bool, optional
            Whether to use PyBullet's GUI.
        record : bool, optional
            Whether to save a video of the simulation in folder `files/videos/`.
        obs : ObservationType, optional
            The type of observation space (kinematic information or vision)
        act : ActionType, optional
            The type of action space (1 or 3D; RPMS, thurst and torques, or waypoint with PID control)

        """
        self.obstacles = []
        self.obstaclePositions = obstaclePositions
        super().__init__(drone_model=drone_model,
                         num_drones=num_drones,
                         neighbourhood_radius=neighbourhood_radius,
                         initial_xyzs=initial_xyzs,
                         initial_rpys=initial_rpys,
                         physics=physics,
                         freq=freq,
                         aggregate_phy_steps=aggregate_phy_steps,
                         gui=gui,
                         record=record, 
                         obs=obs,
                         act=act
                         )
        self.EPISODE_LEN_SEC = 60 #override episode time limit
        

    ################################################################################
    
    def _computeReward(self):
        """Computes the current reward value(s).

        Returns
        -------
        dict[int, float]
            The reward value for each drone.

        """
        rewards = {0:0, 1:0}
        states = np.array([self._getDroneStateVector(i) for i in range(self.NUM_DRONES)])
        pos1 = states[0, 0:3]
        pos2 = states[1, 0:3]
        pos3 = states[2, 0:3]
        
        if (np.linalg.norm(pos1-pos2)<0.2 or np.linalg.norm(pos3-pos2)<0.2 or np.linalg.norm(pos1-pos3)<0.2):

            if np.linalg.norm(pos1-pos2)<0.2: # if collision/too close
                rewards[0] = rewards[1] = -100

            if np.linalg.norm(pos3-pos2)<0.2: # if collision/too close
                rewards[2] = rewards[1] = -100

            if np.linalg.norm(pos1-pos3)<0.2: # if collision/too close
                rewards[0] = rewards[2] = -100
            return rewards
        
        if np.linalg.norm(pos1-np.array([1, 1, 0.5]))<0.2: # award drone 1 if it reaches goal 1
            rewards[0] = 100

        if np.linalg.norm(pos2-np.array([-1, 1, 0.5]))<0.2: # award drone 2 if it reaches goal 2
            rewards[1] = 100

        if np.linalg.norm(pos2-np.array([-1, 1, 0.5]))<0.2: # award drone 2 if it reaches goal 2
            rewards[1] = 100
        
        return rewards
    
    ################################################################################
    
    def _computeDone(self):
        """Computes the current done value(s).

        Returns
        -------
        dict[int | "__all__", bool]
            Dictionary with the done value of each drone and 
            one additional boolean value for key "__all__".

        """
        print("#####EPISODE LENGTH", self.EPISODE_LEN_SEC , "#####")
        done = {0:False, '__all__' :False, 1:False}
        states = np.array([self._getDroneStateVector(i) for i in range(self.NUM_DRONES)])
        pos1 = states[0, 0:3]
        pos2 = states[1, 0:3]
        
        if self.step_counter/self.SIM_FREQ > self.EPISODE_LEN_SEC:
            bool_val = True if self.step_counter/self.SIM_FREQ > self.EPISODE_LEN_SEC else False
            done = {i: bool_val for i in range(self.NUM_DRONES)}
            done["__all__"] = True if True in done.values() else False
            return done
        
        if np.linalg.norm(pos1-np.array([1, 1, 0.5]))<0.2: 
            done[0] = True

        if np.linalg.norm(pos2-np.array([-1, 1, 0.5]))<0.2:
            done[1] = True

        if done[0] == True and done[1] == True:
            done["__all__"] = True

        return done
     
    ################################################################################
    
    def _computeInfo(self):
        """Computes the current info dict(s).

        Unused.

        Returns
        -------
        dict[int, dict[]]
            Dictionary of empty dictionaries.

        """
        return {i: {} for i in range(self.NUM_DRONES)}

    ################################################################################

    def _clipAndNormalizeState(self,
                               state
                               ):
        """Normalizes a drone's state to the [-1,1] range.

        Parameters
        ----------
        state : ndarray
            (20,)-shaped array of floats containing the non-normalized state of a single drone.

        Returns
        -------
        ndarray
            (20,)-shaped array of floats containing the normalized state of a single drone.

        """
        MAX_LIN_VEL_XY = 3 
        MAX_LIN_VEL_Z = 1

        MAX_XY = MAX_LIN_VEL_XY*self.EPISODE_LEN_SEC
        MAX_Z = MAX_LIN_VEL_Z*self.EPISODE_LEN_SEC

        MAX_PITCH_ROLL = np.pi # Full range

        clipped_pos_xy = np.clip(state[0:2], -MAX_XY, MAX_XY)
        clipped_pos_z = np.clip(state[2], 0, MAX_Z)
        clipped_rp = np.clip(state[7:9], -MAX_PITCH_ROLL, MAX_PITCH_ROLL)
        clipped_vel_xy = np.clip(state[10:12], -MAX_LIN_VEL_XY, MAX_LIN_VEL_XY)
        clipped_vel_z = np.clip(state[12], -MAX_LIN_VEL_Z, MAX_LIN_VEL_Z)

        if self.GUI:
            self._clipAndNormalizeStateWarning(state,
                                               clipped_pos_xy,
                                               clipped_pos_z,
                                               clipped_rp,
                                               clipped_vel_xy,
                                               clipped_vel_z
                                               )

        normalized_pos_xy = clipped_pos_xy / MAX_XY
        normalized_pos_z = clipped_pos_z / MAX_Z
        normalized_rp = clipped_rp / MAX_PITCH_ROLL
        normalized_y = state[9] / np.pi # No reason to clip
        normalized_vel_xy = clipped_vel_xy / MAX_LIN_VEL_XY
        normalized_vel_z = clipped_vel_z / MAX_LIN_VEL_XY
        normalized_ang_vel = state[13:16]/np.linalg.norm(state[13:16]) if np.linalg.norm(state[13:16]) != 0 else state[13:16]

        norm_and_clipped = np.hstack([normalized_pos_xy,
                                      normalized_pos_z,
                                      state[3:7],
                                      normalized_rp,
                                      normalized_y,
                                      normalized_vel_xy,
                                      normalized_vel_z,
                                      normalized_ang_vel,
                                      state[16:20]
                                      ]).reshape(20,)

        return norm_and_clipped
    
    ################################################################################
    
    def _clipAndNormalizeStateWarning(self,
                                      state,
                                      clipped_pos_xy,
                                      clipped_pos_z,
                                      clipped_rp,
                                      clipped_vel_xy,
                                      clipped_vel_z,
                                      ):
        """Debugging printouts associated to `_clipAndNormalizeState`.

        Print a warning if values in a state vector is out of the clipping range.
        
        """
        if not(clipped_pos_xy == np.array(state[0:2])).all():
            print("[WARNING] it", self.step_counter, "in TwoDroneAviary._clipAndNormalizeState(), clipped xy position [{:.2f} {:.2f}]".format(state[0], state[1]))
        if not(clipped_pos_z == np.array(state[2])).all():
            print("[WARNING] it", self.step_counter, "in TwoDroneAviary._clipAndNormalizeState(), clipped z position [{:.2f}]".format(state[2]))
        if not(clipped_rp == np.array(state[7:9])).all():
            print("[WARNING] it", self.step_counter, "in TwoDroneAviary._clipAndNormalizeState(), clipped roll/pitch [{:.2f} {:.2f}]".format(state[7], state[8]))
        if not(clipped_vel_xy == np.array(state[10:12])).all():
            print("[WARNING] it", self.step_counter, "in TwoDroneAviary._clipAndNormalizeState(), clipped xy velocity [{:.2f} {:.2f}]".format(state[10], state[11]))
        if not(clipped_vel_z == np.array(state[12])).all():
            print("[WARNING] it", self.step_counter, "in TwoDroneAviary._clipAndNormalizeState(), clipped z velocity [{:.2f}]".format(state[12]))

    ################################################################################

    def _addObstacles(self):
            """Add obstacles to the environment.

            Only if the observation is of type RGB, 4 landmarks are added.
            Overrides BaseMUltiAgentAviary's method.

            """
            if self.OBSTACLES:
                for obstaclePos in self.obstaclePositions:
                    currObstacle = p.loadURDF('sphere_small.urdf', obstaclePos, globalScaling=2)
                    p.changeDynamics(currObstacle, -1, mass=0)
                    self.obstacles.append(currObstacle)