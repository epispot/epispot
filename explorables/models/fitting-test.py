import epispot as epi  # load the epi-spot package


def get_model_predictions(params):

    r_0_1 = params[0]
    r_0_2 = params[1]
    r_0_3 = params[2]
    gamma_1 = params[3]
    start_rec = params[4]

    # variables (used when defining layers)

    # basic reproductive number
    def R_0(t):
        if t < 38:
            return r_0_1
        elif t < 76:
            return r_0_2
        else:
            return r_0_3

    def gamma(t):
        return gamma_1

    # total population
    def N(t):
        return 883305

    # probability of recovering
    def p_recovery(t):
        return 1.0

    # layers
    Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)  # Susceptible layer
    Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_recovery, recovery_rate=gamma)  # Infected layer
    Recovered = epi.comps.Recovered(2, p_from_inf=p_recovery, from_inf_rate=gamma)  # Recovered layer

    # the blank array in `layer_map` symbolizes that the Recovered layer has no further layers
    Model = epi.models.Model(N(0), layers=[Susceptible, Infected, Recovered], layer_names=['Susceptible', 'Infected',
                                                                                           'Recovered'],
                             layer_map=[[Infected],
                                        [Recovered], []])  # compile the model out of the layers defined above

    # results
    result = Model.integrate(range(0, 114), starting_state=[883225, 80 - start_rec, start_rec])
    formatted_result = []
    for system in result:
        formatted_result.append([system[0], system[1] + system[2]])
    return formatted_result


parameters = [1.5, 1.5, 1.5, 0.0714, 0]
new_params = epi.fitters.grad_des(get_model_predictions, open('tests\models\sf-total-cases.csv'), parameters,
                                  3.0, 3, 883305, range(10, 110, 10))
print('\n')
print(new_params)

r_0_1 = new_params[0]
r_0_2 = new_params[1]
r_0_3 = new_params[2]
gamma_1 = new_params[3]
start_rec = new_params[4]


# variables (used when defining layers)

# basic reproductive number
def R_0(t):
    if t < 38:
        return r_0_1
    elif t < 76:
        return r_0_2
    else:
        return r_0_3


def gamma(t):
    return gamma_1


# total population
def N(t):
    return 883305


# probability of recovering
def p_recovery(t):
    return 1.0


# layers
Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)  # Susceptible layer
Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_recovery, recovery_rate=gamma)  # Infected layer
Recovered = epi.comps.Recovered(2, p_from_inf=p_recovery, from_inf_rate=gamma)  # Recovered layer

# the blank array in `layer_map` symbolizes that the Recovered layer has no further layers
Model = epi.models.Model(N(0), layers=[Susceptible, Infected, Recovered], layer_names=['Susceptible', 'Infected',
                                                                                       'Recovered'],
                         layer_map=[[Infected],
                                    [Recovered], []])  # compile the model out of the layers defined above

file = open('tests\models\sf-total-cases.csv').readlines()
data = [file[l].split(',') for l in range(1, len(file))]
for line in range(len(data)):
    for char in range(len(data[line])):
        data[line][char] = float(data[line][char])
for char in range(len(data[0])):
    data[0][char] = int(data[0][char])

print(abs(get_model_predictions(new_params)[-1][1] - data[-1][1]))
epi.plots.plot_comp_nums(Model, range(0, 500), starting_state=[883225, 80 - start_rec, start_rec])