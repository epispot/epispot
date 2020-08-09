"""
The `compartments` module contains pre-built disease compartments for basic modelling and allows for
custom user-defined compartments. This module consists of several classes, each representing a specific
compartment.
STRUCTURE:
    - Susceptible(object)
    - Infected(object)
    - Recovered(object)
    - Exposed(object)
"""

from . import warnings


class Susceptible(object):
    """
    The Susceptible class is the 'S' of the 'SIR' Model.
    This is the portion of individuals who have not yet been exposed to the disease.
    This class can be used as a beginning state.
    Recovered (?) --> Susceptible --> Infected
    STRUCTURE:
        - __init__
        - get_layer_index
        - test
        - get_deriv
    """

    def __init__(self, layer_index, R_0, gamma, N, p_resusceptibility=None, s_rate=None):
        """
        Initialize the Susceptible class

        :param layer_index: index of layer in `layers`
        :param R_0: the basic reproductive number
                    this is the average number of susceptibles infected by one infected
                    implemented as a function R_0(t):
                        - t: time
                        - return: R_0 value
        :param gamma: the infectious period
                      1 / average duration of infectious period
                      implemented as a function gamma(t):
                        - t: time
                        - return: infectious period
        :param N: the total population
                  implemented as a function N(t):
                        - t: time
                        - return: total population
        :param p_resusceptibility: =None, probability of re-susceptibility (0 <= x <= 1)
                                   only applicable if individuals can become susceptible again
                                   implemented as a function p_resusceptibility(t):
                                        - t: time
                                        - return: probability of re-susceptibility
        :param s_rate: =None, 1 / average time to become susceptible again
                       only applicable if individuals can become susceptible again
                       implemented as a function s_rate(t):
                        - t: time
                        - return: susceptiblity rate
        """

        self.layer_index = layer_index
        self.R_0 = R_0
        self.gamma = gamma
        self.N = N

        self.p_resusceptibility = p_resusceptibility
        self.s_rate = s_rate

        self.infected_category_indices = []
        self.prev_layer_indices = []
        self.first_layer = True

    def get_layer_index(self):
        return self.layer_index

    def test(self, layer_map, layer_names):
        """
        Test of the `get_deriv` method
        Used to setup commonly used variables and raise common errors

        :param layer_map: next layers (as classes) for every layer in Model
        :param layer_names: layer names in system
        :return: derivative
        """

        # setup
        for i in range(0, len(layer_names)):
            if layer_names[i] == 'Infected':
                self.infected_category_indices.append(i)

        for layer_no in range(len(layer_map)):
            for next_layer in layer_map[layer_no]:
                if next_layer.get_layer_index() == self.layer_index:
                    self.first_layer = False
                    self.prev_layer_indices.append(layer_no)

        # tests
        if not self.first_layer and not self.s_rate:
            warnings.warn('The Susceptible layer at %s is not the first layer and there does not seem '
                          'to be any specified susceptibility rate. You can specify this '
                          'by passing `s_rate=Value` into this layer.' % self.layer_index)

        for prev_layer_index in self.prev_layer_indices:
            if layer_names[prev_layer_index] != 'Removed' and layer_names[prev_layer_index] != 'Recovered':
                warnings.warn('Previous layer at %s to the Susceptible layer at %s is neither Removed or '
                              'Recovered. If you want to create a layer which does this, add a custom '
                              'layer through `add_layer`. If not, fix the `layer_map`.' % (prev_layer_index,
                                                                                           self.layer_index))

    def get_deriv(self, time, system):
        """
        Derivative of the Susceptible compartment
        must be the *only* Susceptible compartment which people from other layers may enter

        :param time: time to take derivative at
        :param system: system of all states
        :return: derivative
        """

        total_infecteds = 0
        for infected_category_index in self.infected_category_indices:
            total_infecteds += system[infected_category_index]

        derivative = - self.gamma(time) * self.R_0(time) * system[self.layer_index] * \
                        total_infecteds / self.N(time)

        if self.first_layer:
            return derivative

        else:
            possible_new_susceptibles = 0
            for prev_layer_index in self.prev_layer_indices:
                possible_new_susceptibles += system[prev_layer_index]

            derivative += self.p_resusceptibility(time) * self.s_rate(time) * possible_new_susceptibles
            return derivative


