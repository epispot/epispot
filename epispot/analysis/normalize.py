"""
The `epispot.analysis.normalize` module contains various functions intended for cleaning and normalizing raw epidemiological data.
Raw data must usually be sanitized through one or more of these functions before it can be used for forecasting.
This is also useful for processing data even without a forecasting model.

"""

def count(cases, percent):
    """
    Under or overcount the number of cases to account for data inaccuracies.
    For example, if cases are being undercounted by around 20%, overcounting by that amount will correct the data.
    This is only useful if cases are consistently under or overcounted by a given amount.

    ## Parameters

    `cases (list[int])`: The list of cases to be normalized.

    `percent (float)`: The percent by which to overcount or undercount the cases.
        Negative values will result in an undercount and positive values will overcount.
        Overcounting will correct undercounted data and vice versa.
        `percent` should always be a value within the range `[-1, 1]`.
        If `percent` is zero, no correction will be made.

    ## Returns

    Normalized cases (`list[float]`)

    """
    return [case * (1 + percent) for case in cases]

def active(deltas, period, delay=0):
    """
    Extract the number of *active* cases from a list of new confirmed cases per day.
    This works by taking a trailing sum over the number of days that infection usually lasts of all the new cases.
    There is also support for taking into account testing delay.

    ## Parameters

    `deltas (list[int])`: The list of new cases per day.

    `period (int)`: The average period of infectiousness.

    `delay=0 (int)`: The average delay before tests are administered to those infected with the disease.

    .. note::
        If `delay` is changed to any value other than `0`, the resulting list will be shorter than the original list by exactly `delay` timesteps.
        This is because there is no data to remedy the testing delay during these days.

    ## Returns

    A list of active cases at any given time (`list[int]`)

    """
    active = []
    for i in range(len(deltas) - delay):
        if i < period - delay:
            active.append(sum(deltas[:i + delay + 1]))
        else:
            active.append(sum(deltas[i - period + delay:i + delay + 1]))

    return active

def cumulative(deltas):
    """
    Convert a list of new cases per day to a list of cumulative cases.
    This is useful for plotting the cumulative cases over time.

    ## Parameters

    `deltas (list[int])`: The list of new cases per day.

    ## Returns

    A list of cumulative cases (`list[int]`)

    """
    return [sum(deltas[:i + 1]) for i, _ in enumerate(deltas)]

def deltas(cumulative):
    """
    Convert a list of cumulative cases to a list of new cases per day.
    This is useful for plotting the new cases over time.

    ## Parameters

    `cumulative (list[int])`: The list of cumulative cases.

    ## Returns

    A list of new cases per day (`list[int]`)

    """
    out = [cumulative[0]]
    for i in range(1, len(cumulative)):
        out.append(cumulative[i] - cumulative[i - 1])

    return out

def shift(count, delay):
    """
    Shift counts by a given amount.
    This is useful for shifting the data by a given amount to account for testing or other reporting delays.

    ## Parameters

    `count (list[int])`: The list of counts to be shifted.

    `delay (int)`: The number of days by which reporting was delayed.

    .. note::
        If `delay` is changed to any value other than `0`, the resulting list will be shorter than the original list by exactly `delay` timesteps.

    ## Returns

    A list of shifted counts (`list[int]`)

    """
    return count[delay:]

def bound(active, deltas, deaths):
    """
    Bound the number of deaths at any given timestep to the greatest number of people that could have died,
    calculated using the list of active cases and the change in cases each day.

    .. important::
        Ensure that all `active`, `deltas`, and `deaths` were calculated with the same `delay` parameter,
        otherwise you risk inaccurate results.
        They must also all be of the same length.

    ## Parameters

    `active (list[int])`: The list of active cases at any given time.

    `deltas (list[int])`: The list of new cases per day.

    `deaths (list[int])`: The list of new deaths per day.

    ## Returns

    A list of bounded new deaths per day (`list[int]`)

    """
    bounded = []
    for i, death in enumerate(deaths):
        if i == 0:
            bounded.append(death)
        else:
            bounded.append(min(
                death,
                -(active[i] - active[i - 1] - deltas[i])
            ))

    return bounded

def recovered(active, deltas, deaths):
    """
    Calculate the number of people that have recovered from the disease.
    This is calculated by subtracting the number of deaths from the net change in active cases.

    .. important::
        To avoid negative numbers, use `epispot.analysis.bound` to bound the number of deaths at any given timestep.
        Without this, small errors in fatality reporting can result in negative numbers of recovered individuals.

    ## Parameters

    `active (list[int])`: The list of active cases at any given time.

    `deltas (list[int])`: The list of new cases per day.

    `deaths (list[int])`: The list of new deaths per day.

    ## Returns

    A list of new recovered cases per day (`list[int]`)

    .. note::
        The first element of the returned list will be `0`, because it is impossible to calculate the net change in active cases at time `0`,
        and thus the number of recovering individuals.

    """
    recovered = [0]
    for i in range(1, len(active)):
        recovered.append(-(active[i] - active[i - 1] - deltas[i]) - deaths[i])

    return recovered
