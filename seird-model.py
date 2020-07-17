"""
SEIRD Model
S (Susceptible) --> E (Exposed) --> I (Infected) --> R (Recovered) --> D (Dead)
 - N (population), R_0 (basic reproductive number), gamma (recovery rate)
 - delta (infection delay), rho (death delay), alpha (death rate)
 - alpha_opt (plain death rate -not accounting for hospital capacity), s (capacity constraint)
"""

# hyperparameters
N = 1000000
delta = 1 / 2.0
gamma = 1 / 4.0
rho = 1 / 4.0
S, E, I, R, D = 999999, 1, 0, 0, 0


# variable hyperparameters

def R_0(t):
    if t < 50:
        return 3.0
    elif t < 70:
        return 1.5
    else:
        return 3.0


def s(t):
    if t < 50:
        return 1
    else:
        return 1 / 2


def alpha_opt(t):
    if t < 50:
        return 0.1
    elif t < 70:
        return 0.05
    else:
        return 0.01


def alpha(t, I):
    return s(t) * I / N + alpha_opt(t)


# return the derivative of the SIR system at input x
def deriv(x, t, N, R_0, delta, gamma, rho, alpha):
    s, e, i, r, d = x
    ds = -gamma * R_0(t) * s * i / N
    de = gamma * R_0(t) * s * i / N - delta * e
    di = delta * e - (1 - alpha(t, i)) * gamma * i - alpha(t, i) * rho * i
    dr = (1 - alpha(t, i)) * gamma * i
    dd = alpha(t, i) * rho * i

    return ds, de, di, dr, dd


# integration
t = np.linspace(0, 100, 100)
Y = S, E, I, R, D  # vector of initial conditions
integral = odeint(deriv, Y, t, args=(N, R_0, delta, gamma, rho, alpha))
S, E, I, R, D = integral.T


# plots
def plotseird(t, S, E, I, R, D):
    f, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.plot(t, S, 'b', linewidth=2, label='Susceptible')
    ax.plot(t, E, 'y', linewidth=2, label='Exposed')
    ax.plot(t, I, 'r', linewidth=2, label='Infected')
    ax.plot(t, R, 'g', linewidth=2, label='Recovered')
    ax.plot(t, D, '0.25', linewidth=2, label='Dead')

    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)

    ax.set_xlabel('Time (days)')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    for spine in ('top', 'right', 'bottom', 'left'): ax.spines[spine].set_visible(False)
    plt.show()


plotseird(t, S, E, I, R, D)
