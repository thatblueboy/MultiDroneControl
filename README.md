# README

### Usage

Run ```twoDronesGamePynput.py``` to test ```TwoDroneAviary.py``` environment <br>
Simulation starts with drone 1 at (-1, -1) and drone 2 at (1,-1), episode ends in 60 seconds or when drones reach (1, 1) and (-1, 1) respectively. There are by default 100 episodes.<br>Action inputs are manual, 
use ```WASD``` to control Drone 1, and ```arrow keys``` to control Drone 2 <br>

---

### Notes

- TwoDronesAvairy.py is supposed to be in env folder, but had import issues to no folders used
- Keyboard library requires root priveleges, and being in conda env, cant sudo install, so re wrote ```twoDronesGame.py``` code using pynput

---

### To Do

- [ ] parse two drone environment to RL libraries to test
- [ ] Make modular three drone aviary with one place to adjust number of drones, spawn points, etc.
- [ ] Add obstacles, and train again
- [ ] Make noise wrapper
