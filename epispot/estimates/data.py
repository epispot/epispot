"""
The `epispot.estimates.data` module contains all of the estimates pulled from the literature regarding the parameters of specific diseases.
They are classified into a hierarchy of classes:

1. `epispot.estimates.utils.Disease` represents a specific disease (e.g. COVID-19)
2. `epispot.estimates.utils.Paper` represents a specific study published in the literature regarding a specific disease (e.g. Ganyani, et al. 2020)
3. `epispot.estimates.utils.Estimate` represents a specific parameter estimate presented in a particular paper about a specific disease
    (e.g. the recovery rate of COVID-19)

.. note::
    See `epispot.estimates.getters.query()` to get specific estimates from this file.

"""

# imports
from . import dt, utils

# COVID-19

# Estimates
beta_santos = utils.Estimate(
    id='beta',
    dist=lambda t: 2.93,
    name='Constant-valued approximation of Beta',
    description='Estimated using an SEIR model and fit via a genetic algorithm using data from the Philippines',
)
delta_santos = utils.Estimate(
    id='delta',
    dist=lambda t: 0.28,
    name='Constant-valued approximation of Delta',
    description='Estimated using an SEIR model and fit via a genetic algorithm using data from the Philippines; referred to in the paper as "sigma," though it still represents the incubation rate delta',
)
gamma_santos = utils.Estimate(
    id='gamma',
    dist=lambda t: 0.33,
    name='Constant-valued approximation of Gamma',
    description='Estimated using an SEIR model and fit via a genetic algorithm using data from the Philippines; represents the removal rate in particular (not recovery rate)',
)
kappa_tsay = utils.Estimate(
    id='kappa',
    dist=lambda t: 0.2,
    name='Average testing rate',
    description='Estimated using data from the U.S. in the context of an SEAIR model; represents the probability of asymptomatic individuals becoming officially confirmed as infected cases',
)
gamma_tsay = utils.Estimate(
    id='gamma',
    dist=lambda t: 0.0255,
    name='Average recovery rate',
    description='Estimated using data from the U.S. in the context of an SEAIR model; referred to as "beta" in the paper',
)
rho_tsay = utils.Estimate(
    id='rho',
    dist=lambda t: 0.0255,
    name='Average death rate',
    description='Estimated using data from the U.S. in the context of an SEAIR model; referred to as "mu" in the paper',
)
r0_bentout = utils.Estimate(
    id='r_0',
    dist=lambda t: 4.1,
    name='Estimated initial R Naught',
    description='Estimated using data from the beginning of Algeria\'s COVID-19 outbreak in the context of an SEIR model',
)
beta_bentout = utils.Estimate(
    id='beta',
    dist=lambda t: 0.41,
    name='Estimated initial Beta',
    description='Estimated using data from the beginning of Algeria\'s COVID-19 outbreak in the context of an SEIR model',
)
gamma_bentout = utils.Estimate(
    id='gamma',
    dist=lambda t: 0.1,
    name='Gamma approximation (pulled from various sources)',
    description='Estimated using data from the beginning of Algeria\'s COVID-19 outbreak in the context of an SEIR model; represents the removal (not recovery) rate',
)
delta_bentout = utils.Estimate(
    id='delta',
    dist=lambda t: 0.2,
    name='Delta approximation (pulled from various sources including the WHO Coronavirus dataset)',
    description='Estimated using data from the beginning of Algeria\'s COVID-19 outbreak in the context of an SEIR model; referred to as "lambda" in the paper',
)
gamma_mehra = utils.Estimate(
    id='gamma',
    dist=lambda t: 0.222,
    name='Average Gamma estimate',
    description='Estimated using data from South Korea and the U.S. in the context of a SQAIR model; represents the recovery rate; referred to as "g" in the paper',
)
rho_mehra = utils.Estimate(
    id='rho',
    dist=lambda t: 0.0257,
    name='Average Rho estimate',
    description='Estimated using data from South Korea and the U.S. in the context of a SQAIR model; represents the death rate; referred to as "mu sub d" in the paper',
)
kappa_mehra = utils.Estimate(
    id='kappa',
    dist=lambda t: 0.214,
    name='Average testing rate estimate',
    description='Estimated using data from South Korea and the U.S. in the context of a SQAIR model; represents the probability of asymptomatic individuals becoming officially confirmed as infected cases; referred to as "alpha" in the paper but renamed to kappa for consistency',
)

