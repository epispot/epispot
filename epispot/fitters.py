"""
This module contains all available fitting algorithms.
These operate separately from the `Model` class.
STRUCTURE:
- grad_des
"""

from . import np


def grad_des(get_model_pred, real_data, model_params, mu, epochs, N, samples, delta=0.0001, verbose=False):
    """
    The gradient descent fitter. This is not stochastic.
    For long timespans, this may take a long time to converge.

    :param get_model_pred: function in the form:
                                param: parameters, parameters for model
                                return: model predictions (use the integrate() method)
    :param real_data: .csv file in the form:
                        HEADER: ...layer #s
                        CONTENTS: ...people in layers
    :param model_params: list of model parameters
    :param mu: the learning rate (adjust so that loss decreases after every epoch)
    :param epochs: number of training sessions to run
                   (more epochs = more accuracy + more time running)
    :param N: the total population
    :param samples: array of timestamps to use for training
    :param delta: =0.0001, use small values for more precision--increase if gradients are 0
    :param verbose: =False, use to debug and get gradient information
    :return: optimized `model_params`
    """

    # get real data
    file = real_data.readlines()
    # layers_to_opt = [int(char) for char in file[0].split(',')] - for specific layer optimizations

    # quadratic cost

    def cost(pred, real):

        p_samp = []
        r_samp = []

        for sample in samples:
            p_samp.append(pred[sample][0] / N)
            r_samp.append(real[sample][0] / N)

        if verbose:  # pragma: no cover
            print('predicted, data: ')
            print(p_samp)
            print(r_samp)
            print('\n')

        return np.sum(np.abs(np.array(p_samp) - np.array(r_samp)))

    data = [file[l].split(',') for l in range(1, len(file))]
    for line in range(len(data)):
        for char in range(len(data[line])):
            data[line][char] = float(data[line][char])
    for char in range(len(data[0])):
        data[0][char] = int(data[0][char])

    # training iterations
    for epoch in range(epochs):

        predictions = get_model_pred(model_params)
        base_cost = cost(predictions, data[1:])
        print('Epoch %s: Loss at %s' % (epoch, base_cost))

        gradients = []

        # parameter gradients
        for param in range(len(model_params)):

            model_params[param] += delta
            pred = get_model_pred(model_params)

            gradients.append((cost(pred, data[1:]) - base_cost) / delta)

            model_params[param] -= delta

        if verbose:  # pragma: no cover
            print('Gradients: ')
            print(gradients)
            print('\n')

        model_params = model_params - mu * np.array(gradients)
    return model_params


def tree_search(get_model_pred, real_data, model_params, param_ranges, epochs, N, samples, verbose=False):
    """
    Note: This is an experimental fitter
    """

    # get real data
    file = real_data.readlines()
    # layers_to_opt = [int(char) for char in file[0].split(',')] - use for specific layer optimizations

    # quadratic cost

    def cost(pred, real):

        p_samp = []
        r_samp = []

        for sample in samples:
            p_samp.append(pred[sample][0] / N)
            r_samp.append(real[sample][0] / N)

        return np.sum(np.abs(np.array(p_samp) - np.array(r_samp)))

    data = [file[l].split(',') for l in range(1, len(file))]
    for line in range(len(data)):
        for char in range(len(data[line])):
            data[line][char] = float(data[line][char])
    for char in range(len(data[0])):
        data[0][char] = int(data[0][char])

    for epoch in range(epochs):

        predictions = get_model_pred(model_params)
        base_cost = cost(predictions, data[1:])
        print('Epoch %s: Loss at %s' % (epoch, base_cost))

        for param in range(len(model_params)):

            cost_per_value = []

            for value in param_ranges[param]:

                model_params[param] = value
                new_predictions = get_model_pred(model_params)
                new_cost = cost(new_predictions, data[1:])
                cost_per_value.append((value, new_cost))

            best_pair = (0, 1e8)
            for pair in cost_per_value:
                if pair[1] < best_pair[1]:
                    best_pair = pair

            if verbose:  # pragma: no cover
                print(cost_per_value)

            model_params[param] = best_pair[0]

    return model_params
