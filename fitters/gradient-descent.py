def fitting(t_steps, f, y, k, mu, grad_step=1e-3, epochs=10, print_cost=False):
    """
    :param t_steps: array of times to evaluate f at and compare with y
    :param f: function to fit --> f(argument array (`k`)), return func(timestep) --> return pred
    :param y: real data --> y(timestep), return [outputs]
    :param k: arguments of f
    :param mu: learning rate (for gradient descent algorithm)
    :param grad_step: (=1e-3) step size when calculating gradients
    :param epochs: (=100) epochs to run for optimization
    :param print_cost: (=False) to print cost
    :return: optimal `k`
    """

    def cost_function(a, b):
        return np.sum(np.square(np.subtract(a, b)))

    def cost(param):
        total_cost = 0.0
        to_fit = f(param)

        for time in t_steps:
            total_cost += cost_function(to_fit(time), y(time))

        return total_cost

    print('Fitting data ...')
    print('This will take about %s iterations \n\n' % (epochs * len(t_steps) * len(k)))
    for e in range(epochs):
        cost_1 = cost(k)
        if print_cost:
            print('Cost @ %s' % cost_1)

        grads = []  # gradient accumulation array

        for arg in range(0, len(k)):
            # revised cost
            k_delta = k
            k_delta[arg] += grad_step
            cost_2 = cost(k_delta)

            # gradient calculation
            grads.append((cost_2 - cost_1) / grad_step)
        for arg in range(0, len(k)):
            k[arg] -= mu * grads[arg]

        print('Epoch %s completed \n' % (e + 1))

    print('\nData fit complete.')
    if print_cost:
        print('Final cost: %s' % (cost(k)))
    return k