class Infected(object):
    """
    The Infected class is the 'I' of the 'SIR' Model.
    This is the portion of individuals who are actively spreading the disease.
    Susceptible, Exposed --> Infected --> Recovered, Hospitalized, Critical, Dead
    STRUCTURE:
        - __init__
        - get_layer_index
        - test
        - get_deriv
    """

    def __init__(self, layer_index, N, R_0=None, gamma=None, delta=None, p_recovery=None, recovery_rate=None,
                 p_hospitalized=None, hospital_rate=None, p_critical=None, critical_rate=None,
                 p_death=None, death_rate=None):
        """
        Initialize the Infected class

        :param layer_index: index of layer in `layers`
        :param N: the total population
                  implemented as a function N(t):
                        - t: time
                        - return: total population
        :param R_0: =None, the basic reproductive number (only applicable if previous layer is Susceptible)
                    this is the average number of Susceptibles infected by one Infected
                    implemented as a function R_0(t):
                        - t: time
                        - return: R_0 value
        :param gamma: =None, the infectious period (only applicable if previous layer is Susceptible)
                      1 / average duration of infectious period
                      implemented as a function gamma(t):
                        - t: time
                        - return: infectious period
        :param delta: =None, the incubation period (only applicable if previous layer is Exposed)
                      implemented as a function delta(t)--in most cases this should stay constant
                        - t: time
                        - return: incubation period
        :param p_recovery: =None, probability of recovery
                      (only applicable if next layer is Recovered)
                      implemented as a function p_recovery(t):
                        - t: time
                        - return: probability of recovery
        :param recovery_rate: =None, the recovery rate--different from the standard recovery rate `gamma`
                                     measures only 1 / the time it takes to move to the Recovered layer
                      (only applicable if next layer is Recovered)
                      implemented as a function recovery_rate(t):
                        - t: time
                        - return: recovery rate
        :param p_hospitalized: =None, probability of hospitalization
                      (only applicable if next layer is Hospitalized)
                      implemented as a function p_hospitalized(t):
                        - t: time
                        - return: probability of hospitalization
        :param hospital_rate: =None, 1 / average time to hospitalization
                      (only applicable if next layer is Hospitalized)
                      implemented as a function hospital_rate(t)
                        - t: time
                        - return: hospitalization rate
        :param p_critical: =None, probability of becoming a critical patient
                      (only applicable if next layer is Critical)
                      implemented as a function p_critical(t)
                        - t: time
                        - return: critical probability
        :param critical_rate: =None, 1 / average time to becoming a critical patient
                      (only applicable if next layer is Critical)
                      implemented as a function critical_rate(t)
                        - t: time
                        - return: critical rate
        :param p_death: =None, probability of death (only applicable if next layer is Dead)
                      implemented as a function p_death(t)
                        - t: time
                        - return: death probability
        :param death_rate: =None, 1 / rate of death (only applicable if next layer is Dead)
                      implemented as a function death_rate(t)
                        - t: time
                        - return: death rate
        """

        self.layer_index = layer_index
        self.R_0 = R_0
        self.gamma = gamma
        self.delta = delta
        self.N = N
        self.p_recovery = p_recovery
        self.recovery_rate = recovery_rate
        self.p_hospitalized = p_hospitalized
        self.hospital_rate = hospital_rate
        self.p_critical = p_critical
        self.critical_rate = critical_rate
        self.p_death = p_death
        self.death_rate = death_rate

        self.prev_layer_type = None
        self.prev_layer_indices = []

    def get_layer_index(self):
        return self.layer_index

    def test(self, layer_map, layer_names):
        """
        Test of the `get_deriv` method
        Used to setup commonly used variables and raise common errors

        :param layer_map: next layers (as classes) for every layer in Model
        :param layer_names: layer names in system
        :return: derivative
        """

        # setup
        for layer_map_no in range(len(layer_map)):
            for next_layer in layer_map[layer_map_no]:
                if next_layer.get_layer_index() == self.layer_index:
                    self.prev_layer_type = layer_names[layer_map_no]
                    self.prev_layer_indices.append(layer_map_no)
                # warning if there are different input layer types
                if self.prev_layer_type is not None and next_layer.get_layer_index() == self.layer_index and \
                layer_names[layer_map_no] != self.prev_layer_type:
                    warnings.warn('Not all input layers to the Infected layer at %s are the same.'
                                  'Input layers to the Infected layer should either all be Susceptible'
                                  'or Exposed. Consider changing the `layer_map`' %
                                  self.layer_index)

        # warnings
        # undefined parameters
        if self.prev_layer_type == 'Susceptible' and not self.R_0:
            warnings.warn('The previous layer type to the Infected layer at %s is Susceptible and the '
                          'basic reproductive number is not defined. Please define as `R_0=Value`' %
                          self.layer_index)
        if self.prev_layer_type == 'Susceptible' and not self.gamma:
            warnings.warn('The previous layer type to the Infected layer at %s is Susceptible and the '
                          'recovery rate is not defined. Please define as `gamma=Value`' % self.layer_index)

        if self.prev_layer_type == 'Exposed' and not self.delta:
            warnings.warn('The previous layer type to the Infected layer at %s is Exposed and the '
                          'incubation period is not defined. Please define as `delta=Value`' % self.layer_index)

        # layer structures
        if self.prev_layer_type != 'Susceptible' and self.prev_layer_type != 'Exposed':
            warnings.warn('Input layer types to the Infected layer at %s must be either '
                          'Susceptible or Exposed. Consider changing the Input layers in `layer_map` '
                          'or creating a custom Infected layer using `add_layer`.' % self.layer_index)

    def get_deriv(self, time, system):
        """
        Derivative of the Infected compartment
        all layers feeding into the infected layer must be of the same type and either Susceptible or
        Exposed

        :param time: time to take derivative at
        :param system: system of all states
        :return: derivative
        """

        total_prev_layer = 0
        for prev_layer_index in self.prev_layer_indices:
            total_prev_layer += system[prev_layer_index]

        if self.prev_layer_type == 'Susceptible':
            derivative = self.gamma(time) * self.R_0(time) * total_prev_layer * \
                   system[self.layer_index] / self.N(time)
        if self.prev_layer_type == 'Exposed':
            derivative = self.delta(time) * total_prev_layer

        if self.p_recovery:
            derivative -= self.p_recovery(time) * self.recovery_rate(time) * system[self.layer_index]
        if self.p_hospitalized:
            derivative -= self.p_hospitalized(time) * self.hospital_rate(time) * system[self.layer_index]
        if self.p_critical:
            derivative -= self.p_critical(time) * self.critical_rate(time) * system[self.layer_index]
        if self.p_death:
            derivative -= self.p_death(time) * self.death_rate(time) * system[self.layer_index]

        return derivative


