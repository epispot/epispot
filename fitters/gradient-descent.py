def fitting(t_steps, f, y, k, mu, grad_step=1e-3, epochs=10, print_cost=False):

    """
    :param t_steps: array of times to evaluate f at and compare with y
    :param f: function to fit --> f(timestep, argument array (`k`)), return [outputs]
    :param y: real data --> y(timestep), return [outputs]
    :param k: arguments of f
    :param mu: learning rate (for gradient descent algorithm)
    :param grad_step: (=1e-3) step size when calculating gradients
    :param epochs: (=100) epochs to run for optimization
    :param print_cost: (=False) to print cost
    :return: optimal `k`
    """

    def cost(a, b):
        return np.sum(np.square(np.subtract(a, b)))

    print('Fitting data ...')
    print('This will take about %s iterations' % (epochs * len(t_steps) * len(k)))
    for e in range(epochs):
        
        print('Epoch %s completed' % (e))
        for time in t_steps:

            cost_1 = cost(f(time, k), y(time))  # plain cost
            grads = []  # gradient accumulation array

            for arg in range(0, len(k)):

                # revised cost
                k_delta = k
                k_delta[arg] += grad_step
                cost_2 = cost(f(time, k_delta), y(time))

                # gradient calculation
                grads.append((cost_2 - cost_1) / grad_step)
            for arg in range(0, len(k)):
                k[arg] -= mu * grads[arg]

    print('Data fit complete.')
    if print_cost:
        total_cost = 0.0
        for time in t_steps:
            total_cost += cost(f(time, k), y(time))

        print('Total Squared Error Cost Achieved: %s' % (total_cost))
    return k
