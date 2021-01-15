#!/usr/bin/env python

from typing import Sequence, Tuple

import gym
import numpy as np
import random

import gym_wumpus
from gym_wumpus.envs import WumpusEnv

from gym import envs, error, make

from modules.linear_space import SmartCoordinate, SmartVector
from modules.hunt_wumpus_state_custom import HuntWumpusStateCustom

class HuntWumpusCustomQLearningAgent(object):
    """
    defines a Q-Learning agent able to solve any Hunt the Wumpus game
    it needs an extensive training to be sure it solves it
    lower training would still works but sometimes they can fail
    """

    def __init__(self, env):
        self.env = env
        self.q_table = np.zeros([HuntWumpusStateCustom.get_state_space_size(), env.action_space.n])

    def train(self, *, episodes: int, alpha=0.2, gamma=0.7) -> Tuple[np.ndarray, Sequence[int]]:
        
        rewards = []
        hunt_wumpus_state = None

        for episode in range(episodes):
            
            if episode % 10_000 == 0:
                print(f"Running episode: {episode}")
                
            obs = self.env.reset()
            hunt_wumpus_state = HuntWumpusStateCustom()
            hunt_wumpus_state_index = hunt_wumpus_state.get_index()

            action = None
            done = False
            episode_reward = 0
            
            while not done:
                
                # select next action
                # in the first 3/4 of the training we make a deep exploring 
                # (70% of the time we go with a random action)
                # in the last 1/4 of the training we start exploiting what we already learned
                if episode < episodes * 3/4:
                    if np.random.random() > 0.3:
                        # random action
                        action = random.choice(self.env.actions)
                    else:
                        # select best action
                        action_index = np.argmax(self.q_table[hunt_wumpus_state_index])
                        action = self.env.actions[action_index]
                else:
                    if np.random.random() > 0.85:
                        # random action
                        action = random.choice(self.env.actions)
                    else:
                        # select best action
                        action_index = np.argmax(self.q_table[hunt_wumpus_state_index])
                        action = self.env.actions[action_index]
                    
                # perform the action
                new_obs, reward, done, info = self.env.step(action)
                
                old_percepts = self.env.space_to_percept(obs)
                new_percepts = self.env.space_to_percept(new_obs)
                
                if action.value == 0 and new_percepts.bump:
                    reward = -10
                if action.value == 0 and not new_percepts.bump:
                    hunt_wumpus_state.agent_location = hunt_wumpus_state.agent_location + hunt_wumpus_state.agent_orientation
                elif action.value == 1:
                    hunt_wumpus_state.agent_orientation = hunt_wumpus_state.agent_orientation.get_perpendicular_vector_clockwise()
                elif action.value == 2:
                    hunt_wumpus_state.agent_orientation = -hunt_wumpus_state.agent_orientation.get_perpendicular_vector_clockwise()
                elif action.value == 3:
                    hunt_wumpus_state.is_arrow_available = False
                    if new_percepts.scream:
                        hunt_wumpus_state.is_wumpus_alive = False
                elif action.value == 4 and old_percepts.glitter:
                    hunt_wumpus_state.has_agent_grabbed_gold = True
                elif action.value == 5 and hunt_wumpus_state.agent_location == SmartCoordinate(0, 0):
                    hunt_wumpus_state.has_agent_climbed_out = True
                    
                hunt_wumpus_state.is_agent_perceiving_scream = new_percepts.scream
                
                new_hunt_wumpus_state_index = hunt_wumpus_state.get_index()
                
                # update q_table
                self.q_table[hunt_wumpus_state_index, action.value] = (1 - alpha) * self.q_table[hunt_wumpus_state_index, action.value] + alpha * (reward + gamma * np.max(self.q_table[new_hunt_wumpus_state_index]))

                obs = new_obs
                hunt_wumpus_state_index = new_hunt_wumpus_state_index
                
                episode_reward += reward

            rewards.append(episode_reward)

        self.env.close()

        return self.q_table, rewards

    def run_episode(self) -> Tuple[int, Sequence[str]]:
        total_reward = 0
        frames = []

        obs = self.env.reset()

        hunt_wumpus_state = HuntWumpusStateCustom()
        hunt_wumpus_state_index = hunt_wumpus_state.get_index()
        
        done = False
        while not done:
            # save the frame corresponding to the current state
            frames.append(self.env.render('ansi'))

            # select best action
            action_index = np.argmax(self.q_table[hunt_wumpus_state_index])
            action = self.env.actions[action_index]
                
            # perform the action
            new_obs, reward, done, info = self.env.step(action)
                
            old_percepts = self.env.space_to_percept(obs)
            new_percepts = self.env.space_to_percept(new_obs)
                
            if action.value == 0 and not new_percepts.bump:
                hunt_wumpus_state.agent_location = hunt_wumpus_state.agent_location + hunt_wumpus_state.agent_orientation
            elif action.value == 1:
                hunt_wumpus_state.agent_orientation = hunt_wumpus_state.agent_orientation.get_perpendicular_vector_clockwise()
            elif action.value == 2:
                hunt_wumpus_state.agent_orientation = -hunt_wumpus_state.agent_orientation.get_perpendicular_vector_clockwise()
            elif action.value == 3:
                hunt_wumpus_state.is_arrow_available = False
                if new_percepts.scream:
                    hunt_wumpus_state.is_wumpus_alive = False
            elif action.value == 4 and old_percepts.glitter:
                hunt_wumpus_state.has_agent_grabbed_gold = True
            
            hunt_wumpus_state.is_agent_perceiving_scream = new_percepts.scream
            
            hunt_wumpus_state_index = hunt_wumpus_state.get_index()
            obs = new_obs

            total_reward += reward

        self.env.close()

        return total_reward, frames
