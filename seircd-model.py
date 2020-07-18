# hyperparameters

N = 39510000
delta = 1 / 5.0
gamma = 1 / 20.6
gamma_2 = 1 / 34.6
epsilon = 1 / 8.0
zeta = 0.544
rho = 1 / 5.0
S, E, I, R, C, D = 39509782, 0, 218, 0, 0, 0  # begin outbreak Mar. 20


# hyper-hyperparameters

times = [0, 30, 60, 90, 113]
R_0_measures = [1.245, 1.245, 1.67, 1.67, 2.49]
s_measures = [0.5, 0.5, 0.5, 0.5, 0.5]
alpha_opt_measures = [0.01, 0.01, 0.01, 0.01, 0.075]


# variable hyperparameters

def R_0(t):
    for i in range(0, len(times) - 1):
        if times[i] < t < times[i + 1]:
            return R_0_measures[i]
    return R_0_measures[-1]


def s(t):
    for i in range(0, len(times) - 1):
        if times[i] < t < times[i + 1]:
            return s_measures[i]
    return s_measures[-1]


def alpha_opt(t):
    for i in range(0, len(times) - 1):
        if times[i] < t < times[i + 1]:
            return alpha_opt_measures[i]
    return alpha_opt_measures[-1]


def alpha(t, I):
    return s(t) * I / N + alpha_opt(t)


# return the derivative of the SIR system at input x
def deriv(x, t, N, R_0, delta, gamma, gamma_2, rho, alpha, epsilon, zeta):
    s, e, i, r, c, d = x
    ds = -gamma * R_0(t) * s * i / N
    de = gamma * R_0(t) * s * i / N - delta * e
    di = delta * e - gamma * (1 - zeta) * i - epsilon * zeta * i
    dr = gamma * (1 - zeta) * i + gamma_2 * (1 - alpha(t, i)) * c
    dc = epsilon * zeta * i - gamma_2 * (1 - alpha(t, i)) * c - rho * alpha(t, i) * c
    dd = rho * alpha(t, i) * c

    return ds, de, di, dr, dc, dd


# integration
t = np.linspace(0, 287, 287)
Y = S, E, I, R, C, D  # vector of initial conditions
integral = odeint(deriv, Y, t, args=(N, R_0, delta, gamma, gamma_2, rho, alpha, epsilon, zeta))
S, E, I, R, C, D = integral.T


# plots
def plotseircd(t, markers, S, E, I, R, C, D):
    f, ax = plt.subplots(1, 1, figsize=(10, 4))
    plt.yscale('log')

    ax.plot(t, S, '#005fb3', linewidth=2, label='Susceptible')
    ax.plot(t, E, '#fbff00', linewidth=2, label='Exposed')
    ax.plot(t, I, '#ff0000', linewidth=2, label='Infected')
    ax.plot(t, R, '#0ac900', linewidth=2, label='Recovered')
    ax.plot(t, C, '#ff5900', linewidth=2, label='Critical')
    ax.plot(t, D, '#c400c1', linewidth=2, label='Dead')

    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)

    ax.set_xlabel('Time (days)')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)

    for marker in markers:
        ax.axvline(marker, linestyle='--', color='0.67')
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)

    plt.show()


plotseircd(t, [0, 113], S, E, I, R, C, D)
