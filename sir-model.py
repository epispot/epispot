"""
Plain SIR Model:
S (Susceptible) --> I (Infected) --> R (Removed)
N (population), R_0 (basic reproductive number), gamma (recovery rate)
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# hyperparameters
N = 1000000
R_0 = 2.5
gamma = 1 / 7.0
S, I, R = 999999, 1, 0


# return the derivative of the SIR system at input x
def deriv(x, t, N, R_0, gamma):
    s, i, r = x
    dS = -gamma * R_0 * s * i / N
    dI = gamma * R_0 * s * i / N - gamma * i
    dR = gamma * i

    return dS, dI, dR


# integration
t = np.linspace(0, 100, 300)
Y = S, I, R  # vector of inital conditions
integral = odeint(deriv, Y, t, args=(N, R_0, gamma))
S, I, R = integral.T


# plots
def plotsir(t, S, I, R):
    f, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.plot(t, S, 'b', linewidth=2, label='Susceptible')
    ax.plot(t, I, 'r', linewidth=2, label='Infected')
    ax.plot(t, R, '0.25', linewidth=2, label='Removed')

    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)

    ax.set_xlabel('Time (days)')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    for spine in ('top', 'right', 'bottom', 'left'): ax.spines[spine].set_visible(False)
    plt.show()


plotsir(t, S, I, R)
