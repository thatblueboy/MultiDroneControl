# Implementation of Multi-agent control and obstacle avoidance using PPO

Starting off, we we worked with a single drone in an empty world environment followed by adding obstacles and then finally adding multiple drones. The reward system and the hyperparameters were changed accordingly and  have been mentioned in the respective sections. 

## Single Drone-Gate World with Obstacle:

The obstacle in this case is a single pillar. The center of the gate is at (0,-1) in the x-y plane and the drone starts ar (0,5) in the x-y plane. A pillar shaped obstacle has been placed at (0,2) the height being the same as that of the gate supports. 

<strong>Reward System: </strong> We have made use of a continuous reward system as follows. If $p_{drone}(t)$ is the $(x,y,z)$ position of the drone at timestep t and $p_{goal}$ is the position of the goal then the goal reward is:

$$R_{goal}(t) = -  (||p_{drone}(t) - p_{goal}||_2) ^{2}$$

Furthermore the reward is incremented when the drone gets too close to the obstacle. If $d_{min}$ is the minimum distance from the drone to the obstacle that is accepted and $d_{obs}(t)$ is the distance between the drone and the obstacle at timestep $t$ then:


$$ R_{obstacle}(t)=   \left\{
\begin{array}{ll}
     0 & d_{obs}(t) > d_{min} \\
    -5 & d_{obs}(t) \leqslant d_{min} \\
\end{array} 
\right.  $$

Another discrete reward system has been taken for the drone approaching the goal. If $d_{goal}(t)$ is the distance between the drone and the goal at timestep $t$ and $r_{min1}$, $d_{min2}$ and $r_{min3}$ are some radius values from the centre of the goal point such that $r_{min1} \leqslant r_{min2} \leqslant r_{min3}$, then:

$$ R_{approach}(t)=   \left\{
\begin{array}{ll}
     1000 & d_{goal}(t) \leqslant r_{min1} \\
     10 & d_{goal}(t) \leqslant r_{min2} \\
     5 & d_{goal}(t) \leqslant r_{min3}
\end{array} 
\right.  $$

We can write the equation for the agent's reward $R(t)$ by combining the above as follows:

$$R(t) \ = \ R_{goal}(t) \ \ + \ \ R_{obstacle}(t) \ \ + \ \ R_{approach}(t)$$