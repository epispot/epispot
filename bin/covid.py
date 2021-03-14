from bs4 import BeautifulSoup
import requests
import re

if __name__ != "__main__":
    all_cases = []
    country_cases = []
    continent_cases = []
    last_updated_val = ""

    # Getting the data from https://www.worldometers.info/coronavirus/ via web scraping.
    source = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(source, "lxml")

    # Get last updated date
    for page_top in soup.find_all("div", id="page-top"):
        last_updated = page_top.find_next_sibling("div")
        last_updated_val = last_updated.text.strip("Last updated: ")

    # Getting the cases and then added to all_cases list of dictionary
    th_row = []
    table = soup.table
    table_rows = table.find_all("tr")
    for tr in table_rows:
        th = tr.find_all("th")
        td = tr.find_all("td")
        if th:
            for i in th:
                th_text = i.text
                if re.search("Country", th_text):
                    th_row.append("CountryOrRegion")
                elif re.search("Critical", th_text):
                    th_row.append("Critical")
                elif re.search("Cases/", th_text):
                    th_row.append("CasesPerOneMillion")
                elif re.search("Deaths/", th_text):
                    th_row.append("DeathsPerOneMillion")
                elif re.search("Tests/", th_text):
                    th_row.append("TestsPerOneMillion")
                else:
                    th_row.append(th_text)
            th_row.append("LastUpdated")
        if td:
            td_row = [j.text.strip() for j in td]
            td_row.append(last_updated_val)
            table_dict = dict(zip(th_row, td_row))
            all_cases.append(table_dict)

    # Filtering the list and create new list just for the Coutries and Continents
    region_remover = ["World", "Asia", "North America", "Europe",
                      "South America", "Oceania", "Africa", "Total:", ""]
    regions = ["Asia", "North America", "Europe",
               "South America", "Oceania", "Africa"]

    for search in all_cases:
        if search["CountryOrRegion"] not in region_remover:
            country_cases.append(search)
        if search["CountryOrRegion"] in regions:
            continent_cases.append(search)

    # Methods
    def get_global_cases():
        """
        Returns a dictionary of global cases 
        """
        result = None
        for search in all_cases:
            if search["CountryOrRegion"] == "World":
                result = search
        return result

    def get_country_cases(country=None):
        """
        Returns a dictionary for sepecific country or list of dictionaries for all coutries.

        Parameter:
        country =  Name of a Country that has COVID-19 case. Will return None if country is not available.
        """
        result = None
        if country:
            if not type(country) is str:
                raise TypeError("Parameter is not a string!")
            else:
                if country.upper() == "South Korea".upper():
                    country = "S. Korea".upper()
                for country_search in country_cases:
                    if country_search["CountryOrRegion"].upper() == country.upper():
                        result = country_search
                return result
        else:
            return country_cases

    def get_continent_cases(continent=None):
        """
        Returns a dictionary for sepecific continent or list of dictionaries for all continents.

        Parameter:
        continent =  Name of the continent that has COVID-19 case. Will return None if continent is not available.
        """
        result = None
        if continent:
            if not type(continent) is str:
                raise TypeError("Parameter is not a string!")
            else:
                for continent_search in continent_cases:
                    if continent_search["Continent"].upper() == continent.upper():
                        result = continent_search
                return result
        else:
            return continent_cases
