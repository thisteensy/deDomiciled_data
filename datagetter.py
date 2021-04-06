import pandas
import datacommons_pandas as dcp
import json
import csv
import os

states = {"AL":"Alabama",
          "AK":"Alaska",
          "AZ":"Arizona",
          "AR":"Arkansas",
          "CA":"California",
          "CO":"Colorado",
          "CT":"Connecticut",
          "DE":"Delaware",
          "FL":"Florida",
          "GA":"Georgia",
          "HI":"Hawaii",
          "ID":"Idaho",
          "IL":"Illinois",
          "IN":"Indiana",
          "IA":"Iowa",
          "KS":"Kansas",
          "KY":"Kentucky",
          "LA":"Louisiana",
          "ME":"Maine",
          "MD":"Maryland",
          "MA":"Massachusetts",
          "MI":"Michigan",
          "MN":"Minnesota",
          "MS":"Mississippi",
          "MO":"Missouri",
          "MT":"Montana",
          "NE":"Nebraska",
          "NV":"Nevada",
          "NH":"New Hampshire",
          "NJ":"New Jersey",
          "NM":"New Mexico",
          "NY":"New York",
          "NC":"North Carolina",
          "ND":"North Dakota",
          "OH":"Ohio",
          "OK":"Oklahoma",
          "OR":"Oregon",
          "PA":"Pennsylvania",
          "RI":"Rhode Island",
          "SC":"South Carolina",
          "SD":"South Dakota",
          "TN":"Tennessee",
          "TX":"Texas",
          "UT":"Utah",
          "VT":"Vermont",
          "VA":"Virginia",
          "WA":"Washington",
          "WV":"West Virginia",
          "WI":"Wisconsin",
          "WY":"Wyoming"}

geoIds = {"geoId/02":"AK",
        "geoId/01":"AL",
        "geoId/05":"AR",
        "geoId/04":"AZ",
        "geoId/06":"CA",
        "geoId/08":"CO",
        "geoId/09":"CT",
        "geoId/10":"DE",
        "geoId/12":"FL",
        "geoId/13":"GA",
        "geoId/15":"HI",
        "geoId/19":"IA",
        "geoId/16":"ID",
        "geoId/17":"IL",
        "geoId/18":"IN",
        "geoId/20":"KS",
        "geoId/21":"KY",
        "geoId/22":"LA",
        "geoId/25":"MA",
        "geoId/24":"MD",
        "geoId/23":"ME",
        "geoId/26":"MI",
        "geoId/27":"MN",
        "geoId/29":"MO",
        "geoId/28":"MS",
        "geoId/30":"MT",
        "geoId/37":"NC",
        "geoId/38":"ND",
        "geoId/31":"NE",
        "geoId/33":"NH",
        "geoId/34":"NJ",
        "geoId/35":"NM",
        "geoId/32":"NV",
        "geoId/36":"NY",
        "geoId/39":"OH",
        "geoId/40":"OK",
        "geoId/41":"OR",
        "geoId/42":"PA",
        "geoId/44":"RI",
        "geoId/45":"SC",
        "geoId/46":"SD",
        "geoId/47":"TN",
        "geoId/48":"TX",
        "geoId/49":"UT",
        "geoId/51":"VA",
        "geoId/50":"VT",
        "geoId/53":"WA",
        "geoId/55":"WI",
        "geoId/54":"WV",
        "geoId/56":"WY"}

def get_low_rent_count():
    states = dcp.get_places_in(['country/USA'], 'State')['country/USA']
    counts0 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_Upto100USDollar')
    counts1 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_100To149USDollar')
    counts2 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_150To199USDollar')
    counts3 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_200To249USDollar')
    counts4 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_250To299USDollar')
    counts5 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_300To349USDollar')
    counts6 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_350To399USDollar')
    counts7 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_400To449USDollar')
    counts8 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_450To499USDollar')
    counts9 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_500To549USDollar')
    counts10 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_550To599USDollar')
    counts11 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_600To649USDollar')
    counts12 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_650To699USDollar')
    counts13 = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_700To749USDollar')

    add_dfs_under350 = [counts1, counts2, counts3, counts4, counts5]
    add_dfs_under500 = [counts1, counts2, counts3, counts4, counts5, counts6, counts7, counts8]
    add_dfs_under750 = [counts1, counts2, counts3, counts4, counts5, counts6, counts7, counts8, counts9, counts10, counts11, counts12, counts13]

    years = list(range(2007,2020))
    counts = counts0
    for count in add_dfs_under750:
        counts = counts.add(count, fill_value=0)
    
    counts.drop(labels=["geoId/11", "geoId/72"], axis=0, inplace=True)
    counts.rename(index=geoIds, inplace = True, errors = "raise")


    return counts

def get_belowpoverty_population():
    states = dcp.get_places_in(['country/USA'], 'State')['country/USA']
    bp_population = dcp.build_time_series_dataframe(states, 'Count_Person_BelowPovertyLevelInThePast12Months')
    bp_population.drop(labels=["geoId/11", "geoId/72"], axis=0, inplace=True)
    bp_population.rename(index=geoIds, inplace = True, errors = "raise")
    
    return bp_population

def get_state_population():
    states = dcp.get_places_in(['country/USA'], 'State')['country/USA']
    years = list(range(2007,2020))
    string_years = [str(year) for year in years]
    population_male= dcp.build_time_series_dataframe(states, 'Count_Person_Male')
    population_female= dcp.build_time_series_dataframe(states, 'Count_Person_Female')
    population = population_male.add(population_female, fill_value=0)
    column_names = list(population)
    known_years = [year for year in string_years if year in column_names]

    pop_years = population[known_years]
    pop_years.drop(labels=["geoId/11", "geoId/72"], axis=0, inplace=True)
    pop_years.rename(index=geoIds, inplace = True, errors = "raise")
    
    

    return pop_years