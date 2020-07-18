def gradient_descent(t_steps, f, y, k, mu, grad_step=1e-3, epochs=100):

    """
    :param t_steps: array of times to evaluate f at and compare with y
    :param f: function to fit --> f(timestep, argument array (`k`))
    :param y: real data --> y(timestep)
    :param k: arguments of f
    :param mu: learning rate (for gradient descent algorithm)
    :param grad_step: (=1e-3) step size when calculating gradients
    :param epochs: (=100) epochs to run for optimization
    :return: optimal `k`
    """

    def cost(a, b):
        return (a - b)**2

    print('Fitting data ...')
    print('This will take about %s iterations' % (epochs * len(t_steps) * len(k)))
    for _ in range(epochs):
        for time in t_steps:
            for arg in range(0, len(k)):

                # plain cost
                cost_1 = cost(f(time, k), y(time))

                # revised cost
                k_delta = k
                k_delta[arg] += grad_step
                cost_2 = cost(f(time, k_delta), y(time))

                # gradient calculation
                grad = (cost_2 - cost_1) / grad_step
                k[arg] -= mu * grad

    print('Data fit complete.')
    return k
