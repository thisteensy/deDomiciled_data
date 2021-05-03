import csv
import os
import json
import api_fetcher

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
homeless_count_by_state = []
def pitcount_to_dictlist():
    """reads data from csv and creates a list"""

    global homeless_count_by_state
    directory = "data/PIT_csv_years"
    n = len(homeless_count_by_state)
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            with open(f"data/PIT_csv_years/{filename}", newline='') as csvfile:
                
                for row in csv.DictReader(csvfile):
                    year = int(filename[:4])
                    state_abr = row["CoC"][:2]
                    count = int(row["Count"])
                
                    filtered_list = [i for i in homeless_count_by_state if i.get('state_id') == state_abr and i.get('data_year') == year]                                   
                    
                    if filtered_list:
                        filtered_list[0]['pit_count'] += count
                    
                    else:
                        if state_abr in states:
                            name = states[state_abr]
                            homeless_count_by_state.append({'state_id' : state_abr,
                                                        'state_name': name,
                                                        'data_year' : year, 
                                                        'pit_count' : count})
                        else:
                            continue

                    
def lowrent_count_to_dictlist():
    """reads low income housing data from Pandas dataframe and adds it to a list"""

    global homeless_count_by_state
    for state, timeseries in api_fetcher.get_low_rent_count().items():
        for year, count in timeseries.items():
            filtered_list = [i for i in homeless_count_by_state if i.get('state_id') == state and i.get('data_year') == int(year)]
            if filtered_list:
                filtered_list[0]["li_rental_inv"] = int(count)

def belowpoverty_population_to_dictlist():
    """reads population below poverty data from Pandas dataframe and adds it into a list"""

    global homeless_count_by_state
    for state, timeseries in api_fetcher.get_belowpoverty_population().items():
        for year, count in timeseries.items():
            filtered_list = [i for i in homeless_count_by_state if i.get('state_id') == state and i.get('data_year') == int(year)]
            if filtered_list:
                filtered_list[0]["state_below_poverty"] = int(count)

def state_population_to_dictlist():
    """reads population below poverty data from Pandas dataframe and adds it into a list"""

    global homeless_count_by_state
    for state, timeseries in api_fetcher.get_state_population().items():
        for year, count in timeseries.items():
            filtered_list = [i for i in homeless_count_by_state if i.get('state_id') == state and i.get('data_year') == int(year)]
            if filtered_list:
                filtered_list[0]["state_population"] = int(count)
        




pitcount_to_dictlist()
lowrent_count_to_dictlist()
belowpoverty_population_to_dictlist()
state_population_to_dictlist()


with open('./data/deDomiciled.json', 'w') as f:
    json.dump(homeless_count_by_state, f)
