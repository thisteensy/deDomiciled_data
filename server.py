from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db
import crud
import csv
import json

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def all_states_landing():
   
   all_states = crud.get_data_by_year(2019)
   years = reversed(range(2011, 2020))
   

   return render_template('index.html', all_states = all_states, years = years)

@app.route('/year/<data_year>')
def all_states_by_year(data_year):

   all_states = crud.get_data_by_year(data_year)
   years = reversed(range(2011, 2020))
   
   return render_template('index.html', all_states = all_states, years = years)



@app.route('/state/<state>') 
def show_state(state):
   

   return render_template("state.html", state = state)
   

@app.route('/load-state-data/<state>')
def send_yearsdata(state):

   dict_data_unsorted = []
   state_data = crud.get_data_by_state(state)
   
   for year in state_data:
      if year.data_year >= 2011:
         
         dict_data_unsorted.append({"date": year.data_year,
                                    "Unhoused Population": year.pit_count, 
                                    "Households Below Poverty": round(year.state_below_poverty/3),
                                    "Available Low Income Housing": year.li_rental_inv,
                                    "Total Population": year.state_population})
   dict_data = sorted(dict_data_unsorted, key = lambda i: i["date"])
   dict_data[0]["unhoused_percent_change"] = 0
   dict_data[0]["below_poverty_percent_change"] = 0
   dict_data[0]["available_housing_percent_change"] = 0
   dict_data[0]["population_percent_change"] = 0

   def get_percent_change(prior, current):
      return round(((current-prior)/prior)*100)
   

   
   for i, entry in enumerate(dict_data[1:]):
      entry["unhoused_percent_change"] = get_percent_change(dict_data[i]["Unhoused Population"], entry["Unhoused Population"])
      entry["below_poverty_percent_change"] = get_percent_change(dict_data[i]["Households Below Poverty"], entry["Households Below Poverty"])
      entry["available_housing_percent_change"] = get_percent_change(dict_data[i]["Available Low Income Housing"], entry["Available Low Income Housing"])
      entry["population_percent_change"] = get_percent_change(dict_data[i]["Total Population"], entry["Total Population"])
 
   print(dict_data)
   csv_file = "state_data.csv"
   fieldnames = [i for i in dict_data[0].keys()]
   
   
   with open(csv_file, 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for data in dict_data:
         writer.writerow(data)
   
   return open("state_data.csv", "r").read()
   

@app.route('/load-data/<year>')
def send_data(year):
   # fix this so that the map colors update properly
   data = []

   state_data = crud.get_data_by_year(year)

   state_ranking=[]
   print(state_ranking)

   for state in state_data:
      homeless_per100000 = round(state.pit_count/state.state_population*100000)
      state_ranking.append(homeless_per100000)

   state_ranking.sort()
   state_ranking_decile = {}
   state_ranking_decile[1]=state_ranking[:5]
   state_ranking_decile[2]=state_ranking[5:10]
   state_ranking_decile[3]=state_ranking[10:15]
   state_ranking_decile[4]=state_ranking[15:20]
   state_ranking_decile[5]=state_ranking[20:25]
   state_ranking_decile[6]=state_ranking[25:30]
   state_ranking_decile[7]=state_ranking[30:35]
   state_ranking_decile[8]=state_ranking[35:40]
   state_ranking_decile[9]=state_ranking[40:45]
   state_ranking_decile[10]=state_ranking[45:50]
   
   for state in state_data:
      homeless_per100000 = round(state.pit_count/state.state_population*100000)
      for key, values in state_ranking_decile.items():
         if homeless_per100000 in values:
            data.append([state.state_id, 
                        state.pit_count,
                        state.state_name,
                        homeless_per100000, 
                        key, year])
      

   
   return jsonify(data)


@app.route("/us-states.json")
def send_states():

   return open("us-states.json", "r").read()

# # @app.route('/about')

# #     """returns project about page"""
# #     pass

# # @app.route('/state')
# #     """get state by state id"""
# #     pass

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)