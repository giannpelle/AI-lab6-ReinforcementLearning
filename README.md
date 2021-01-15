# AIMA 2020 Assignment 6 - Reinforcement Learning

This repository contains the group work submitted for the Assignment 6 of the [AIMA 2020](https://ole.unibz.it/course/view.php?id=6841) course from the Free University of Bozen-Bolzano.

## Problem description

The task of the assignment was to implement an q-learning agent to solve the "Hunt the Wumpus" game getting the best reward using the reinforcement learning technique. A brief description of the game is as follow: we are in a chess-like world environmentwhere each cell can either be empty or a pit, and there might be a wumpus in it. The agent can only move in empty cells (otherwise he would die either by falling into a pit or killed by the wumpus) and the movement is restricted by the orientation the agent has before performing the movement action. The world contains exactly one gold, which has to be grabbed by the agent if that is possible, and exactly one wumpus (monster) which can be killed if necessary in order to move into its location. Since the player we had to implement was an uninformed one,it couldn’t see the whole world configuration as needed, so it has to explore the world using its sensors and elaborating its percepts as it progresses in the game to get information about the environment. The agent perceives a BREEZE, if there is one or more pits in the 4 ortogonallyadjacent locations (but doesn’t know where exactly that pit is, and how many of them there are).It perceives a STENCH, if the wumpus is in one of the ortogonally adjacent locations, and it perceives BUMP if it bumps on the border of the world. The last percept the agent can perceive is GLITTER, which tells the agent that there is a gold in that location. The aim of the game is to get the best reward possible from trying to grab the gold and climbing out of the world.

<img src="/images/hunt_wumpus_rl.gif"  width="300">

## Technical description

For a complete description of the solution we developed, you can have a look at the documentation available [here](https://github.com/giannpelle/AI-lab6-ReinforcementLearning/tree/master/documentation/documentation.pdf).

## Solution outputs

If you want to see the results (outputs) we got from running the Reinforcement Learning agent on the 3 main game scenarios, have a look here:

* [safe world](https://github.com/giannpelle/AI-lab6-ReinforcementLearning/blob/master/wumpus_safe_sample.ipynb)
* [wumpus blocking world](https://github.com/giannpelle/AI-lab6-ReinforcementLearning/blob/master/wumpus_blocking_sample.ipynb)
* [no way world](https://github.com/giannpelle/AI-lab6-ReinforcementLearning/blob/master/wumpus_no_way_sample.ipynb)

## Running requirements

To run the code you have to create an *anaconda* environment with the configuration file found in *environment.yml* and then activate it to run the code.  
The required commands to make it work are the following:
1. `conda create env -f environment.yml`
2. `conda activate aima_gym`
3. `jupyter lab`

To run the sample code you just need to run the code cells in the file *frozen_lake.ipynb*, *frozen_lake_8x8.ipynb*, *wumpus_safe_sample.ipynb*, *wumpus_blocking_sample.ipynb*, *wumpus_no_way_sample.ipynb*.

