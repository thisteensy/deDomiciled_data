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

@app.route('/year <data_year>')
# def all_states_by_year(data_year):

#    chosen_year = request.form.get('data-year')
#    all_states = crud.get_data_by_year(data_year)
   
#    return redirect('/', all_states = all_states)



@app.route('/state/ <state_id>')
def show_state(state_id):
   
   state_data = crud.get_data_by_state_and_year(state_id)
   

   return render_template("state.html", state_data = state_data)
   

@app.route('/get-data')
def send_data():
   
   data = []

   state_data = crud.get_data_by_year(2019)
  
   for state in state_data:
      data.append([state.state_id, state.pit_count])

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