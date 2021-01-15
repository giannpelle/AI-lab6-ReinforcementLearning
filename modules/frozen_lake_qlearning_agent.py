#!/usr/bin/env python

from typing import Sequence, Tuple

import gym
import numpy as np
import random

import gym_wumpus
from gym_wumpus.envs import WumpusEnv

from gym import envs, error, make

class FrozenLakeQLearningAgent(object):
    """
    class descr
    """

    def __init__(self, env):
        self.env = env
        self.q_table = np.zeros([env.observation_space.n, env.action_space.n])

    def train(self, *, episodes: int, alpha=0.1, gamma=0.6) -> Tuple[np.ndarray, Sequence[int]]:
        rewards = []
        
        exploration_rate = 1.0
        max_exploration_rate = 1.0
        min_exploration_rate = 0.1
        exploration_decay_rate = 0.001

        for episode in range(episodes):
            obs = self.env.reset()
            done = False
            episode_reward = 0
            while not done:

                # select next action
                if exploration_rate > np.random.random():
                    # random action
                    action = self.env.action_space.sample()
                else:
                    # select best action
                    action = np.argmax(self.q_table[obs])
                # perform the action
                new_obs, reward, done, info = self.env.step(action)
                
                if done and new_obs == self.env.observation_space.n - 1:
                    reward = 10
                elif done:
                    reward = -10

                # update q_table
                self.q_table[obs, action] = (1 - alpha) * self.q_table[obs, action] + alpha * (reward + gamma * np.max(self.q_table[new_obs]))

                obs = new_obs

                episode_reward += reward
                
            exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)

            rewards.append(episode_reward)

        self.env.close()

        return self.q_table, rewards


    def run_episode(self) -> Tuple[int, Sequence[str]]:
        total_reward = 0
        frames = []

        obs = self.env.reset()
        done = False
        while not done:
            # save the frame corresponding to the current state
            frames.append(self.env.render('ansi'))

            # select best action
            action = np.argmax(self.q_table[obs])

            # perform the action
            obs, reward, done, info = self.env.step(action)

            total_reward += reward

        self.env.close()

        return total_reward, frames