class Recovered(object):
    """
    The Recovered class is commonly confused with the 'R' of the 'SIR' Model.
    This class actually consists of individuals who have had the disease and recovered
    (i.e. did not die).
    This class can be used as a terminal state.
    Infected, Critical, Hospitalized --> Recovered --> Susceptible (?)
    STRUCTURE:
        - __init__
        - get_layer_index
        - test
        - get_deriv
    """

    def __init__(self, layer_index, p_from_inf=None, from_inf_rate=None, p_from_cri=None,
                 from_cri_rate=None, p_from_hos=None, from_hos_rate=None, p_resusceptibility=None,
                 s_rate=None):
        """
        Initialize the Recovered class

        :param layer_index: index of layer in `layers`
        :param p_from_inf: =None, probability of recovery from Infected (only applicable if previous layer is Infected)
                           implemented as a function p_from_inf(t)
                                - t: time
                                - return: probability of recovery
        :param from_inf_rate: =None, 1 / time to recover from Infected (only applicable if previous layer is Infected)
                           implemented as a function from_inf_rate(t)
                                - t: time
                                - return: recovery rate
        :param p_from_cri: =None, probability of recovery from Critical (only applicable if previous layer is Critical)
                           implemented as a function p_from_cri(t)
                                - t: time
                                - return: probability of recovery
        :param from_cri_rate: =None, 1 / time to recover from Critical (only applicable if previous layer is Critical)
                           implemented as a function from_cri_rate(t)
                                - t: time
                                - return: recovery rate
        :param p_from_hos: =None, probability of recovery from Hospitalized
                           (only applicable if previous layer is Hospitalized)
                           implemented as a function p_from_hos(t)
                                - t: time
                                - return: probability of recovery
        :param from_hos_rate: =None, 1 / time to recover from Hospitalized
                           (only applicable if previous layer is Hospitalized)
                           implemented as a function from_hos_rate(t)
                                - t: time
                                - return: recovery rate
        :param p_resusceptibility: =None, probability of resusceptibility (only applicable if next layer is Susceptible)
                           implemented as a function p_resusceptibility(t)
                                - t: time
                                - return: probability of resusceptibility
        :param s_rate: =None, 1 / time to resusceptibility (only applicable if next layer is Susceptible)
                           implemented as a function s_rate(t)
                                - t: time
                                - return: rate of resusceptibility
        """

        self.layer_index = layer_index
        self.p_from_inf = p_from_inf
        self.from_inf_rate = from_inf_rate
        self.p_from_cri = p_from_cri
        self.from_cri_rate = from_cri_rate
        self.p_from_hos = p_from_hos
        self.from_hos_rate = from_hos_rate
        self.p_resusceptibility = p_resusceptibility
        self.s_rate = s_rate

        self.prev_layer_indices_by_type = [[], [], []]  # in order [infected, critical, hospitalized]

    def get_layer_index(self):
        return self.layer_index

    def test(self, layer_map, layer_names):
        """
        Test of the `get_deriv` method
        Used to setup commonly used variables and raise common errors

        :param layer_map: next layers (as classes) for every layer in Model
        :param layer_names: layer names in system
        :return: derivative
        """

        # setup
        for layer_no in range(len(layer_map)):
            for next_layer in layer_map[layer_no]:
                if next_layer.get_layer_index() == self.layer_index:
                    if layer_names[layer_no] == 'Infected':
                        self.prev_layer_indices_by_type[0].append(layer_no)
                    elif layer_names[layer_no] == 'Critical':
                        self.prev_layer_indices_by_type[1].append(layer_no)
                    elif layer_names[layer_no] == 'Hospitalized':
                        self.prev_layer_indices_by_type[2].append(layer_no)
                    else:
                        warnings.warn('Previous layer at %s to Recovered layer at %s is not Infected, Critical, or '
                                      'Hospitalized. Consider either correcting the `layer_map` if this is not '
                                      'supposed to happen, or accomodating for this setup by using a custom '
                                      'Recovered layer.' % (layer_no, self.layer_index))

        # warnings
        for next_layer_index in range(len(layer_map[self.layer_index])):
            if layer_names[next_layer_index] != 'Susceptible':
                warnings.warn('The next layer to the Recovered layer at %s must be a Susceptible layer. '
                              'Change the `layer_map` to avoid this complication or use a custom layer.'
                              % self.layer_index)

    def get_deriv(self, time, system):
        """
        Derivative of the Recovered compartment

        :param time: time to take derivative at
        :param system: system of all states
        :return: derivative
        """

        derivative = 0

        # previous layers
        # infected
        for prev_layer_index in self.prev_layer_indices_by_type[0]:
            derivative += self.p_from_inf(time) * self.from_inf_rate(time) * system[prev_layer_index]

        # critical
        for prev_layer_index in self.prev_layer_indices_by_type[1]:
            derivative += self.p_from_cri(time) * self.from_cri_rate(time) * system[prev_layer_index]

        # hospitalized
        for prev_layer_index in self.prev_layer_indices_by_type[2]:
            derivative += self.p_from_hos(time) * self.from_hos_rate(time) * system[prev_layer_index]

        # next layers
        # susceptible
        if self.p_resusceptibility:
            derivative -= self.p_resusceptibility(time) * self.s_rate(time) * system[self.layer_index]

        return derivative


