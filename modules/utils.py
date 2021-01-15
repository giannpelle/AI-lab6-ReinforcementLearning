from statistics import mean
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def training_plot(rewards: Sequence[int], ax:plt.Axes=None):
    """Creates a plot showing the training history of the given list of rewards.
    Returns the axes in which the plot has been created.
    """
    rews = np.array(rewards).T
    # calculate the running average <https://stackoverflow.com/a/30141358>
    smoothed_rews = pd.Series(rews).rolling(max(1, int(len(rews) * .1))).mean()

    ax = ax if ax is not None else plt.axes()

    ax.plot(smoothed_rews)
    ax.plot(rews, color='grey', alpha=0.3)
    ax.set_xlabel('Episode')
    ax.set_ylabel('Total Reward')

    return ax
