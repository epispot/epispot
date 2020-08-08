# The Basic SIR Model
#### This serves as a basic overview of how the epi-spot library works.

Refer to `tests/basic-sir-model.py` for the 
complementary code to this tutorial.
<br><br>

## Importing
Let's begin by importing `epispot`. If you've installed 
it from the pip, then just use `import epispot`. 
Otherwise, import from the file that you have cloned 
the library to, as shown in the example.

1. Installed from pip
    1. Use `import epispot`
2. Cloned from GitHub
    1. Use `from DIRECTORY-NAME import epispot`

## Parameters
Before we dive into creating the `Model`, we need to 
establish some of the parameters that will be used to 
define out model.
<br><br>
**Note: if you aren't sure about which parameters are 
needed for a specific model, always consult the 
compartment docstrings using the built-in Python 
`help()` command.**
<br><br>

### 1. `R_0` (basic reproductive number)
This number represents the number of 
Susceptibles one Infected will infect, 
assuming that everyone else is Susceptible. A 
number greater than one means the disease is still 
spreading, whereas a number less than one means 
the disease is dying out. For reference, most 
epidemics have an `R_0` value of around 2.

### 2. `gamma` (recovery rate)
This variable is set to: <br>
`1 / avg time to recover` <br><br>
This acts as a buffer between the time an individual 
is infected and when that individual recovers.

### 3. `N` (total population)
This is, of course, the total population of the 
region in question.

### 4. `p_recovery` (probability of recovery)
The probability of recovery determines an individual's 
chances of recovering after `1 / gamma` days. This can 
be used as a proxy measure to increase or decrease 
`gamma` or can just be left as 1.

Before we finish this section, it is important to 
understand how parameters are implemented in epi-spot. 
**All parameters are functions.** This is because many 
parameters change over the course of a disease. Take 
`R_0` for example. As social distancing and 
quarantining measures are put in place, the disease 
spreads more slowly and Infecteds are only able to 
spread the disease to a fewer number of people, if at 
all. This essentially lowers `R_0` *during the course 
of the disease*. In order to do this in epi-spot, we 
simply change `R_0` as time progresses, as we will be 
doing in this example.

## Coding

For `R_0` we will use a simple logistic model, 
something that lowers `R_0` as a function of time: 
slowly at the beginning, fast as the outbreak emerges, 
and then slowly as `R_0` creeps to 0 in order to end 
the outbreak. We will use the following values:

`R_0` start value: 2.0 
`R_0` end value: 0.0
`gamma`: 0.2
`N`: 100,000
`p_recovery`: 1.0

Each function takes in a parameter `t` representing 
the time in days from the beginning of the outbreak. 
This is implemented in lines 1-27.

Next, we create an instance of each `layer` in the 
Model. These are listed in `epispot.comps`. Each 
layer contains a certain category of people, whether 
that be Susceptible, Infected, or Recovered. Before 
using any of them, be sure to look at which parameters 
to include depending on the next and previous layers. 
Here, we implement them as:
```python
Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)  # Susceptible layer
Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_recovery, recovery_rate=gamma)  # Infected layer
Recovered = epi.comps.Recovered(2, p_from_inf=p_recovery, from_inf_rate=gamma)  # Recovered layer
```
Next, we compile the Model class in `epispot.models`.
```python
Model = epi.models.Model(N(0), 
        layers=[Susceptible, Infected, Recovered], 
        layer_names=['Susceptible', 'Infected', 'Recovered'],
        layer_map=[[Infected], [Recovered], []])
```
The `layer_map` parameter here contains an array with 
an instance of the class of the next layer to each of 
the layers in the Model. It will be more useful later 
in complex models where we want to create different 
paths through each of the layers.
<br>
Lastly, we call
```python
epi.plots.plot_comp_nums(Model, range(0, 150, 1))
```
passing in our Model as one parameter and a time 
range that we would like to plot. This will return a 
matplotlib plot showing the values of each of those 
compartments over the timerange specified.
<br>
There you have it! You've completed the basic tutorial 
and understand the three main modules of epi-spot 
(comps, models, and plots) and how to use them!