class Exposed(object):
    """
    The Exposed class represents the incubation period of the disease.
    This portion of individuals cannot spread the disease but are bound to become infected after some period of time.
    Susceptible --> Exposed --> Infected
    STRUCTURE:
        - __init__
        - get_layer_index
        - test
        - get_deriv
    """

    def __init__(self, layer_index, R_0, gamma, N, delta):
        """
        Initialize the Exposed class

        :param layer_index: index of layer in `layers`
        :param R_0: the basic reproductive number
                    this is the average number of Susceptibles infected by one Infected
                    implemented as a function R_0(t):
                        - t: time
                        - return: R_0 value
        :param gamma: the infectious period
                      1 / average duration of infectious period
                      implemented as a function gamma(t):
                        - t: time
                        - return: infectious period
        :param N: the total population
                  implemented as a function N(t):
                        - t: time
                        - return: total population
        :param delta: the incubation period (only applicable if previous layer is Exposed)
                      implemented as a function delta(t)--in most cases this should stay constant
                        - t: time
                        - return: incubation period
        """

        self.layer_index = layer_index
        self.R_0 = R_0
        self.gamma = gamma
        self.N = N
        self.delta = delta

        self.prev_layer_indices = []
        self.infected_category_indices = []

    def get_layer_index(self):
        return self.layer_index

    def test(self, layer_map, layer_names):
        """
        Test of the `get_deriv` method
        Used to setup commonly used variables and raise common errors

        :param layer_map: next layers (as classes) for every layer in Model
        :param layer_names: layer names in system
        :return: derivative
        """

        # setup
        for layer_no in range(len(layer_map)):
            for next_layer in layer_map[layer_no]:

                if next_layer.get_layer_index() == self.layer_index and \
                        layer_names[layer_no] == 'Susceptible':
                    self.prev_layer_indices.append(layer_no)

                # warning
                elif next_layer.get_layer_index() == self.layer_index:
                    warnings.warn('It seems like you want to connect the layer at %s to the Exposed layer at %s. '
                                  'However, only Susceptible layers can be fed into an Exposed layer. '
                                  'Consider creating a custom layer to handle this or remove the connection.' %
                                  (layer_no, self.layer_index))

        for next_layer_index in range(len(layer_map[self.layer_index])):

            if layer_names[layer_map[self.layer_index][next_layer_index].get_layer_index()] == 'Infected':
                self.infected_category_indices.append(layer_map[self.layer_index][next_layer_index].
                                                      get_layer_index())

            # warnings
            else:
                warnings.warn('It seems like you want to connect Exposed layer at %s to the layer at %s. '
                              'However, only Infected layers can be placed in front of Exposed layers. '
                              'Consider creating a custom layer to handle this or remove the connection.' %
                              (self.layer_index, next_layer_index))

        # warnings
        if len(self.prev_layer_indices) == 0:
            warnings.warn('It seems that the Exposed layer at %s is not in use. Please find a Susceptible '
                          'layer to route through this layer or remove this layer altogether.' %
                          self.layer_index)

    def get_deriv(self, time, system):
        """
        Derivative of the Exposed compartment

        :param time: time to take derivative at
        :param system: system of all states
        :return: derivative
        """

        total_susceptibles = 0
        for prev_layer_index in self.prev_layer_indices:
            total_susceptibles += system[prev_layer_index]

        total_infecteds = 0
        for infected_index in self.infected_category_indices:
            total_infecteds += system[infected_index]

        return self.gamma(time) * self.R_0(time) * total_susceptibles * \
               total_infecteds / self.N(time) - self.delta(time) * system[self.layer_index]
