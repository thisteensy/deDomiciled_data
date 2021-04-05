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

with open('data/census/states_geoid.csv', 'r', newline='') as csvfile:
    od_geoid_to_stateid = csv.DictReader(csvfile)
    ordered_dict_list = list(od_geoid_to_stateid)[0]
    geoid_to_state_id = dict(ordered_dict_list)

print(geoid_to_state_id)

   


def get_low_rent_count():
    states = dcp.get_places_in(['country/USA'], 'State')['country/USA']
    counts = dcp.build_time_series_dataframe(states, 'Count_HousingUnit_WithRent_100To149USDollar')
    return counts

def get_state_population():
    population = []
    states = dcp.get_places_in(['country/USA'], 'State')['country/USA']
    for state in states:
        pop = (dcp.build_time_series(state, 'Count_Person'))
        if state in geoid_to_state_id:
            state_id = geoid_to_state_id[state]
        pop.append(state_id)

    # population = dcp.build_time_series_dataframe(states, 'Count_Person')

    return population



