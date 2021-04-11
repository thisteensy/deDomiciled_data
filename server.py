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



# @app.route('/state/ <state_id>')
# def show_state(state_id):
   
#    state_data = crud.get_data_by_state_and_year(state_id)
   

#    return render_template("state.html", state_data = state_data)
   

@app.route('/load-data')
def send_data():
   
   data = []

   state_data = crud.get_data_by_year(2019)

   state_ranking=[]

   for state in state_data:
      homeless_per100000 = state.pit_count/state.state_population*100000
      state_ranking.append(homeless_per100000)

   state_ranking.sort()
   state_ranking_quintiles = {}
   state_ranking_quintiles[1]=state_ranking[:10]
   state_ranking_quintiles[2]=state_ranking[10:20]
   state_ranking_quintiles[3]=state_ranking[20:30]
   state_ranking_quintiles[4]=state_ranking[30:40]
   state_ranking_quintiles[5]=state_ranking[40:50]
   
   for state in state_data:
      homeless_per100000 = state.pit_count/state.state_population*100000
      for key, values in state_ranking_quintiles.items():
         if homeless_per100000 in values:
            data.append([state.state_id, 
                        state.pit_count,
                        state.state_name, 
                        homeless_per100000, 
                        key])
      

   
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