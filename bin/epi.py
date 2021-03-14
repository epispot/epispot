"""
Run the epispot package faster with high-level commands
Uses fire to initialize a CLI
"""

print('Initializing CLI ...')
import epispot as epi
try:
    import fire
except ModuleNotFoundError as E:
    errormsg = f'Please install fire via `pip install fire` in order to initialize a CLI.'
    raise ModuleNotFoundError(errormsg) from E

print('Preparing job ...')
import covid
import numpy as np
from matplotlib import pyplot as plt


"""
CLI functions
"""


def base():
    """
    Basic package information
    """

    print('\nPackage metadata: ')
    print('Version: ' + epi.__version__)
    print('\nFor more detailed package information, see `credits`')


def sources():
    """
    List credits for epi-cli contributions
    """

    print('\nepi-cli credits: ')
    print(' - The epi-cli would not have been possible without the many people who have contributed to the epispot '
               'organization on Github in order to end COVID-19.')
    print('    - The epispot organization on Github: https://www.github.com/epispot')
    print(' - COVID-19 data is gathered using the COVID-19-Data API along with a regions file to map certain regions '
               'to countries. If your country or region is missing, submit an issue on Github.')
    print('    COVID-19-Data API: https://github.com/jrclarete/COVID-19-Cases')
    print(' - Lastly, the Fire package was used to initialize the epi-cli: ')
    print('    - Fire: https://www.github.com/google/python-fire')
    print(' - The main Medium blog posts that inspired the epispot package are linked below:')
    print('    - https://towardsdatascience.com/infectious-disease-modelling-part-i-understanding-sir-28d60e29fdfc')
    print('    - https://q9i.medium.com/reopening-safely-the-data-science-approach-289fd86ef63')
    print(' - No docs have been posted at this time. Use --help to get command info.')


def regions():
    """
    List all available regions
    """

    print('Compiling list of regions ...')
    country_list = open('data/list-of-countries.csv', 'r').readlines()
    country_list = [country.replace('\n', '') for country in country_list]

    print('\nList of regions: ')
    print(', '.join(country_list))


def find(abbr):
    """
    Finds region by abbreviation
    For example:
        Bra for Brazil
        CR for Costa Rica
        tm for The Mediterranean
    Not case-sensitive
    """

    print('Loading list of regions ...')
    country_list = open('data/list-of-countries.csv').readlines()
    matches = []

    print('Searching for region ...')
    for country in country_list:

        country_words = country.split(' ')

        if len(country_words) > 1:

            country_abbr = []
            for word in country_words:
                country_abbr.append(list(word)[0])

            country_abbr = ''.join(country_abbr)
            if country_abbr.lower() == abbr.lower():
                print('')
                return country.replace('\n', '')

        else:

            country_letters = list(country.replace('\n', ''))
            string_letters = list(abbr)
            num_matches = 0

            for letter in range(0, min(len(country_letters), len(string_letters))):

                if country_letters[letter].lower() == string_letters[letter].lower():
                    num_matches += 1
                else:
                    break

            if num_matches != 0:
                matches.append((country.replace('\n', ''), num_matches))

    print('Comparing matches ...\n')
    max_matching = ('[Country]', 0)
    for match in matches:
        if match[1] > max_matching[1]:
            max_matching = match

    return max_matching[0]


# non-CLI
def out(region, case_info):
    """
    Output for a region with case_info
    """

    print(region + ' has ' + case_info['TotalCases'] + ' total confirmed cases')

    if case_info['NewCases'] != '':
        print('    ' + region + ' has ' + case_info['NewCases'] + ' new cases today')
    if case_info['TotalDeaths'] != '':
        print('    ' + region + ' has ' + case_info['TotalDeaths'] + ' total deaths')
    if case_info['NewDeaths'] != '':
        print('    ' + region + ' has ' + case_info['NewDeaths'] + ' new deaths today')
    if case_info['TotalRecovered'] != '':
        print('    ' + region + ' has ' + case_info['TotalRecovered'] + ' total recovered patients')
    if case_info['NewRecovered'] != '':
        print('    ' + region + ' has ' + case_info['NewRecovered'] + ' new recovered patients today')
    if case_info['ActiveCases'] != '':
        print('    ' + region + ' has ' + case_info['ActiveCases'] + ' estimated active cases')
    if case_info['Critical'] != '':
        print('    ' + region + ' has ' + case_info['Critical'] + ' patients in critical condition')
    if case_info['CasesPerOneMillion'] != '':
        print('    ' + region + ' has ' + case_info['CasesPerOneMillion'] + ' cases per 1M')
    if case_info['DeathsPerOneMillion'] != '':
        print('    ' + region + ' has ' + case_info['DeathsPerOneMillion'] + ' deaths per 1M')
    if case_info['TotalTests'] != '':
        print('    ' + region + ' has ' + case_info['TotalTests'] + ' total tests')
    if case_info['TestsPerOneMillion'] != '':
        print('    ' + region + ' has ' + case_info['TestsPerOneMillion'] + ' total tests per 1M')

    print('For reference, other statistics and notes are displayed below')
    if case_info['Population'] != '':
        print('    ' + region + ' has ' + case_info['Population'] + ' people')
    if case_info['Continent'] != '':
        print('    ' + region + ' is located in ' + case_info['Continent'])
    if case_info['LastUpdated'] != '':
        print('    Data for ' + region + ' was last updated as of ' + case_info['LastUpdated'])


def covid19(region='world'):
    """
    Get case data for a specific region or continent
    Also includes UN-distinguished areas such as the Holy See
    Includes many cruise ships that were once quarantined
    """

    print('Loading regions file ...')
    regions = open('data/regions.csv').readlines()
    regions_list = [line.split(',')[0] for line in regions]

    print('Identifying region type ...')
    if region != 'world':
        case_info = covid.get_country_cases(country=region)

    if region == 'world':

        print('Preparing statistics ...')
        case_info = covid.get_global_cases()
        print('')
        out(region, case_info)

    elif region in ['North America', 'South America', 'Europe', 'Africa', 'Asia', 'Australia']:

        print('Preparing statistics ...')
        case_info = covid.get_continent_cases(continent=region)
        print('')
        out(region, case_info)

    elif case_info is not None:

        print('')
        out(region, case_info)

    elif region in regions_list:

        print('Searching for region ...')
        line_num = 0
        for line in range(len(regions)):
            if region == regions[line].split(',')[0]:
                line_num = line

        print('Preparing statistics ...')
        region_countries = regions[line_num].split(',')
        total_cases = 0
        exceptions = 0
        exception_cases = []

        print('Locating region ...')
        for region_region in region_countries[1:]:
            case_info = covid.get_country_cases(country=region_region.replace('\n', ''))
            if case_info is not None:
                total_cases += int(case_info['TotalCases'].replace(',', ''))
            else:
                exceptions += 1
                exception_cases.append(region_region)

        print('')
        print(region + ' has ' + str(total_cases) + ' cases')
        if exceptions != 0:
            print('This search raised ' + str(exceptions) + ' exceptions for the following countries')
            print(exception_cases)

    else:

        print('Region not found ...')
        print('Searching for an abbreviation ...')

        guess = find(region)
        print('Here are results for ' + guess + ':')
        case_info = covid.get_country_cases(country=guess)

        if case_info:
            out(guess, case_info)
        else:
            print("Sorry, you can't use regional abbreviations just yet ...")


"""
Call CLI
"""

if __name__ == '__main__':
    fire.Fire()
