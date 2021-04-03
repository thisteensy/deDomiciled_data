from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def all_states_landing():
   
   all_states = crud.get_data_by_year(2019)

   return render_template('homepage.html', all_states = all_states)
@app.route('/year <data_year>')
def all_states_by_year(data_year):

   year_data = crud.get_data_by_year(data_year)
   return redirect('/')



@app.route('/state/ <state_id>')
def show_state(state_id):
   
   state_data = crud.get_data_by_state_and_year(state_id)
   
   print('**************************')
   print(state_data)
   print('**************************')
   return render_template("state.html", state_data = state_data)
   



# # @app.route('/about')

# #     """returns project about page"""
# #     pass

# # @app.route('/state')
# #     """get state by state id"""
# #     pass

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)