# Papers
santos = utils.Paper(
    ('Santos', 2022),
    params=[
        beta_santos,
        delta_santos,
        gamma_santos,
    ],
    metadata={
        'title': 'Parameter Estimation for a Modified SEIR Model of the COVID-19 Dynamics in the Philippines using Genetic Algorithm',
        'authors': ('Gabriel Lorenzo I. Santos'),
        'journal': 'medRxiv',
        'date': dt.datetime(2022, 5, 19),
        'url': 'https://www.medrxiv.org/content/10.1101/2022.05.17.22275187v1',
    },
    full='Santos, G. L. I. (2022). Parameter estimation for a modified SEIR model of the COVID-19 dynamics in the Philippines using genetic algorithm (p. 2022.05.17.22275187). medRxiv. https://www.medrxiv.org/content/10.1101/2022.05.17.22275187v1',
)
tsay = utils.Paper(
    ('Tsay', 'et al.', 2020),
    params=[
        kappa_tsay,
        gamma_tsay,
        rho_tsay,
    ],
    metadata={
        'title': 'Modeling, state estimation, and optimal control for the US COVID‑19 outbreak',
        'authors': ('Calvin Tsay', 'Fernando Lejarza', 'Mark A. Stadtherr', 'Michael Baldea'),
        'journal': 'Nature',
        'date': dt.datetime(2020, 7, 1),
        'url': 'https://www.fmda.org/COVID/Published-Peer-Reviewed-Journal-Articles/s41598-020-67459-8.pdf',
    },
    full='Tsay, C., Lejarza, F., Stadtherr, M. A., & Baldea, M. (2020). Modeling, state estimation, and optimal control for the US COVID-19 outbreak. Scientific Reports, 10(1), 10711. https://doi.org/10.1038/s41598-020-67459-8',
)
bentout = utils.Paper(
    ('Bentout', 'et al.', 2020),
    params=[
        r0_bentout,
        beta_bentout,
        gamma_bentout,
        delta_bentout,
    ],
    metadata={
        'title': 'Parameter estimation and prediction for coronavirus disease outbreak 2019 (COVID-19) in Algeria',
        'authors': ('Soufiane Bentout', 'Abdennasser Chekroun', 'Toshikazu Kuniya'),
        'journal': 'AIMS Public Health',
        'date': dt.datetime(2020, 5, 22),
        'url': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7327392/',
    },
    full='Bentout, Soufiane, Abdennasser Chekroun, and Toshikazu Kuniya. “Parameter Estimation and Prediction for Coronavirus Disease Outbreak 2019 (COVID-19) in Algeria.” AIMS Public Health 7, no. 2 (May 22, 2020): 306–18. https://doi.org/10.3934/publichealth.2020026.',
)
mehra = utils.Paper(
    ('Mehra', 'et al.', 2020),
    params=[
        gamma_mehra,
        rho_mehra,
        kappa_mehra,
    ],
    metadata={
        'title': 'Parameter Estimation and Prediction of COVID-19 Epidemic Turning Point and Ending Time of a Case Study on SIR/SQAIR Epidemic Models',
        'authors': ('Amir Hossein Amiri Mehra', 'Mohsen Shafieirad', 'Zohreh Abbasi', 'Iman Zamani'),
        'journal': 'Hindawi',
        'date': dt.datetime(2020, 12, 29),
        'url': 'https://www.hindawi.com/journals/cmmm/2020/1465923/',
    },
    full='Amiri Mehra, Amir Hossein, Mohsen Shafieirad, Zohreh Abbasi, and Iman Zamani. “Parameter Estimation and Prediction of COVID-19 Epidemic Turning Point and Ending Time of a Case Study on SIR/SQAIR Epidemic Models.” Computational and Mathematical Methods in Medicine 2020 (December 29, 2020): e1465923. https://doi.org/10.1155/2020/1465923.',
)

# Initialize
Covid = utils.Disease(
    id='SARS-CoV-2',
    papers=[
        santos,
        tsay,
        bentout,
        mehra,
    ],
    name='COVID-19',
    description='severe acute respiratory syndrome coronavirus 2',
)
