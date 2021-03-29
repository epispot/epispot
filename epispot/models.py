"""
The `Model` classes help create a model out of various disease compartments.
For example, the basic SIR model would be a model consisting of the Susceptible, Infected, and Recovered
compartments. These classes also allow for differentiation and integration to evaluate the model's
predictions.
STRUCTURE:
- Model(object)
"""


class Model(object):
    """
    Helps create a model out of various disease compartments
    STRUCTURE:
        - __init__()
    """

    def __init__(self, init_pop, layers=None, layer_names=None, layer_map=None):
        """
        Initialize the `Model` class

        All optional parameters can be added through the `add_layer` method
        :param init_pop: initial population of the area in question
        :param layers: =[], every layer in Model (as a class, e.g [Susceptible(), Infected(), Recovered()]
        :param layer_names: =[], names of every previous layer in Model
                                 (e.g [None, 'Susceptible', 'Infected'])
                                allowed names are listed below:
                                - Susceptible
                                - Infected
                                - Recovered
                                - Exposed
                                - Removed
                                - Dead
                                - Critical
                                - Hospitalized
                                use `None` to indicate that no other layer precedes the first layer.
        :param layer_map: =[] next layers (as classes) for every layer in Model
                              (e.g. [Infected(), Recovered(), None]) Use `None` to indicate that no other
                              layer succeeds the last layer.
        """

        self.init_pop = init_pop
        self.layers = layers
        self.layer_names = layer_names
        self.layer_map = layer_map

    def get_deriv(self, time, system):
        """
        Return list of derivatives from each layer.
        Used by `integrate()` for evaluating model predictions.

        :param time: Time to take derivative at
        :param system: System of state values (S, I, R, etc.) --> e.g [973, 12, 15]
        :return: List of derivatives in the order that layers were added
        """

        derivatives = []
        for layer in range(len(self.layers)):
            derivatives.append(self.layers[layer].get_deriv(time, system))

        return derivatives

    def integrate(self, timesteps, starting_state=None):
        """
        Integrate the model from `get_deriv` to arrive at future predictions using Euler's Method

        :param timesteps: range of evenly-spaced times (from start of epidemic to prediction time)
                          The difference between each of the times is used as `delta` in Euler's Method.
                          The closer this difference is to zero, the more accurate these predictions
                          become.
        :param starting_state: starting state of the model--the system of values of each layer at time 0
                               e.g [973, 12, 15]
        :return: predictions in the form of `timesteps`, each timestep consisting of a list of derivatives
                 derivative order is the same as the order of the layers passed into Model
        """

        results = []
        delta = timesteps[1] - timesteps[0]

        if starting_state:
            system = starting_state

        else:
            system = [self.init_pop - 1, 1]
            for _ in range(0, len(self.layers) - 2):
                system.append(0)

        # test the `get_deriv` method for any errors and setup any commonly used variables
        for layer in range(len(self.layers)):
            self.layers[layer].test(self.layer_map, self.layer_names)

        for timestep in timesteps:
            derivatives = self.get_deriv(timestep, system)
            for state_no in range(0, len(system)):
                system[state_no] += derivatives[state_no] * delta
            results.append([system[n] for n in range(len(system))])

        return results

    def add_layer(self, layer, layer_name, layer_map):
        """
        Add a custom compartment to Model

        :param layer: the layer class
                      should be an instance of a class with the following structure:
                        - get_layer_index()
                            - return: layer index in `self.layers`
                        - test(time, system, next_layers, layer_names, layer_no)
                        (to test the `get_deriv` method: output optional)
                        usually used to save common operations as a class variable
                            - next_layers: a list of the classes of the following layers
                            - layer names: names of each layer in Model
                            - layer_no: index of current layer in `layer_names`
                            - raise: any errors or warnings
                        - get_deriv(time, system, next_layers, layer_names, layer_no)
                            - time: time to take derivative at
                            - system: system of state values (S, I, R, etc.) --> e.g [973, 12, 15]
                            - next_layers: a list of the classes of the following layers
                            - layer names: names of each layer in Model
                            - layer_no: index of current layer in `layer_names`
                            - return: derivative
        :param layer_name: =[], names of every layer in Model
                                 (e.g [None, 'Susceptible', 'Infected'])
                                allowed names are listed below:
                                    - Susceptible
                                    - Infected
                                    - Recovered
                                    - Exposed
                                    - Removed
                                    - Dead
                                    - Critical
                                    - Hospitalized
                                use `None` to indicate that no other layer precedes the first layer.
        :param layer_map: =[] next layers (as classes) for every layer in Model
                              (e.g. [Infected(), Recovered(), None]) Use `None` to indicate that no other
                              layer succeeds the last layer.
        """

        if self.layers is None:
            self.layers = [layer]
        else:
            self.layers.append(layer)

        if self.layer_names is None:
            self.layer_names = [layer_name]
        else:
            self.layer_names.append(layer_name)

        if self.layer_map is None:
            self.layer_map = [layer_map]
        else:
            self.layer_map.append(layer_map)
