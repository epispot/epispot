"""
This module contains all available fitting algorithms.
These operate separately from the `Model` class.
STRUCTURE:
    - grad_des
"""

from . import np


def grad_des(get_model_pred, real_data, model_params, mu, epochs, N, samples, delta=0.0001):
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
    :return: optimized `model_params`
    """

    # get real data
    file = real_data.readlines()
    layers_to_opt = [int(char) for char in file[0].split(',')]

    # quadratic cost

    def cost(pred, real):

        p_samp = []
        r_samp = []

        for sample in samples:
            p_samp.append(pred[sample][1] / N)
            r_samp.append(real[sample][1] / N)

        return np.sum((np.array(p_samp) - np.array(r_samp)) ** 2)

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

        # print(gradients)
        # print(model_params)
        model_params = model_params - mu * np.array(gradients)
        # print(model_params)
        # predictions = get_model_pred(model_params)
        # print(cost(predictions, data[1:]))

    return model_params
