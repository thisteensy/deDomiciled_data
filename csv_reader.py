import csv
import os



def csv_to_dictlist():
    directory = "data/PIT_csv_years"
    homeless_count_by_state = []
    n = len(homeless_count_by_state)
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            with open(f"data/PIT_csv_years/{filename}", newline='') as csvfile:
                
                for row in csv.DictReader(csvfile):
                    year = int(filename[:4])
                    state_abr = row["CoC"][:2]
                    count = int(row["Count"])
                    # if homeless_count_by_state = []:
                    #     homeless_count_by_state.append({'state_id' : state_abr,
                    #                                       'data_year' : year, 
                    #                                       'pit_count' : count})
                    filtered_list = [i for i in homeless_count_by_state if i.get('state_id') == state_abr and i.get('data_year') == year]                                   
                    if filtered_list:
                        filtered_list[0]['pit_count'] += count
                    
                    else:
                        homeless_count_by_state.append({'state_id' : state_abr,
                                                        'data_year' : year, 
                                                        'pit_count' : count})
                        

    return homeless_count_by_state
