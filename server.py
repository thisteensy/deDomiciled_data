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
   
   # chosen_year = request.form.get('data_year')
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
   
   data = []
   state_data = crud.get_data_by_state(state)
   for year in state_data:
      data.append([year.state_id, 
                   year.state_name,
                   year.data_year, 
                   year.pit_count,
                   year.state_below_poverty,
                   year.li_rental_inv,
                   year.state_population])
   print('***************************')
   print(data)
   print('***************************')

   return render_template("state.html", data = data, state=state)
   

@app.route('/load-data/<year>')
def send_data(year):
   
   data = []

   state_data = crud.get_data_by_year(year)

   state_ranking=[]

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